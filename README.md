# ntc-nautobot-plugin-nornir

A plugin for [Nautobot](https://github.com/nautobot/nautobot), that intends to be a small shim layer between
[nornir-nautobot](https://github.com/nautobot/nornir-nautobot) and other plugins. The primary abilities that the plugin provides is a native Nornir
ORM based inventory and a credential manager.

![Architecture Overview](./docs/img/architecture-overview.png)

As of the writing of this readme, the only plugin leveraging this plugin is the [golden-config](https://github.com/nautobot/nautobot-plugin-golden-config). However, future plugins are planned, such as the "network importer".

That being said, there is currently little reason to install this plugin by itself, without an enabler, which can be seen represented as the white
rectangles inside the yellow rectangle in the diagram above. An enabler could be a Plugin, Job, or another piece of code like a Chatops command.

# Installation

If using the installation pattern from the Nautobot Documentation, you will need sudo to the `nautobot` user before installing so that you install the package into the Nautobot virtual environment.

```no-highlight
sudo -iu nautobot
```

The plugin is available as a Python package in PyPI and can be installed with `pip3`.

```no-highlight
$ pip3 install nautobot-plugin-nornir
```

To ensure the plugin is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (or append if it already exists) in the [`NAUTOBOT_ROOT`](https://nautobot.readthedocs.io/en/latest/configuration/optional-settings/#nautobot_root) directory and list the `nautobot-plugin-nornir` package:

```no-highlight
$ echo nautobot-plugin-nornir >> $NAUTOBOT_ROOT/local_requirements.txt
```

> The plugin is compatible with Nautobot 1.0.0 and higher
 
Once installed, the plugin needs to be enabled in your `nautobot_config.py`

```python
# In your nautobot_config.py
PLUGINS = ["nautobot_plugin_nornir"]

PLUGINS_CONFIG = {
  "nautobot_plugin_nornir": {
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

Alternatively you can use the `CredentialsSettingsVars` class to set the username and password via settings.

```python
PLUGINS_CONFIG = {
  "nautobot_plugin_nornir": {
    "nornir_settings": {
      "credentials": "nautobot_plugin_nornir.plugins.credentials.settings_vars.CredentialsSettingsVars",
      "runner": {
        "plugin": "threaded",
        "options": {
            "num_workers": 20,
        },
      },
    },
    "username": "ntc",
    "password": "password123",
    "secret": "password123",
  }
}
```

Finally, as root, restart Nautobot and the Nautobot worker.

```no-highlight
$ sudo systemctl restart nautobot nautobot-worker
```
# Inventory

The Nautobot ORM inventory is rather static in nature at this point. The user has the ability to define the `default` data. The native capabilites
include. 

* Providing an object called within the `obj` key that is a Nautobot `Device` object instance.
* Provide additional keys for hostname, name, id, type, site, role, config_context, and custom_field_data.
* Provide grouping for global, site, role, type, and manufacturer based on their slug.
* Provide credentials for NAPALM and Netmiko.
* Link to the credential class as defined by the `nornir_settings['settings']` definition.

# Credentials

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

Out of the box, users have access to the `nautobot_plugin_nornir.plugins.credentials.settings_vars.CredentialsSettingsVars` and 
`nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars` class. This `CredentialsEnvVars` class simply leverages the 
environment variables `NAPALM_USERNAME`, `NAPALM_PASSWORD`, and `DEVICE_SECRET`.

The environment variable must be accessible on the web service. This often means simply exporting the environment variable will not 
suffice, but instead requiring users to update the `nautobot.service` file, however this will ultimately depend on your own setup.

```
[Service]
Environment="NAPALM_USERNAME=ntc"
Environment="NAPALM_PASSWORD=password123"
Environment="DEVICE_SECRET=password123"
```

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
