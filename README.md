# ntc-nautobot-plugin-nornir

A plugin for [Nautobot](https://github.com/nautobot/nautobot), that intends to be a small shim layer between
[nornir_nautobot](https://github.com/nautobot/nornir-nautobot) and other plugins. The primary abilities that the plugin provides is a native Nornir
ORM based inventory and a credential manager.

# Installation

The plugin is available as a Python package in pypi and can be installed with pip
```shell
pip install nautobot-plugin-nornir
```

> The plugin is compatible with Nautobot 1.0.0 and higher
 
Once installed, the plugin needs to be enabled in your `configuration.py`
```python
# In your configuration.py
PLUGINS = ["nautobot_nornir"]

PLUGINS_CONFIG = {
  "nautobot_nornir": {
    "nornir_settings": {
      "credentials": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
      "runner": {
        "plugin": "threaded",
        "options": {
            "num_workers": 20,
        },
      },
    },
  }
```

The plugin behavior can be controlled with the following list of settings

# Inventory

The Nautobot ORM inventory is rather static in nature at this point. The user has the ability to define the `default` data. The native capabilites
include. 

* Providing an object called `orm` that is a Nautobot `Device` object instance.
* Provide keys for hostname, name, id, type, stie, role, config_context, obj, and custom_field_data.
* Provide grouping for global, site, role, type, and manufacturer based on their slug.
* Provide credentials for napalm and netmiko.
* Link to the credential class as defined.

# Credentials

There is a `NautobotORMCredentials` that describes what the object the Nornir inventory is looking for. 

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

Any custom credential class should inherit from this model and provide get_device_creds and/or get_group_creds methods. Currently, only the
get_device_creds is used. Building your own custom credential class allows users to control their own credential destiny. As an example, a user could
integrate with their own vaulting system, and obtain credentials that way. To provide a simple but concrete example.

```python
class CustomNautobotORMCredentials(NautobotORMCredentials):

    def get_device_creds(self, device):
        if device.startswith('csr'):
            return ("cisco", "cisco123", None)
        return ("net-admin", "ops123", None)
```

You would have to set your `nornir_settings['credentials']` path to your custom class, such as `local_plugin.creds.CustomNautobotORMCredentials`.

Out of the box, users have access to the `nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars` class. This simply leverages the environment variables `NAPALM_USERNAME`, `NAPALM_PASSWORD`, and `DEVICE_SECRET`. 

# Contributing

Pull requests are welcomed and automatically built and tested against multiple version of Python and multiple version of Nautobot through TravisCI.

The project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.

The project is following Network to Code software development guideline and is leveraging:
- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.
- Django unit test to ensure the plugin is working properly.

# CLI Helper Commands

The project is coming with a CLI helper based on [invoke](http://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories `dev environment`, `utility` and `testing`. 

Each command can be executed with `invoke <command>`. All commands support the arguments `--nautobot-ver` and `--python-ver` if you want to manually define the version of Python and Nautobot to use. Each command also has its own help `invoke <command> --help`

## Local dev environment
```
  build            Build all docker images.
  debug            Start Nautobot and its dependencies in debug mode.
  destroy          Destroy all containers and volumes.
  restart          Restart Nautobot and its dependencies.
  start            Start Nautobot and its dependencies in detached mode.
  stop             Stop Nautobot and its dependencies.
```

## Utility 
```
  cli              Launch a bash shell inside the running Nautobot container.
  create-user      Create a new user in django (default: admin), will prompt for password.
  makemigrations   Run Make Migration in Django.
  nbshell          Launch a nbshell session.
```
## Testing 

```
  bandit           Run bandit to validate basic static code security analysis.
  black            Run black to check that Python files adhere to its style standards.
  flake8           This will run flake8 for the specified name and Python version.
  pydocstyle       Run pydocstyle to validate docstring formatting adheres to NTC defined standards.
  pylint           Run pylint code analysis.
  tests            Run all tests for this plugin.
  unittest         Run Django unit tests for the plugin.
```

# Questions

For any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).
Sign up [here](http://slack.networktocode.com/)
