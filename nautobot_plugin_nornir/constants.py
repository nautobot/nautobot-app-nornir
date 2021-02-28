"""Constants for plugin."""
from django.conf import settings
from nornir_nautobot.plugins.tasks.dispatcher import _DEFAULT_DRIVERS_MAPPING

_NORNIR_SETTINGS = {
    "inventory": "nautobot_plugin_nornir.plugins.inventory.nautobot_orm.NautobotORMInventory",
    "credentials": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
    "nornir.core": {"num_workers": 20},
}

NORNIR_SETTINGS = settings.PLUGINS_CONFIG["nautobot_plugin_nornir"].get("nornir_settings", _NORNIR_SETTINGS)


DEFAULT_DRIVERS_MAPPING = settings.PLUGINS_CONFIG["nautobot_plugin_nornir"].get(
    "DEFAULT_DRIVERS_MAPPING", _DEFAULT_DRIVERS_MAPPING
)
