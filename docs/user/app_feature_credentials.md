# Credentials

The credentials that will be used by Nornir to connect to the device is based on the `credential` parameter. Credentials come in both provided and also allows you to create your own credential provider. 

> For any of these classes, if a "secret" value is not defined, the "password" will also be used as the "secret" value.

## Supported Credential Types

Out of the box, there are three credential plugins.

* Environment Variables - Leveraging pre-defined environment variables for your credentials.
* Setting Variables - Leveraging the `nautobot_config.py` for your credentials
* Nautobot Secrets - Leveraging the [Nautobot Secrets Group](https://nautobot.readthedocs.io/en/latest/core-functionality/secrets/#secrets-groups) feature for your credentials.

### Environment Variables

**Dotted string path:** `nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars`

Leverages the environment variables `NAPALM_USERNAME`, `NAPALM_PASSWORD`, and `DEVICE_SECRET`.

The environment variable must be accessible on the web service. This often means simply exporting the environment variable on the cli will not suffice, but instead requiring users to update the `nautobot.service` and `nautobot-worker.service` files. Keep in mind this will ultimately depend **on your own setup** and is simply based on standard Linux environment variables. Environment variables are distinctively not nautobot configuration parameters (in `nautobot_config.py`), if that does not makes sense, expect to see authentication issues. If you wish to simply put the passwords in `nautobot_config.py`, see Settings Variables section.


An example of what the `nautobot.service` and `nautobot-worker.service` would look like.

```
[Service]
Environment="NAPALM_USERNAME=ntc"
Environment="NAPALM_PASSWORD=password123"
Environment="DEVICE_SECRET=password123"
```

```python
PLUGINS_CONFIG = {
    "nautobot_plugin_nornir": {
        "nornir_settings": {
           "credentials": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars"
        },
    }
}
```

### Setting Variables

**Dotted string path:** `nautobot_plugin_nornir.plugins.credentials.settings_vars.CredentialsSettingsVars`

This leverages the username, password, secret that is specified in the plugin configuration.

```python
PLUGINS_CONFIG = {
    "nautobot_plugin_nornir": {
        "nornir_settings": {
            "credentials": "nautobot_plugin_nornir.plugins.credentials.settings_vars.CredentialsSettingsVars",
        },
        "username": "ntc",
        "password": "password123",
        "secret": "password123",
    }
}
```

### Nautobot Secrets

**Dotted string path:** `nautobot_plugin_nornir.plugins.credentials.nautobot_secrets.CredentialsNautobotSecrets`

Leverages the [Nautobot Secrets Group](https://nautobot.readthedocs.io/en/latest/core-functionality/secrets/#secrets-groups) core functionality.

**The default assumes Secrets Group contain secrets with "Access Type" of `Generic`** and expects these secrets to have "Secret Type" of `username`, `password`, and optionally `secret`. The "Access Type" is configurable via the plugin configuration parameter `use_config_context`, which if enabled changes the plugin functionality to pull `device_obj.get_config_context()['nautobot_plugin_nornir']['secret_access_type']` from each devices config_context. Which is the config context dictionary `nautobot_plugin_nornir` and the subkey of `secret_access_type`.

Enabling the use of Config Context:

```python
PLUGINS_CONFIG = {
    "nautobot_plugin_nornir": {
        "use_config_context": {"secrets": True}, 
        "nornir_settings": {
            "credentials": "nautobot_plugin_nornir.plugins.credentials.nautobot_secrets.CredentialsNautobotSecrets",
        }
    }
}
```

Local Device Config Context:
```json
{
    "nautobot_plugin_nornir": {
        "secret_access_type": "SSH"
    }
}
```
  
Device Type Config Context:

```yaml
---
_metadata:
  name: spine
  weight: 1000
  description: Group Definitions for device type SPINE
  is_active: true
  device-roles:
    - slug: spine
nautobot_plugin_nornir:
  secret_access_type: SSH
```

By default the device secret connection option path will be set for connections using: Napalm, Netmiko, and Scrapli.  If an additional path needs to be registered it can be done by setting it inside the config context data.  See below for an example.

```yaml
---
_metadata:
  name: spine
  weight: 1000
  description: Group Definitions for device type SPINE
  is_active: true
  device-roles:
    - slug: spine
nautobot_plugin_nornir:
  pluginx: 
    connection_secret_path: "pluginx.extras.secret"
```

## Custom Credential Manager

There is a `NautobotORMCredentials` class that describes what methods a Nautobot Nornir credential class should have.

```python
class NautobotORMCredentials:
    """Abstract Credentials Class designed to work with Nautobot ORM."""

    def get_device_creds(self, device):
        """Return the credentials for a given device.

        Args:
            device (dcim.models.Device): Nautobot device object

        Return:
            username (string):
            password (string):
            secret (string):
        """
        return (None, None, None)

    def get_group_creds(self, group_name):
        """Return the credentials for a given group.

        Args:
            group_name (string): Name of the group

        Return:
            string: username
            string: password
            string: secret
        """
        return (None, None, None)
```

Any custom credential class should inherit from this class and provide get_device_creds and/or get_group_creds methods. Currently, only the get_device_creds is used. Building your own custom credential class allows users to control their own credential destiny. As an example, a user could integrate with their own vaulting system, and obtain credentials that way. To provide a simple but concrete example.

```python
class CustomNautobotORMCredentials(NautobotORMCredentials):

    def get_device_creds(self, device):
        if device.startswith('csr'):
            return ("cisco", "cisco123", None)
        return ("net-admin", "ops123", None)
```

You would have to set your `nornir_settings['credentials']` path to your custom class, such as `local_plugin.creds.CustomNautobotORMCredentials`:

```python
PLUGINS_CONFIG = {
    "nautobot_plugin_nornir": {
        "nornir_settings": {
            "credentials": "local_plugin.creds.CustomNautobotORMCredentials",
        }
    }
}
```
