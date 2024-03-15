"""Unit Tests for NautobotORM Inventory with Nautobot Secrets Feature."""
import os
from unittest import mock
from django.test import TestCase
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister
from nautobot.dcim.models import Device, DeviceType, Manufacturer, Platform, LocationType, Location
from nautobot.extras.models.secrets import (
    SecretsGroup,
    Secret,
    SecretsGroupAssociation,
    SecretsGroupAccessTypeChoices,
    SecretsGroupSecretTypeChoices,
)
from nautobot.extras.models.roles import ContentType, Role
from nautobot.extras.models.statuses import Status
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory
from nautobot_plugin_nornir.plugins.credentials.settings_vars import PLUGIN_CFG

InventoryPluginRegister.register("nautobot-inventory", NautobotORMInventory)


@mock.patch.dict(
    PLUGIN_CFG,
    {
        "nornir_settings": {
            "credentials": "nautobot_plugin_nornir.plugins.credentials.nautobot_secrets.CredentialsNautobotSecrets",
        },
    },
)
@mock.patch.dict(os.environ, {"NET_FIREWALL_USERNAME": "fw-user"})
@mock.patch.dict(os.environ, {"NET_FIREWALL_PASSWORD": "fw-password123"})
@mock.patch.dict(os.environ, {"NET_FIREWALL_SECRET": "fw-secret123"})
@mock.patch.dict(os.environ, {"NET_SWITCH_USERNAME": "sw-user"})
@mock.patch.dict(os.environ, {"NET_SWITCH_PASSWORD": "sw-password123"})
@mock.patch.dict(os.environ, {"NET_SWITCH_SECRET": "sw-secret123"})
class SecretsGroupCredentialTests(TestCase):
    """Test cases for ensuring the NautobotORM Inventory is working properly with Secrets Feature."""

    def setUp(self):
        """Create a superuser and token for API calls."""
        device_content_type = ContentType.objects.get(model="device")
        location_type_region = LocationType.objects.create(name="Region")
        self.location_type = LocationType.objects.create(name="Site")
        self.location_type.content_types.set([device_content_type])
        active = Status.objects.get(name="Active")
        location_us = Location.objects.create(
            name="US",
            location_type=location_type_region,
            status_id=active.id,
        )
        self.location = Location.objects.create(
            name="USWEST",
            parent=location_us,
            location_type_id=self.location_type.id,
            status_id=active.id,
        )
        self.manufacturer1 = Manufacturer.objects.create(name="Juniper")
        self.platform = Platform.objects.create(
            name="Juniper Junos", network_driver="juniper_junos", napalm_driver="junos"
        )

        self.device_type1 = DeviceType.objects.create(model="SRX3600", manufacturer=self.manufacturer1)
        self.device_role1 = Role.objects.create(name="Firewall")
        self.device_role1.content_types.set([device_content_type])
        self.device_role2 = Role.objects.create(name="Switch")
        self.device_role2.content_types.set([device_content_type])

        user_user = Secret.objects.create(
            name="Environment Vars User",
            parameters={"variable": "NET_{{ obj.role.name | upper }}_USERNAME"},
            provider="environment-variable",
        )
        password = Secret.objects.create(
            name="Environment Vars Password",
            parameters={"variable": "NET_{{ obj.role.name | upper  }}_PASSWORD"},
            provider="environment-variable",
        )
        secret = Secret.objects.create(
            name="Environment Vars Secret",
            parameters={"variable": "NET_{{ obj.role.name | upper  }}_SECRET"},
            provider="environment-variable",
        )

        sec_group = SecretsGroup.objects.create(name="Environment Vars SG")
        SecretsGroup.objects.create(name="Net Creds")
        SecretsGroupAssociation.objects.create(
            secret=user_user,
            secrets_group=sec_group,
            access_type=SecretsGroupAccessTypeChoices.TYPE_GENERIC,
            secret_type=SecretsGroupSecretTypeChoices.TYPE_USERNAME,
        )
        SecretsGroupAssociation.objects.create(
            secret=password,
            secrets_group=sec_group,
            access_type=SecretsGroupAccessTypeChoices.TYPE_GENERIC,
            secret_type=SecretsGroupSecretTypeChoices.TYPE_PASSWORD,
        )
        SecretsGroupAssociation.objects.create(
            secret=secret,
            secrets_group=sec_group,
            access_type=SecretsGroupAccessTypeChoices.TYPE_GENERIC,
            secret_type=SecretsGroupSecretTypeChoices.TYPE_SECRET,
        )
        Device.objects.create(
            name="device1",
            location=self.location,
            device_type=self.device_type1,
            platform=self.platform,
            role=self.device_role1,
            status_id=active.id,
            secrets_group=sec_group,
        )

        Device.objects.create(
            name="device2",
            location=self.location,
            device_type=self.device_type1,
            platform=self.platform,
            role=self.device_role2,
            status_id=active.id,
            secrets_group=sec_group,
        )

    def test_hosts_credentials(self):
        """Ensure credentials is assigned to hosts."""
        qs = Device.objects.all()
        nr_obj = InitNornir(
            inventory={
                "plugin": "nautobot-inventory",
                "options": {
                    "credentials_class": PLUGIN_CFG["nornir_settings"]["credentials"],
                    "params": PLUGIN_CFG["nornir_settings"].get("inventory_params"),
                    "queryset": qs,
                },
            },
        )
        self.assertEqual(nr_obj.inventory.hosts["device1"].username, "fw-user")
        self.assertEqual(nr_obj.inventory.hosts["device1"].password, "fw-password123")
        self.assertEqual(
            nr_obj.inventory.hosts["device1"]["connection_options"]["netmiko"]["extras"]["secret"], "fw-secret123"
        )
        self.assertEqual(
            nr_obj.inventory.hosts["device1"]["connection_options"]["napalm"]["extras"]["optional_args"]["secret"],
            "fw-secret123",
        )
        # self.assertEqual(
        #     nr_obj.inventory.hosts["device1"]["connection_options"]["pyntc"]["extras"]["secret"], "credsenv-secret123"
        # )
        # self.assertEqual(
        #     nr_obj.inventory.hosts["device1"]["connection_options"]["scrapli"]["extras"]["auth_secondary"], "credsenv-secret123"
        # )
        self.assertEqual(nr_obj.inventory.hosts["device1"]["connection_options"]["napalm"]["platform"], "junos")
        self.assertEqual(nr_obj.inventory.hosts["device2"].username, "sw-user")
        self.assertEqual(nr_obj.inventory.hosts["device2"].password, "sw-password123")
        self.assertEqual(
            nr_obj.inventory.hosts["device2"]["connection_options"]["netmiko"]["extras"]["secret"], "sw-secret123"
        )
        self.assertEqual(
            nr_obj.inventory.hosts["device2"]["connection_options"]["napalm"]["extras"]["optional_args"]["secret"],
            "sw-secret123",
        )
        # self.assertEqual(
        #     nr_obj.inventory.hosts["device2"]["connection_options"]["pyntc"]["extras"]["secret"], "credsenv-secret123"
        # )
        # self.assertEqual(
        #     nr_obj.inventory.hosts["device2"]["connection_options"]["scrapli"]["extras"]["auth_secondary"], "credsenv-secret123"
        # )
        self.assertEqual(nr_obj.inventory.hosts["device2"]["connection_options"]["napalm"]["platform"], "junos")
