# Installing the App in Nautobot

## Prerequisites

- The plugin is compatible with Nautobot 1.2.0 and higher.
- Databases supported: PostgreSQL, MySQL

!!! note
    Please check the [dedicated page](compatibility_matrix.md) for a full compatibility matrix and the deprecation policy.

### Access Requirements

N/A

## Install Guide

!!! note
    Plugins can be installed manually or using Python's `pip`. See the [nautobot documentation](https://nautobot.readthedocs.io/en/latest/plugins/#install-the-package) for more details. The pip package name for this plugin is [`nautobot_plugin_nornir`](https://pypi.org/project/nautobot_plugin_nornir/).

The plugin is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install nautobot-plugin-nornir
```

To ensure Nautobot Plugin Nornir is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-plugin-nornir` package:

```no-highlight
# echo nautobot-plugin-nornir >> local_requirements.txt
```

Once installed, the plugin needs to be enabled in your Nautobot configuration. The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

- Append `"nautobot_plugin_nornir"` to the `PLUGINS` list.
- Append the `"nautobot_plugin_nornir"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.

```python
# In your nautobot_config.py
PLUGINS = ["nautobot_plugin_nornir"]

PLUGINS_CONFIG = {
    "nautobot_plugin_nornir": {
        "use_config_context": {"secrets": False, "connection_options": True},
        # Optionally set global connection options.
        "connection_options": {
            "napalm": {
                "extras": {
                    "optional_args": {"global_delay_factor": 1},
                },
            },
            "netmiko": {
                "extras": {
                    "global_delay_factor": 1,
                },
            },
        },
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
}
```

## App Configuration

The plugin behavior can be controlled with the following list of settings. 

| Key                    | Example | Default | Description |
| ---------------------- | ------- | ------- | ----------- |
| nornir_settings        | {"nornir_settings": { "credentials": "cred_path"}} | N/A | The expected configuration paramters that Nornir uses, see Nornir documentation. |
| dispatcher_mapping     | {"newos": "dispatcher.newos"} | None | A dictionary in which the key is a platform slug and the value is the import path of the dispatcher in string format |
| username               | ntc | N/A | The username when leveraging the `CredentialsSettingsVars` credential provider. |
| password               | password123 | N/A | The password when leveraging the `CredentialsSettingsVars` credential provider. |
| secret                 | password123 | N/A | The secret password when leveraging the `CredentialsSettingsVars` credential provider.|
| connection_options     | N/A | {"netmiko": {"extras": {"global_delay_factor": 1}}} | Set Nornir connection options globally to be used with **all** connections.
| use_config_context     | {"secrets": True, "connection_options": True} | {"secrets": False, "connection_options": False} | Whether to pull Secret Access Type, and/or Connection Options from Config Context. |
| connection_secret_path | "my_plugin.newos" |  <see note> | Dotted expression of the dictionary path where a device secret should be stored for a given Nornir Plugin. |
<!-- This is actually not implemented in the source code. Add back after implemented. -->
<!-- | secret_access_type     | "SSH" | "GENERIC" | Type of Secret Access Type to use. Examples. "GENERIC", "CONSOLE", "GNMI", "HTTP", "NETCONF", "REST", "RESTCONF", "SNMP", "SSH"| -->

> Note: The default value for  `connection_secret_path` is "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars", left here to import rendering of the table.

The plugin behavior can be extended further with [config context](https://nautobot.readthedocs.io/en/stable/models/extras/gitrepository/#configuration-contexts) data. The plugin currently implements two options: Nornir connection options, and secrets.  The supported settings are listed below.

| Key                    | Description |
| ---------------------- | ----------- |
| connection_options     | Dictionary representation of a Nornir Plugins connection options. |
| connection_secret_path | Dotted expression of the dictionary path where a device secret should be stored for a given Nornir Plugin. |
| secret_access_type     | Type of Secret Access Type to use. Examples. "GENERIC", "CONSOLE", "GNMI", "HTTP", "NETCONF", "REST", "RESTCONF", "SNMP", "SSH"|

For details on the [credentials](../../user/app_feature_credentials), [inventory](../../user/app_feature_inventory), and [dispatcher](../../user/app_feature_dispatcher) please see their respective documentation.