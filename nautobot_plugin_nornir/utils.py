"""Utilities for plugin."""


def get_dispatcher():
    """Helper method to load the dispatcher from nautobot nornir or config if defined."""
    if PLUGIN_CFG.get("dispatcher_mapping"):
        return PLUGIN_CFG["dispatcher_mapping"]
    return _DEFAULT_DRIVERS_MAPPING
