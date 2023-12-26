# Uninstall the App from Nautobot

## Uninstall Guide

Remove the configuration you added in `nautobot_config.py` from `PLUGINS` & `PLUGINS_CONFIG`.

Uninstall the package

```bash
$ pip3 uninstall nautobot-plugin-nornir
```

## Database Cleanup

Not applicable, as the app does not have any models.
