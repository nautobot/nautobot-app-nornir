# Frequently Asked Questions

_What grouping options are available via the ORM inventory?_

There is currently no user/operator defined grouping or inventory. The implementation defines the following groups.

```python
"global",
f"site__{device.site.slug}",
f"role__{device.device_role.slug}",
f"type__{device.device_type.slug}",
f"manufacturer__{device.device_type.manufacturer.slug}",
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

Once again, the wrong indentation will not work. This leads to errors one would not expect.