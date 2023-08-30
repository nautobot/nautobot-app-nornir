# Dispatcher

[Nornir Nautobot](https://github.com/nautobot/nornir-nautobot) provides a series of tasks via a dispatcher. This provides sane defaults for how to use Nornir. Providing tasks like `get_config`, `check_connectivity`, and `compliance_config` for a variety of vendors. That being said, there are many reasons in which the default may not be beneficial to you.

* The default dispatcher does not support your vendor
* The default dispatcher uses a connectivity model (e.g. 443) that is not compatible with your environment
* The default dispatcher does not work for your older hardware
* The default dispatcher leverages a network_driver name you do not use

## Configuring the Dispatcher

The `dispatcher_mapping` configuration option can be set to extend or map the platform network_driver to a proper nornir class.

```python
PLUGINS_CONFIG = {
  "nautobot_plugin_nornir": {
    "dispatcher_mapping": {
      "newos": "dispatcher.newos",
      "ios": "nornir_nautobot.plugins.tasks.dispatcher.cisco_ios.NautobotNornirDriver",
      "ios_xe": "nornir_nautobot.plugins.tasks.dispatcher.cisco_ios.NautobotNornirDriver",
      "fortinet": "nornir_nautobot.plugins.tasks.dispatcher.default.NetmikoNautobotNornirDriver",
    }
  }
}
```

The above example demonstrates the following use cases.

* Creating a custom only local dispatcher (`"newos"`)
* Mapping a user defined and preferred platform network_driver name to expected driver (`e.g. ios -> cisco_ios`)
* Overloading platform network_driver keys, by mapping ios and ios_xe to the same class (`"ios_xe":`)
* Leveraging the existing "default" Netmiko driver (`"fortinet"`)

Plugin developers that leverage the plugin, are recommended to use the `get_dispatcher` function in `nautobot_plugin_nornir.utils` file to provide the ability to allow users to define their own mappings as described above.
