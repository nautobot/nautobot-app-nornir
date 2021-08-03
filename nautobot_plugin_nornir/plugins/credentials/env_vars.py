"""Credentials class for environment variables."""
import os
from .nautobot_orm import NautobotORMCredentials

USERNAME_ENV_VAR_NAME = "NAPALM_USERNAME"  # nosec
PASSWORD_ENV_VAR_NAME = "NAPALM_PASSWORD"  # nosec
SECRET_ENV_VAR_NAME = "DEVICE_SECRET"  # nosec
ALT_USERNAME_ENV_VAR_NAME = "NAUTOBOT_NAPALM_USERNAME"  # nosec
ALT_PASSWORD_ENV_VAR_NAME = "NAUTOBOT_NAPALM_PASSWORD"  # nosec
ALT_SECRET_ENV_VAR_NAME = "NAUTOBOT_DEVICE_SECRET"  # nosec


class CredentialsEnvVars(NautobotORMCredentials):
    """Credentials Class designed to work with Nautobot ORM.

    This class is the default class that will return the same login and password
    for all devices based on the values of the environment variables

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

        self.username = params.get("username", os.getenv(USERNAME_ENV_VAR_NAME, os.getenv(ALT_USERNAME_ENV_VAR_NAME)))
        self.password = params.get("password", os.getenv(PASSWORD_ENV_VAR_NAME, os.getenv(ALT_PASSWORD_ENV_VAR_NAME)))
        self.secret = params.get("secret", os.getenv(SECRET_ENV_VAR_NAME, os.getenv(ALT_SECRET_ENV_VAR_NAME)))

        if not self.secret:
            self.secret = self.password

    def get_device_creds(self, device):
        """Return the credentials for a given device.

        Args:
            device (dcim.models.Device): Nautobot device object

        Return:
            username (string):
            password (string):
            secret (string):
        """
        return (self.username, self.password, self.secret)
