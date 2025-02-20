# v1.0 Release Notes


## Release Overview

- Add provider class for Nautobot Secrets Functionality

## [v1.0.5] - 2024-04

### Fixed

- [#155](https://github.com/nautobot/nautobot-plugin-nornir/issues/155) - Fixed secrets group access type overrides not working.

## [v1.0.4] - 2024-04

### Fixed

- [#153](https://github.com/nautobot/nautobot-plugin-nornir/issues/153) - Fixed credential cache when using Nautobot secrets.


## [v1.0.3] - 2024-04

### Fixed

- [#147](https://github.com/nautobot/nautobot-plugin-nornir/issues/147) - Changed mechanism to get secrets by caching them.

## [v1.0.2] - 2024-04

### Fixed

- [#143](https://github.com/nautobot/nautobot-plugin-nornir/issues/143) - Deprecate Python 3.7 add Python 3.11.

## [v1.0.1] - 2023-08

### Changed

- [#53](https://github.com/nautobot/nautobot-plugin-nornir/issues/53) - Update credentials for GH publishing.
- [#60](https://github.com/nautobot/nautobot-plugin-nornir/issues/60) - Doc cleanup and better error handling.
- [#62](https://github.com/nautobot/nautobot-plugin-nornir/issues/62) - Update readme to describe secrets usage.
- [#63](https://github.com/nautobot/nautobot-plugin-nornir/issues/63) - Update docs to new standards and development environment to NTC standards.
- [#64](https://github.com/nautobot/nautobot-plugin-nornir/issues/64) - Update links on Readme to point to read the docs page.
- [#65](https://github.com/nautobot/nautobot-plugin-nornir/issues/65) - More update links on Readme to point to read the docs page.
- [#66](https://github.com/nautobot/nautobot-plugin-nornir/issues/66) - Even more update links on Readme to point to read the docs page.
- [#69](https://github.com/nautobot/nautobot-plugin-nornir/issues/69) - Add suggested custom CSS for mkdocstrings indentation.
- [#70](https://github.com/nautobot/nautobot-plugin-nornir/issues/70) - Remove Args from class definition docstring.
- [#80](https://github.com/nautobot/nautobot-plugin-nornir/issues/80) - Update docs to new standards and development environment to NTC standards March addition.
- [#72](https://github.com/nautobot/nautobot-plugin-nornir/issues/72) - Update __init__.py to better describe the app in the UI.
- [#93](https://github.com/nautobot/nautobot-plugin-nornir/issues/93) - fix and cleanup some incorrect docs.

### Fixed

- [#68](https://github.com/nautobot/nautobot-plugin-nornir/issues/68) - Merge dispatcher rather than overwrite.
- [#91](https://github.com/nautobot/nautobot-plugin-nornir/issues/91) - Fix conn_options by using deepcopy to avoid pointers.
- [#102](https://github.com/nautobot/nautobot-plugin-nornir/issues/102) - Fix jinja settings support for golden config plugin.

## [v1.0.0] - 2022-02

### Changed

- [#43](https://github.com/nautobot/nautobot-plugin-nornir/issues/43) Update postgres Docker tag to v14.
- [#46](https://github.com/nautobot/nautobot-plugin-nornir/issues/46) Update Dependencies.
- [#48](https://github.com/nautobot/nautobot-plugin-nornir/issues/48) Make consistent default NORNIR_SETTINGS.

### Added

- [#41](https://github.com/nautobot/nautobot-plugin-nornir/issues/41) Configure Renovate.
- [#45](https://github.com/nautobot/nautobot-plugin-nornir/issues/45) Add napalm/netmiko extras support to plugin config.
- [#49](https://github.com/nautobot/nautobot-plugin-nornir/issues/49) Add provider class for Nautobot Secrets Functionality.

