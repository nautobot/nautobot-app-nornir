"""Credentials class for environment variables."""
import os
from .nautobot_orm import NautobotORMCredentials

USERNAME_ENV_VAR_NAME = "NAPALM_USERNAME"  # nosec
PASSWORD_ENV_VAR_NAME = "NAPALM_PASSWORD"  # nosec
SECRET_ENV_VAR_NAME = "DEVICE_SECRET"  # nosec


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
            params ([dict], optional): Crednetials Parameters
        """
        if not params:
            params = {}

        if not isinstance(params, dict):
            raise TypeError("params must be a dictionnary")

        self.username = os.getenv(params.get("username", USERNAME_ENV_VAR_NAME))
        self.password = os.getenv(params.get("password", PASSWORD_ENV_VAR_NAME))
        self.secret = os.getenv(params.get("secret", SECRET_ENV_VAR_NAME))

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
