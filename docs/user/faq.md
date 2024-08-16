# Frequently Asked Questions

_What grouping options are available via the ORM inventory?_

There is currently no user/operator defined grouping or inventory. The implementation defines the following groups.

```python
"global",
f"location__{device.location.name}",
f"role__{device.device_role.name}",
f"type__{device.device_type.model}",
f"manufacturer__{device.device_type.manufacturer.name}",
```

_Why is the plugin installed as nautobot_plugin_nornir and not nautobot_nornir?_

There is already a repository called `nornir-nautbot` and in order to avoid the confusion of both a `nornir-nautobot` and `nautobot-nornir`, the word `plugin` was left in the name. While it is clear that this will still remain confusing, it was deemed the lesser of two evils.

_What is the difference between `nautobot_plugin_nornir` and `nornir_settings`? Why not just flatten?_

Nautobot provides each plugin a set of settings and Nornir has it's own settings. In order to "pass on" the Nornir settings as required, this leads to the nesting as seen. 

This does often lead to some confusion. Let's take a few examples. 

Expected 1:
```python
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
    },
}
```

Configured 1:
```python
PLUGINS_CONFIG = {
    "nautobot_plugin_nornir": {
        "credentials": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
        "nornir_settings": {
            "runner": {
                "plugin": "threaded",
                "options": {
                    "num_workers": 20,
                },
            },
        },
    },
}
```
As you can see the `credentials` was not set underneath the correct key. 

Expected 2:
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

Configured 2:
```python
PLUGINS_CONFIG = {
    "nautobot_plugin_nornir": {
        "nornir_settings": {
            "credentials": "nautobot_plugin_nornir.plugins.credentials.settings_vars.CredentialsSettingsVars",
            "username": "ntc",
            "password": "password123",
            "secret": "password123",
        },
    }
}
```

_How can I set the TCP Port that is used in the connectivity check?_

Nornir-Nautobot provides the ability to check the connectivity first via TCP, this port is set per OS driver and is generally port 22. Howeever, you can adjust this yourself, and is partially described in the [nornir-nautobot docs](https://docs.nautobot.com/projects/nornir-nautobot/en/latest/task/task/#check-connectivity-configuration).

The docs indicate that there is 3 choices for check connectivity will send attempt to tcp ping the port based on the following order or precedence from most to least preferred.

- If there is a [Custom Field](https://docs.nautobot.com/projects/core/en/stable/user-guide/feature-guides/custom-fields/) called `tcp_port` that is an integer, prefer that.
- Next check if there is a [Config Context](https://docs.nautobot.com/projects/core/en/stable/user-guide/core-data-model/extras/configcontext/) key called `tcp_port` and if it is a valid integer, prefer that.
- Finally, there is default for each driver, which is generally port 22 which it will be defaulted to.
