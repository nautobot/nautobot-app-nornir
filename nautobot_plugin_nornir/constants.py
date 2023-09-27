"""Constants for plugin."""
from django.conf import settings

_NORNIR_SETTINGS = {
    "inventory": "nautobot_plugin_nornir.plugins.inventory.nautobot_orm.NautobotORMInventory",
    "credentials": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
    "runner": {"options": {"num_workers": 20}},
}

PLUGIN_CFG = settings.PLUGINS_CONFIG.get("nautobot_plugin_nornir", {})
NORNIR_SETTINGS = PLUGIN_CFG.get("nornir_settings", _NORNIR_SETTINGS)

CONNECTION_SECRETS_PATHS = {
    "netmiko": "netmiko.extras.secret",
    "napalm": "napalm.extras.optional_args.secret",
    "pyntc": "pyntc.extras.secret",
    "scrapli": "scrapli.extras.auth_secondary",
}
DRIVERS = ["napalm", "netmiko", "scrapli", "pyntc"]

ALLOWED_LOCATION_TYPES = PLUGIN_CFG.get("allowed_location_types", [])
DENIED_LOCATION_TYPES = PLUGIN_CFG.get("denied_location_types", [])
