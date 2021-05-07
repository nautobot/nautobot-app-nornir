"""Credentials class for setting credentials."""
from django.conf import settings
from .nautobot_orm import MixinNautobotORMCredentials

PLUGIN_SETTINGS = settings.PLUGINS_CONFIG["nautobot_plugin_nornir"]


class CredentialsSettingsVars(MixinNautobotORMCredentials):
    """Credentials Class designed to work with Nautobot ORM that comes from settings.

    This class will return the same login and password for all devices based on the values
    within your settings.

    Args:
        NautobotORMCredentials ([type]): [description]
    """

    def __init__(self, params=None):
        """Initialize Credentials Class designed to work with Nautobot ORM.

        Args:
            params ([dict], optional): Credentials Parameters
        """
        if not params:
            params = {}

        if not isinstance(params, dict):
            raise TypeError("params must be a dictionnary")

        self.username = PLUGIN_SETTINGS.get("username")
        self.password = PLUGIN_SETTINGS.get("password")
        self.secret = PLUGIN_SETTINGS.get("secret")

        if not self.secret:
            self.secret = self.password
