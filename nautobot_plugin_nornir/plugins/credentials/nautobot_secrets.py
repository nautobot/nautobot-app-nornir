"""Credentials class designed to work with Nautobot Secrets Functionality."""

from nautobot.extras.choices import SecretsGroupAccessTypeChoices, SecretsGroupSecretTypeChoices
from nautobot.extras.models.secrets import SecretsGroupAssociation

from .nautobot_orm import NautobotORMCredentials


class CredentialsNautobotSecrets(NautobotORMCredentials):
    """Credentials Class designed to work with Nautobot Secrets Functionality."""

    def get_device_creds(self, device):
        """Return the credentials for a given device.

        Args:
            device (dcim.models.Device): Nautobot device object

        Return:
            username (string):
            password (string):
            secret (string):
        """
        if device.secrets_group:
            self.username = device.secrets_group.get_secret_value(
                access_type=SecretsGroupAccessTypeChoices.TYPE_GENERIC,
                secret_type=SecretsGroupSecretTypeChoices.TYPE_USERNAME,
                obj=device,
            )
            self.password = device.secrets_group.get_secret_value(
                access_type=SecretsGroupAccessTypeChoices.TYPE_GENERIC,
                secret_type=SecretsGroupSecretTypeChoices.TYPE_PASSWORD,
                obj=device,
            )
            try:
                self.secret = device.secrets_group.get_secret_value(
                    access_type=SecretsGroupAccessTypeChoices.TYPE_GENERIC,
                    secret_type=SecretsGroupSecretTypeChoices.TYPE_SECRET,
                    obj=device,
                )
            except SecretsGroupAssociation.DoesNotExist:
                self.secret = self.password
            return (self.username, self.password, self.secret)
        else:
            raise ValueError(
                "The credential provider for Nautobot Secrets requires a Secrets Group to be set on a device."
            )
