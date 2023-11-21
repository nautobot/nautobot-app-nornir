"""Plugin declaration for nautobot_plugin_nornir."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import NautobotAppConfig
from nautobot_plugin_nornir.utils import verify_setting


class NautobotPluginNornirConfig(NautobotAppConfig):
    """Plugin configuration for nautobot_plugin_nornir."""

    name = "nautobot_plugin_nornir"
    verbose_name = "Nautobot Plugin for Nornir"
    version = __version__
    author = "Network to Code, LLC"
    description = (
        "Nautobot App that provides a shim layer to simplify using Nornir within other Nautobot Apps and Nautobot Jobs"
    )
    base_url = "plugin-nornir"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}

    def ready(self):
        """Check for accidental legacy configurations."""
        from django.conf import settings  # pylint: disable=import-outside-toplevel

        plugin_settings = settings.PLUGINS_CONFIG["nautobot_plugin_nornir"]

        dispatcher_mapping_message = (
            "The `dispatcher_mapping` key is no longer functional, failing early "
            "to ensure your application works as expected, please see: "
            "https://docs.nautobot.com/projects/plugin-nornir/en/latest/admin/migrating_to_v2/#dispatcher-settings for more details."
        )
        verify_setting(plugin_settings, "dispatcher_mapping", dispatcher_mapping_message)
        custom_dispatcher_message = (
            "The `custom_dispatcher` key is only meant for `golden_config_plugin` settings "
            "and not `nautobot_plugin_nornir` settings, please see: "
            "https://docs.nautobot.com/projects/plugin-nornir/en/latest/admin/migrating_to_v2/#dispatcher-settings for more details."
        )
        verify_setting(plugin_settings, "custom_dispatcher", custom_dispatcher_message)
        verify_setting(
            plugin_settings, "credentials", "The `credentials` key should be within the `nornir_settings` dictionary"
        )
        verify_setting(
            plugin_settings, "runners", "The `runners` key should be within the `nornir_settings` dictionary"
        )
        verify_setting(
            plugin_settings,
            "nornir_settings.connection_options",
            "The `connection_options` key should NOT be within the `nornir_settings` dictionary",
        )
        verify_setting(
            plugin_settings,
            "nornir_settings.use_config_context",
            "The `use_config_context` key should NOT be within the `nornir_settings` dictionary",
        )
        # TODO: Commenting the below out, which I believe are correct but want to verify first
        # verify_setting(plugin_settings, "nornir_settings.username", "The `username` key should NOT be within the `nornir_settings` dictionary")
        # verify_setting(plugin_settings, "nornir_settings.password", "The `password` key should NOT be within the `nornir_settings` dictionary")
        # verify_setting(plugin_settings, "nornir_settings.secret", "The `secret` key should NOT be within the `nornir_settings` dictionary")
        # verify_setting(plugin_settings, "nornir_settings.connection_secret_path", "The `connection_secret_path` key should NOT be within the `nornir_settings` dictionary")
        # verify_setting(plugin_settings, "nornir_settings.secret_access_type", "The `secret_access_type` key should NOT be within the `nornir_settings` dictionary")
        super().ready()


config = NautobotPluginNornirConfig  # pylint:disable=invalid-name
