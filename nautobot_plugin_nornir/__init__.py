"""App declaration for nautobot_plugin_nornir."""

# Metadata is inherited from Nautobot. If not including Nautobot in the environment, this should be added
from importlib import metadata

from nautobot.apps import NautobotAppConfig

__version__ = metadata.version(__name__)


class NautobotPluginNornirConfig(NautobotAppConfig):
    """App configuration for the nautobot_plugin_nornir app."""

    name = "nautobot_plugin_nornir"
    verbose_name = "Nautobot Nornir Plugin"
    version = __version__
    author = "Network to Code, LLC"
    description = "Nautobot App that provides a shim layer to simplify using Nornir within other Nautobot Apps and Nautobot Jobs."
    base_url = "plugin-nornir"
    required_settings = []
    min_version = "2.0.0"
    max_version = "2.9999"
    default_settings = {}
    caching_config = {}
    docs_view_name = "plugins:nautobot_plugin_nornir:docs"


config = NautobotPluginNornirConfig  # pylint:disable=invalid-name
