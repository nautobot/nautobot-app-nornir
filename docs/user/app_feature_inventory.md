
# Inventory

The Nautobot ORM inventory is rather static in nature at this point. The user has the ability to define the `default` data. The native capabilities include.

* Providing an object called within the `obj` key that is a Nautobot `Device` object instance.
* Provide additional keys for hostname, name, id, type, site, role, config_context, and custom_field_data.
* Provide grouping for global, site, role, type, and manufacturer based on their slug (more details below).
* Provide credentials for NAPALM, Netmiko, and Scrapli.
* Link to the credential class as defined by the `nornir_settings['settings']` definition.

Enabling the use of Config Context:

```python
PLUGINS_CONFIG = {
    "nautobot_plugin_nornir": {
        "use_config_context": {
            "connection_options": True
        },
    }
}
```

Local Device Config Context:

```python
{
    "nautobot_plugin_nornir": {
        "connection_options": {
            "napalm": {
                "extras": {
                    "optional_args": {
                        "global_delay_factor": 5
                    }
                }
            }
        }
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
  connection_options:
    napalm:
    extras:
        optional_args:
        global_delay_factor: 5
```

## Inventory Groupings

The inventory provides natural groupings of the following.

* "global"
* "site__{device.site.slug}"
* "role__{device.device_role.slug}"
* "type__{device.device_type.slug}"
* "manufacturer__{device.device_type.manufacturer.slug}"

As an example, if you had manufacturer of `cisco` and `arista`, there will automatically be groups call `manufacturer__cisco` and `manufacturer__arista`.

## Using the Inventory

The inventory provides a series of parameters that you can use, similar to any Nornir inventory. The specific parameters provided are:

```python
queryset: QuerySet = None
filters: Dict = None
credentials_class: str = "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars"
credentials_params: Dict = None
params: Dict = None
defaults: Dict = None
```

The most important part about the inventory is providing a valid `queryset`. This defines what is in scope for your environment. Ideally, the code that interacts with the inventory (via jobs, a plugin, or other custom code) would take some parameters to filter the queryset. In the below illustrative example we simply use the full inventory:

```python
from nautobot.dcim.models import Device

from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister

from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory

InventoryPluginRegister.register("nautobot-inventory", NautobotORMInventory)

qs = Device.objects.all()
data = {"company": "acme"}

nr = InitNornir(
    runner={"options": {"num_workers": 20}},
    logging={"enabled": False},
    inventory={
        "plugin": "nautobot-inventory",
        "options": {
            "credentials_class": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
            "params": {"use_fqdn": True, "fqdn": "acme.com"},
            "queryset": qs,
            "defaults": data,
        },
    },
)

print(nr)
```

To illustrate this further, included is an example in which we filter the queryset further. This pattern while simple can be used to provide query capabilities within a specific Nornir play vs another one.

```python
from nautobot.dcim.models import Device
from nautobot.dcim.filters import DeviceFilterSet

from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister

from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory

InventoryPluginRegister.register("nautobot-inventory", NautobotORMInventory)

def get_qs(site=None):
    query = {}
    if site:
        query["site__slug"] = site
    base_qs = Device.objects.all()
    return DeviceFilterSet(data=query, queryset=base_qs).qs

qs = get_qs("acme")
data = {"company": "acme"}

nr = InitNornir(
    runner={"options": {"num_workers": 20}},
    logging={"enabled": False},
    inventory={
        "plugin": "nautobot-inventory",
        "options": {
            "credentials_class": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
            "params": {"use_fqdn": True, "fqdn": "acme.com"},
            "queryset": qs,
            "defaults": data,
        },
    },
)

print(nr)
```
