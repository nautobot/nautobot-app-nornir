"""Utilities for plugin."""

from nornir_nautobot.plugins.tasks.dispatcher import _DEFAULT_DRIVERS_MAPPING
from nautobot_plugin_nornir.constants import PLUGIN_CFG


def get_dispatcher():
    """Helper method to load the dispatcher from nautobot nornir or config if defined."""
    if PLUGIN_CFG.get("dispatcher_mapping"):
        return {**_DEFAULT_DRIVERS_MAPPING, **PLUGIN_CFG["dispatcher_mapping"]}
    return _DEFAULT_DRIVERS_MAPPING
