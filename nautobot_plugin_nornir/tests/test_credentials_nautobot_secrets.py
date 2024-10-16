"""Unit Tests for NautobotORM Inventory with Nautobot Secrets Feature."""

import os
from unittest import mock

from django.test import TestCase
from nautobot.dcim.models import Device
from nautobot.extras.models.secrets import (
    Secret,
    SecretsGroup,
    SecretsGroupAccessTypeChoices,
    SecretsGroupAssociation,
    SecretsGroupSecretTypeChoices,
)
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister

from nautobot_plugin_nornir.plugins.credentials.settings_vars import PLUGIN_CFG
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory
from nautobot_plugin_nornir.tests.fixtures import create_test_data

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
        create_test_data()

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
        dev1 = Device.objects.get(name="device1")
        dev1.secrets_group = sec_group
        dev1.save()

        dev2 = Device.objects.get(name="device2")
        dev2.secrets_group = sec_group
        dev2.save()

    def test_hosts_credentials(self):
        """Ensure credentials is assigned to hosts."""
        # pylint: disable=duplicate-code
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
