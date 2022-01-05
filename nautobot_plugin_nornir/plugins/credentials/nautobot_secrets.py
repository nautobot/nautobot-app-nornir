"""Credentials class designed to work with Nautobot Secrets Functionality."""

from nautobot.extras.models.secrets import SecretsGroupAssociation

from .nautobot_orm import MixinNautobotORMCredentials


class NautobotSecretCredentials(MixinNautobotORMCredentials):
    """Abstract Credentials Class designed to work with Nautobot Secrets Functionality."""

    def get_device_creds(self, device):  # pylint: disable=unused-argument, no-self-use
        """Return the credentials for a given device.

        Args:
            device (dcim.models.Device): Nautobot device object

        Return:
            username (string):
            password (string):
            secret (string):
        """
        self.username = device.secrets_group.get_secret_value("Generic", "username", obj=device)
        self.password = device.secrets_group.get_secret_value("Generic", "password", obj=device)
        try:
            self.secret = device.secrets_group.get_secret_value("Generic", "secret", obj=device)
        except SecretsGroupAssociation.DoesNotExist:
            self.secret = self.password
        return (self.username, self.password, self.secret)
