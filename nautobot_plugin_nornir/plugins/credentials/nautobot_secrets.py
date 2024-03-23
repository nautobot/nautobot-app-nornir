"""
Credentials class designed to work with Nautobot Secrets Functionality.

Nautobot Secrets Feature:

secret-group:
    secret: username <supports templating>
        - Because of templating can be `n` number of actual values.
    secret: password <supports templating>
        - Because of templating can be `n` number of actual values.
    secret: secret <supports templating>
        - Because of templating can be `n` number of actual values.

Caching Solution:

creds_cache = {
        "hashed key": "value"
    }

    - "hashed key" is the rendred.parameter which is post template rendered secret key.
    - "value" is the literal secrets value.
"""
# pylint: disable=attribute-defined-outside-init
import json

from nautobot.extras.choices import SecretsGroupAccessTypeChoices, SecretsGroupSecretTypeChoices
from nautobot_plugin_nornir.constants import PLUGIN_CFG

from .nautobot_orm import MixinNautobotORMCredentials


def _get_access_type_value(device_obj):
    """Get value for access_type.

    Args:
        device_obj (dcim.models.Device): Nautobot device object.

    Returns:
        SecretsGroupAccessTypeChoices: Choice
    """
    if PLUGIN_CFG.get("use_config_context", {}).get("secrets"):
        access_type_str = device_obj.get_config_context()["nautobot_plugin_nornir"]["secret_access_type"].upper()
        access_type = getattr(SecretsGroupAccessTypeChoices, f"TYPE_{access_type_str}")
    else:
        access_type = SecretsGroupAccessTypeChoices.TYPE_GENERIC
    return access_type


class CredentialsNautobotSecrets(MixinNautobotORMCredentials):
    """Credentials Class designed to work with Nautobot Secrets Functionality."""

    def __init__(self):
        """Initialize class with empty creds_cache."""
        self._creds_cache = {}

    def _get_or_cache_secret_key(self, device, sec):
        """Check if secret_key is already in cache, if not call setter method to add the entry.

        Args:
            device (dcim.Device): Nautobot Device object.
            sec (extra.SecretGroup): Nautobot SecretGroup objects.

        Returns:
            str: A rendered secgret group hashed into a single hashed id to use as a unique key.

        Examples:
            >>> # Example of a Environment Variable rendered.
            >>> device = Device.objects.first()
            >>> sec = device.secrets_group.secrets.last()
            >>> sec
            >>> <Secret: router-u>
            >>> sec.rendered_parameters(obj=device)
            >>> {'variable': 'DEVICE_ROUTER_USERNAME'}
            >>> str(hash(json.dumps(sec.rendered_parameters(obj=device), sort_keys=True)))
            >>> '588946476233721127'
            >>>
            >>> # Example using hashicorp vault secrets provider backend.
            >>> sec = device.secrets_group.secrets.first()
            >>> sec.rendered_parameters(obj=device)
            >>>
            {'key': 'username',
            'path': 'goldenconfig',
            'kv_version': 'v2',
            'mount_point': 'secret'}
            >>> str(hash(json.dumps(sec.rendered_parameters(obj=device), sort_keys=True)))
            >>> '-3888945057722956687'
        """
        # hash the rendered secrets params.
        secret_key_hash = str(hash(json.dumps(sec.rendered_parameters(obj=device), sort_keys=True)))
        if not self.creds_cache.get(secret_key_hash):
            # If hashed value isn't in the cache, then call actual get_value to pull secret value itself and
            # Update the cache property.
            self.creds_cache = {secret_key_hash: sec.get_value(obj=device)}
        return secret_key_hash

    @property
    def creds_cache(self):
        """
        Getter for in memory creds cache. This is useds to temporarily cache secrets-group creds to avoid re-querying secrets providers over and over per device if the same secret-group was used.

        Example:
            {"123435": 'supersecret'}
        """
        return self._creds_cache

    @creds_cache.setter
    def creds_cache(self, new_cred):
        """
        Setter for creds_cache.

        Args:
            new_cred (dict): new secret group key and values.
        """
        self._creds_cache.update(new_cred)

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
            self.secret = None
            for sec in device.secrets_group.secrets.all():
                secret_value = self.creds_cache.get(self._get_or_cache_secret_key(device, sec))
                current_secret_type = getattr(
                    SecretsGroupSecretTypeChoices, f"TYPE_{sec.secrets_group_associations.first().secret_type.upper()}"
                )
                current_access_type = getattr(
                    SecretsGroupAccessTypeChoices, f"TYPE_{sec.secrets_group_associations.first().access_type.upper()}"
                )
                configured_access_type = _get_access_type_value(device)
                if (
                    current_secret_type == SecretsGroupSecretTypeChoices.TYPE_USERNAME
                    and configured_access_type == current_access_type
                ):
                    self.username = secret_value
                if (
                    current_secret_type == SecretsGroupSecretTypeChoices.TYPE_PASSWORD
                    and configured_access_type == current_access_type
                ):
                    self.password = secret_value
                if (
                    current_secret_type == SecretsGroupSecretTypeChoices.TYPE_SECRET
                    and configured_access_type == current_access_type
                ):
                    self.secret = secret_value
            if not self.secret:
                self.secret = self.password
            return (self.username, self.password, self.secret)
        return (None, None, None)
