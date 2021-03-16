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

There is already a repo called `nornir-nautbot` and in order to avoid the confusion of both a `nornir-nautobot` and `nautobot-nornir`, the word 
`plugin` was left in the name. While it is clear that this will still remain confusing, it was deemed the lesser of two evils.