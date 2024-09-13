"""Unit Tests for NautobotORM Inventory."""

from unittest.mock import patch

from django.test import TestCase
from nautobot.dcim.models import Device

from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory
from nautobot_plugin_nornir.constants import CONNECTION_SECRETS_PATHS, DRIVERS, PLUGIN_CFG
from nautobot_plugin_nornir.tests.fixtures import create_test_data


class NautobotORMInventoryTests(TestCase):
    """Test cases for ensuring the NautobotORM Inventory is working properly."""

    def setUp(self):
        """Create a superuser and token for API calls."""
        create_test_data()

    def test_init_default(self):
        """Ensure inventory is working properly with default settings."""
        inv = NautobotORMInventory().load()
        self.assertEqual(len(inv.hosts), 2)

    def test_init_queryset(self):
        """Ensure the inventory is working properly when a queryset is provided."""
        queryset = Device.objects.filter(name="device1")
        inv = NautobotORMInventory(queryset=queryset).load()
        self.assertEqual(len(inv.hosts), 1)

    def test_init_filters_device(self):
        """Ensure the inventory is working properly when a filters dict is provided."""
        inv = NautobotORMInventory(filters={"name": "device1"}).load()
        self.assertEqual(len(inv.hosts), 1)

    def test_hosts_platform(self):
        """Ensure platform is assigned to hosts."""
        inv = NautobotORMInventory().load()
        self.assertEqual(inv.hosts["device1"]["connection_options"]["napalm"]["platform"], "junos")
        self.assertEqual(inv.hosts["device2"]["connection_options"]["napalm"]["platform"], "junos")

    def test_get_all_devices_to_parent_mapping(self):
        """Ensure the mapping of devices to parents is correct."""
        self.assertEqual(
            NautobotORMInventory().get_all_devices_to_parent_mapping(),
            {
                "device1": ["location__USWEST", "location__US"],
                "device2": ["location__USWEST", "location__US"],
            },
        )

    @patch("nautobot_plugin_nornir.plugins.inventory.nautobot_orm.ALLOWED_LOCATION_TYPES", ["Region"])
    def test_get_all_devices_to_parent_mapping_allowed(self):
        """Ensure the mapping of devices to parents is correct with allowed locations."""
        self.assertEqual(
            NautobotORMInventory().get_all_devices_to_parent_mapping(),
            {
                "device1": ["location__US"],
                "device2": ["location__US"],
            },
        )

    @patch("nautobot_plugin_nornir.plugins.inventory.nautobot_orm.DENIED_LOCATION_TYPES", ["Site"])
    def test_get_all_devices_to_parent_mapping_denied(self):
        """Ensure the mapping of devices to parents is correct with denied locations."""
        self.assertEqual(
            NautobotORMInventory().get_all_devices_to_parent_mapping(),
            {
                "device1": ["location__US"],
                "device2": ["location__US"],
            },
        )

    def test_credentials_path(self):
        """Ensure credentials path is getting built."""
        self.assertEqual(
            CONNECTION_SECRETS_PATHS,
            {
                "netmiko": "netmiko.extras.secret",
                "napalm": "napalm.extras.optional_args.secret",
                "pyntc": "pyntc.extras.secret",
                "scrapli": "scrapli.extras.auth_secondary",
            },
        )

    @patch.dict(
        PLUGIN_CFG,
        {
            "nornir_settings": {
                "credentials": "nautobot_plugin_nornir.plugins.credentials.settings_vars.CredentialsSettingsVars",
            },
            "connection_options": None,
        },
    )
    def test_credentials_path_drivers_defaults(self):
        """Ensure credentials path is getting built."""
        self.assertEqual(sorted(DRIVERS), sorted(["napalm", "netmiko", "scrapli", "pyntc"]))

        # global_options = PLUGIN_CFG.get("connection_options", {item: {} for item in DRIVERS})
        # drivers = list(set(DRIVERS + list(PLUGIN_CFG.get("connection_options", {}).keys())))
        # self.assertEqual(list(global_options.keys()), drivers)

    @patch.dict(
        PLUGIN_CFG,
        {
            "nornir_settings": {
                "credentials": "nautobot_plugin_nornir.plugins.credentials.settings_vars.CredentialsSettingsVars",
            },
            "connection_options": {
                "napalm": {
                    "extras": {
                        "optional_args": {"global_delay_factor": 1},
                    },
                },
                "netmiko": {
                    "extras": {
                        "global_delay_factor": 1,
                    },
                },
            },
        },
    )
    def test_credentials_path_drivers_global_override(self):
        """Ensure credentials path is getting built."""
        global_options = PLUGIN_CFG.get("connection_options", {item: {} for item in DRIVERS})
        self.assertEqual(sorted(global_options), sorted(["napalm", "netmiko"]))
