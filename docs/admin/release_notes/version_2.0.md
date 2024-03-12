# v2.0 Release Notes

This document describes all new features and changes in the release `2.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Updated `nautobot` to `2.0.0` and made associated changes.
- Added a standard way to provide error codes.
- Removed dispatcher mapping.
- Provided a mechanism to allow for Location Groupings to be configurable.


## [v2.0.1] - 2024-03

### Changed

- [#120](https://github.com/nautobot/nautobot-plugin-nornir/issues/120) - Updated to use Cookiecutter from drift manager.
- [#134](https://github.com/nautobot/nautobot-plugin-nornir/issues/134) - Changed to app vs plugin, first of many.
- [#139](https://github.com/nautobot/nautobot-plugin-nornir/issues/139) - Changed mechanism to get secrets by caching them.

## [v2.0.0] - 2023-09

### Changed

- [#117](https://github.com/nautobot/nautobot-plugin-nornir/issues/117) - Updated `nautobot` to `2.0.0`.
- [#117](https://github.com/nautobot/nautobot-plugin-nornir/issues/117) - Removed `dispatcher_mapping` a similar functionality can be found in Nautobot's Golden Config plugin, but simplified version in nornir-nautobot means this is no longer required.
- [#117](https://github.com/nautobot/nautobot-plugin-nornir/issues/117) - Moved all references of `Platform.slug` to `Platform.network_driver`.
- [#117](https://github.com/nautobot/nautobot-plugin-nornir/issues/117) - Removed references to `.slug` for Nautobot core models and changed to `.name`.
- [#117](https://github.com/nautobot/nautobot-plugin-nornir/issues/117) - Moved all references of `Site` or `Region` to `Location`.

### Added

- [#117](https://github.com/nautobot/nautobot-plugin-nornir/issues/117) - Plugin config `allowed_location_types` to limit what locations are **allowed** based on location types, specifically from `LocationType.name`.
- [#117](https://github.com/nautobot/nautobot-plugin-nornir/issues/117) - Plugin config `denied_location_types` to limit what locations are turned **denied** based on location types, specifically from `LocationType.name`.
- [#117](https://github.com/nautobot/nautobot-plugin-nornir/issues/117) - Added early failure with message when settings are in the wrong location such as `dispatcher_mapping` or `custom_dispatcher`.
- [#117](https://github.com/nautobot/nautobot-plugin-nornir/issues/117) - Added error code framework.
