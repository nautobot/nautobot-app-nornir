# Migrating to v2

While not a replacement of the [Nautobot Migration guide](https://docs.nautobot.com/projects/core/en/stable/development/apps/migration/from-v1/) these migration steps specifically for Nautobot App Nornir are pretty straight forward, here is a quick overview with details information below.

1. Ensure `Platform.network_driver` is set on every `Platform` object you have, in most circumstances running `nautobot-server populate_platform_network_driver` will take care of it.
2. Remove any `dispatcher_mapping` settings you have in your `nautobot_config.py` settings, see Golden Config for alternative options.
3. Configure your Location settings, if you do not want all locations becoming grouped with the `allowed_location_types` or `denied_location_types` settings.

!!! warning
    Before you start, please note the `nautobot-server populate_platform_network_driver` command **must be ran in Nautobot 1.6.2 -> 1.6.X** as it will not work once on Nautobot 2.0.

## Platform Network Driver

The `Platform.slug` has been replace by Nautobot's `Platform.network_driver`. The nice thing about this feature is it provides mappings to all of the major network library (or frameworks) such as Netmiko and NAPALM to properly map between the slightly different names each library provides, such as `cisco_ios` vs `ios`. However, that means that you must now provide the network_driver on the the Platform object.

While still on a Nautobot 1.6 instance, run the command `nautobot-server populate_platform_network_driver`, this will help map all of your `Platform.slug`'s to `Platform.network_driver`. If there are any Platform's missed, you must go in and update the Platforms that will be used by Nautobot App Nornir.

## Dispatcher Settings

The `dispatcher_mapping` configuration has been removed. The use cases covered by it was:

1. The default dispatcher does not support your vendor
2. The default dispatcher uses a connectivity model (e.g. 443) that is not compatible with your environment
3. The default dispatcher does not work for your older hardware
4. The default dispatcher leverages a network_driver name you do not use

Use cases 2 & 4 are covered natively by nornir-nautobot now and for 1 & 3 nautobot-plugin-nornir does not actually directly call the dispatcher and should be pushed off to other systems, such as Golden Config. If you are using Golden Config and fit within use cases 1 & 3, please see Golden Config's documentation.

!!! warning
    Golden Config provides the `custom_dispatcher` method, these settings should go to the `nautobot_golden_config` settings and **NOT** the `nautobot_plugin_nornir` settings.

## Location Information

Previously there were inventory groups automatically created out of each `Region` and `Site` object, with moving everything to `Location` there will automatically be created groups by each of those. This may lead to odd cases in which always having every Location as a group is not desirable. 

Take for instance, you have multiple Locations that are on "floor04" as an example perhaps `nyc-floor04` and `sfo-floor04`, creating grouping in this case may create more confusion than help. For that reason, locations can be allowed or denied based on their `LocationType`. See the [docs](../user/app_feature_inventory.md#inventory-groupings) for more information on how to configure `allowed_location_types` or `denied_location_types`.
