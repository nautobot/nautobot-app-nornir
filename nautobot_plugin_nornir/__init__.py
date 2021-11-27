"""Plugin declaration for nautobot_plugin_nornir."""

__version__ = "0.9.7"

from nautobot.extras.plugins import PluginConfig


class NornirConfig(PluginConfig):
    """Plugin configuration for nautobot_plugin_nornir."""

    name = "nautobot_plugin_nornir"
    verbose_name = "Nautobot Plugin for Nornir"
    version = __version__
    author = "Network to Code, LLC"
    description = "A plugin/library for using Nornir within Nautobot."
    base_url = "plugin-nornir"
    required_settings = []
    # min_version = "0"
    # max_version = "100"
    default_settings = {}
    caching_config = {}


config = NornirConfig  # pylint:disable=invalid-name
