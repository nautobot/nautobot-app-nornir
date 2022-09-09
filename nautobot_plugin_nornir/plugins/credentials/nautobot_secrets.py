"""Credentials class designed to work with Nautobot Secrets Functionality."""
# pylint: disable=attribute-defined-outside-init

from nautobot.extras.choices import SecretsGroupAccessTypeChoices, SecretsGroupSecretTypeChoices
from nautobot.extras.models.secrets import SecretsGroupAssociation
from nautobot_plugin_nornir.constants import PLUGIN_CFG

from .nautobot_orm import MixinNautobotORMCredentials


def _get_secret_value(secret_type, device_obj):
    """Get value for a secret based on secret type and device.

    Args:
        secret_type (SecretsGroupSecretTypeChoices): Type of secret to check.
        device_obj (dcim.models.Device): Nautobot device object.

    Returns:
        str: Secret value.
    """
    if PLUGIN_CFG.get("use_config_context", {}).get("secrets"):
        access_type_str = device_obj.get_config_context()["nautobot_plugin_nornir"]["secret_access_type"].upper()
        access_type = getattr(SecretsGroupAccessTypeChoices, f"TYPE_{access_type_str}")
    else:
        access_type = SecretsGroupAccessTypeChoices.TYPE_GENERIC
    try:
        value = device_obj.secrets_group.get_secret_value(
            access_type=access_type,
            secret_type=secret_type,
            obj=device_obj,
        )
    except SecretsGroupAssociation.DoesNotExist:
        value = None
    return value


class CredentialsNautobotSecrets(MixinNautobotORMCredentials):
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
            self.username = _get_secret_value(
                secret_type=SecretsGroupSecretTypeChoices.TYPE_USERNAME, device_obj=device
            )
            self.password = _get_secret_value(
                secret_type=SecretsGroupSecretTypeChoices.TYPE_PASSWORD, device_obj=device
            )
            self.secret = _get_secret_value(secret_type=SecretsGroupSecretTypeChoices.TYPE_SECRET, device_obj=device)
            if not self.secret:
                self.secret = self.password
            return (self.username, self.password, self.secret)
        return (None, None, None)
