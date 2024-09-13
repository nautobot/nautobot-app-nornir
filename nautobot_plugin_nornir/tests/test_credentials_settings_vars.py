"""Unit Tests for NautobotORM Inventory with Settings Vars."""

from unittest import mock
from django.test import TestCase
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister
from nautobot.dcim.models import Device
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory
from nautobot_plugin_nornir.plugins.credentials.settings_vars import PLUGIN_CFG
from nautobot_plugin_nornir.tests.fixtures import create_test_data

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
        create_test_data()

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
        self.assertEqual(nr_obj.inventory.hosts["device1"]["connection_options"]["napalm"]["platform"], "junos")
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
        self.assertEqual(nr_obj.inventory.hosts["device2"]["connection_options"]["napalm"]["platform"], "junos")
