"""Credentials class for setting credentials."""
# pylint: disable=duplicate-code
from nautobot_plugin_nornir.constants import PLUGIN_CFG
from nautobot_plugin_nornir.plugins.credentials.nautobot_orm import MixinNautobotORMCredentials


class CredentialsSettingsVars(MixinNautobotORMCredentials):
    """Credentials Class designed to work with Nautobot ORM that comes from settings.

    This class will return the same login and password for all devices based on the values
    within your settings.
    """

    def __init__(self, params=None):
        """Initialize Credentials Class designed to work with Nautobot ORM.

        Args:
            params ([dict], optional): Credentials Parameters
        """
        if not params:
            params = {}

        if not isinstance(params, dict):
            raise TypeError("params must be a dictionary")

        self.username = PLUGIN_CFG.get("username")
        self.password = PLUGIN_CFG.get("password")
        self.secret = PLUGIN_CFG.get("secret")

        if not self.secret:
            self.secret = self.password
