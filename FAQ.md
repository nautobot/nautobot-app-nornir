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