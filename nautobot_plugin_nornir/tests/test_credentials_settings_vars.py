"""Unit Tests for NautobotORM Inventory with Settings Vars."""
from unittest import mock
from django.test import TestCase
from nautobot.dcim.models import Device, DeviceType, Manufacturer, Platform, LocationType, Location
from nautobot.extras.models.roles import ContentType, Role
from nautobot.extras.models.statuses import Status
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory
from nautobot_plugin_nornir.plugins.credentials.settings_vars import PLUGIN_CFG
from nornir.core.plugins.inventory import InventoryPluginRegister


from nornir import InitNornir

InventoryPluginRegister.register("nautobot-inventory", NautobotORMInventory)


@mock.patch.dict(
    PLUGIN_CFG,
    {
        "nornir_settings": {
            "credentials": "nautobot_plugin_nornir.plugins.credentials.settings_vars.CredentialsSettingsVars",
        },
        "username": "settings-ntc",
        "password": "settings-password123",
        "secret": "settings-secret123",
    },
)
class SettingsVarCredentialTests(TestCase):
    """Test cases for ensuring the NautobotORM Inventory is working properly with settings vars."""

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

        Device.objects.create(
            name="device1",
            location=self.location,
            device_type=self.device_type1,
            platform=self.platform,
            role=self.device_role1,
            status_id=active.id,
        )

        Device.objects.create(
            name="device2",
            location=self.location,
            device_type=self.device_type1,
            platform=self.platform,
            role=self.device_role2,
            status_id=active.id,
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
        self.assertEqual(nr_obj.inventory.hosts["device1"].username, "settings-ntc")
        self.assertEqual(nr_obj.inventory.hosts["device1"].password, "settings-password123")
        self.assertEqual(
            nr_obj.inventory.hosts["device1"]["connection_options"]["netmiko"]["extras"]["secret"], "settings-secret123"
        )
        self.assertEqual(
            nr_obj.inventory.hosts["device1"]["connection_options"]["napalm"]["extras"]["optional_args"]["secret"],
            "settings-secret123",
        )
        # self.assertEqual(
        #     nr_obj.inventory.hosts["device1"]["connection_options"]["pyntc"]["extras"]["secret"], "settings-secret123"
        # )
        # self.assertEqual(
        #     nr_obj.inventory.hosts["device1"]["connection_options"]["scrapli"]["extras"]["auth_secondary"], "settings-secret123"
        # )
        self.assertEqual(
            nr_obj.inventory.hosts["device1"]["connection_options"]["napalm"]["platform"], self.platform.napalm_driver
        )
        self.assertEqual(nr_obj.inventory.hosts["device2"].username, "settings-ntc")
        self.assertEqual(nr_obj.inventory.hosts["device2"].password, "settings-password123")
        self.assertEqual(
            nr_obj.inventory.hosts["device2"]["connection_options"]["netmiko"]["extras"]["secret"], "settings-secret123"
        )
        self.assertEqual(
            nr_obj.inventory.hosts["device2"]["connection_options"]["napalm"]["extras"]["optional_args"]["secret"],
            "settings-secret123",
        )
        # self.assertEqual(
        #     nr_obj.inventory.hosts["device2"]["connection_options"]["pyntc"]["extras"]["secret"], "settings-secret123"
        # )
        # self.assertEqual(
        #     nr_obj.inventory.hosts["device2"]["connection_options"]["scrapli"]["extras"]["auth_secondary"], "settings-secret123"
        # )
        self.assertEqual(
            nr_obj.inventory.hosts["device2"]["connection_options"]["napalm"]["platform"], self.platform.napalm_driver
        )
