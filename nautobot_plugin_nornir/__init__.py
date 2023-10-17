"""Plugin declaration for nautobot_plugin_nornir."""
# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

__version__ = metadata.version(__name__)

from nautobot.extras.plugins import NautobotAppConfig


class NautobotPluginNornirConfig(NautobotAppConfig):
    """Plugin configuration for the nautobot_plugin_nornir plugin."""

    name = "nautobot_plugin_nornir"
    verbose_name = "Nautobot Nornir Plugin"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot Nornir Plugin."
    base_url = "plugin-nornir"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}


config = NautobotPluginNornirConfig  # pylint:disable=invalid-name
