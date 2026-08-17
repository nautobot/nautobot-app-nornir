"""Unit Tests for the App configuration defaults."""

from django.conf import settings
from django.test import TestCase

from nautobot_plugin_nornir import NautobotPluginNornirConfig
from nautobot_plugin_nornir.constants import NORNIR_SETTINGS
from nautobot_plugin_nornir.db_management import RUNNER_SETTINGS


class DefaultSettingsTests(TestCase):
    """Test cases for ensuring the App supplies its own defaults."""

    def test_default_settings_merged_into_plugins_config(self):
        """Ensure Nautobot merges `default_settings` when the config omits `nornir_settings`."""
        self.assertEqual(
            settings.PLUGINS_CONFIG["nautobot_plugin_nornir"]["nornir_settings"],
            NautobotPluginNornirConfig.default_settings["nornir_settings"],
        )

    def test_nornir_settings_resolves_inventory_default(self):
        """Ensure the inventory plugin path comes from the defaults."""
        self.assertEqual(
            NORNIR_SETTINGS["inventory"],
            "nautobot_plugin_nornir.plugins.inventory.nautobot_orm.NautobotORMInventory",
        )

    def test_nornir_settings_resolves_credentials_default(self):
        """Ensure the credentials provider path comes from the defaults."""
        self.assertEqual(
            NORNIR_SETTINGS["credentials"],
            "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
        )

    def test_runner_defaults_to_threaded_plugin(self):
        """Ensure the threaded runner is the default, which enables idle DB connection cleanup."""
        self.assertEqual(RUNNER_SETTINGS.get("plugin"), "threaded")

    def test_runner_defaults_to_twenty_workers(self):
        """Ensure the default worker count is applied."""
        self.assertEqual(RUNNER_SETTINGS["options"]["num_workers"], 20)
