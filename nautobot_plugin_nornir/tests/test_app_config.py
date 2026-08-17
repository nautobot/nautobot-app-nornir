"""Unit Tests for the App configuration defaults."""

from django.test import TestCase

from nautobot_plugin_nornir.constants import NORNIR_SETTINGS
from nautobot_plugin_nornir.db_management import RUNNER_SETTINGS
from nautobot_plugin_nornir.defaults import DEFAULT_NORNIR_SETTINGS, merge_nornir_settings

EXPECTED_DEFAULTS = {
    "inventory": "nautobot_plugin_nornir.plugins.inventory.nautobot_orm.NautobotORMInventory",
    "credentials": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
    "runner": {"plugin": "threaded", "options": {"num_workers": 20}},
}


class DefaultSettingsTests(TestCase):
    """Test cases for ensuring the App supplies its own defaults."""

    def test_nornir_settings_defaults_when_config_omits_them(self):
        """Ensure `nornir_settings` resolves to the App defaults when `PLUGINS_CONFIG` omits it."""
        self.assertEqual(NORNIR_SETTINGS, EXPECTED_DEFAULTS)

    def test_runner_settings_default_enables_threaded_db_cleanup(self):
        """Ensure `RUNNER_SETTINGS` derives the threaded runner that gates idle DB connection cleanup."""
        self.assertEqual(RUNNER_SETTINGS, {"plugin": "threaded", "options": {"num_workers": 20}})

    def test_partial_override_keeps_remaining_defaults(self):
        """Ensure an override that sets one key keeps the defaults for the keys it leaves out."""
        merged = merge_nornir_settings({"credentials": "my_app.creds.Custom"})

        self.assertEqual(merged["credentials"], "my_app.creds.Custom")
        self.assertEqual(merged["inventory"], EXPECTED_DEFAULTS["inventory"])
        self.assertEqual(merged["runner"], EXPECTED_DEFAULTS["runner"])

    def test_runner_override_replaces_the_whole_runner(self):
        """Ensure the merge stays one level deep, so `runner` is replaced rather than merged."""
        merged = merge_nornir_settings({"runner": {"plugin": "serial"}})

        self.assertEqual(merged["runner"], {"plugin": "serial"})

    def test_merge_does_not_mutate_the_declared_defaults(self):
        """Ensure a caller that mutates the merged result never affects `DEFAULT_NORNIR_SETTINGS`."""
        merged = merge_nornir_settings(None)
        merged["runner"]["options"]["num_workers"] = 1

        self.assertEqual(DEFAULT_NORNIR_SETTINGS["runner"]["options"]["num_workers"], 20)
