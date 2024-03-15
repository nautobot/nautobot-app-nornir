"""Unit Tests for NautobotORM Inventory with Environment Vars."""
import os
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
            "credentials": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
        },
    },
)
@mock.patch.dict(os.environ, {"NAPALM_USERNAME": "credsenv-user"})
@mock.patch.dict(os.environ, {"NAPALM_PASSWORD": "credsenv-password123"})
@mock.patch.dict(os.environ, {"DEVICE_SECRET": "credsenv-secret123"})
class EnvironmentVarCredentialTests(TestCase):
    """Test cases for ensuring the NautobotORM Inventory is working properly with env vars."""

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
        self.assertEqual(nr_obj.inventory.hosts["device1"].username, "credsenv-user")
        self.assertEqual(nr_obj.inventory.hosts["device1"].password, "credsenv-password123")
        self.assertEqual(
            nr_obj.inventory.hosts["device1"]["connection_options"]["netmiko"]["extras"]["secret"], "credsenv-secret123"
        )
        self.assertEqual(
            nr_obj.inventory.hosts["device1"]["connection_options"]["napalm"]["extras"]["optional_args"]["secret"],
            "credsenv-secret123",
        )
        # self.assertEqual(
        #     nr_obj.inventory.hosts["device1"]["connection_options"]["pyntc"]["extras"]["secret"], "credsenv-secret123"
        # )
        # self.assertEqual(
        #     nr_obj.inventory.hosts["device1"]["connection_options"]["scrapli"]["extras"]["auth_secondary"], "credsenv-secret123"
        # )
        self.assertEqual(nr_obj.inventory.hosts["device1"]["connection_options"]["napalm"]["platform"], "junos")
        self.assertEqual(nr_obj.inventory.hosts["device2"].username, "credsenv-user")
        self.assertEqual(nr_obj.inventory.hosts["device2"].password, "credsenv-password123")
        self.assertEqual(
            nr_obj.inventory.hosts["device2"]["connection_options"]["netmiko"]["extras"]["secret"], "credsenv-secret123"
        )
        self.assertEqual(
            nr_obj.inventory.hosts["device2"]["connection_options"]["napalm"]["extras"]["optional_args"]["secret"],
            "credsenv-secret123",
        )
        # self.assertEqual(
        #     nr_obj.inventory.hosts["device2"]["connection_options"]["pyntc"]["extras"]["secret"], "credsenv-secret123"
        # )
        # self.assertEqual(
        #     nr_obj.inventory.hosts["device2"]["connection_options"]["scrapli"]["extras"]["auth_secondary"], "credsenv-secret123"
        # )
        self.assertEqual(nr_obj.inventory.hosts["device2"]["connection_options"]["napalm"]["platform"], "junos")
