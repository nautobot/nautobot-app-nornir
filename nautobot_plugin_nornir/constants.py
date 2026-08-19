"""Constants for plugin."""

from django.conf import settings

from nautobot_plugin_nornir.defaults import merge_nornir_settings

PLUGIN_CFG = settings.PLUGINS_CONFIG.get("nautobot_plugin_nornir", {})
NORNIR_SETTINGS = merge_nornir_settings(PLUGIN_CFG.get("nornir_settings"))

CONNECTION_SECRETS_PATHS = {
    "netmiko": "netmiko.extras.secret",
    "napalm": "napalm.extras.optional_args.secret",
    "pyntc": "pyntc.extras.secret",
    "scrapli": "scrapli.extras.auth_secondary",
}
DRIVERS = ["napalm", "netmiko", "scrapli", "pyntc"]

ALLOWED_LOCATION_TYPES = PLUGIN_CFG.get("allowed_location_types", [])
DENIED_LOCATION_TYPES = PLUGIN_CFG.get("denied_location_types", [])
