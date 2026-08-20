"""Default settings for the nautobot_plugin_nornir App.

This module must not import Django or Nautobot. Nautobot imports the App config in
`__init__.py` before Django settings are configured, so the defaults have to be available
without a settings module.
"""

from copy import deepcopy

DEFAULT_NORNIR_SETTINGS = {
    "inventory": "nautobot_plugin_nornir.plugins.inventory.nautobot_orm.NautobotORMInventory",
    "credentials": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
    "runner": {
        "plugin": "threaded",
        "options": {"num_workers": 20},
    },
}


def merge_nornir_settings(user_settings):
    """Merge user-supplied `nornir_settings` over `DEFAULT_NORNIR_SETTINGS`.

    Nautobot merges `default_settings` at the top level only, so a `nornir_settings` dictionary
    that sets a single key would otherwise drop the remaining defaults. The merge is one level
    deep, which keeps `runner` a single unit, matching how Nornir consumes it.

    Args:
        user_settings (dict): The `nornir_settings` dictionary from `PLUGINS_CONFIG`, or `None`.

    Returns:
        dict: A new dictionary. Mutating it never affects `DEFAULT_NORNIR_SETTINGS`.
    """
    return deepcopy({**DEFAULT_NORNIR_SETTINGS, **(user_settings or {})})
