# v0.9 Release Notes

## Release Overview

- Initial Release

## [v0.9.7] - 2021-11

### Fixed

- [#37](https://github.com/nautobot/nautobot-plugin-nornir/issues/37) Fix dev dependencies and loosen Python 3.6 requirements

## [v0.9.6] - 2021-11

### Fixed

- [#35](https://github.com/nautobot/nautobot-plugin-nornir/issues/35) Fix bug introduced in secret support, update pinned nornir-nautobot version

### Added

- [#35](https://github.com/nautobot/nautobot-plugin-nornir/issues/35) Testing support for Python 3.10


## [v0.9.5] - 2021-11

### Added

- [#32](https://github.com/nautobot/nautobot-plugin-nornir/issues/32) Add device secret support for nautobot pin and updated black pinned version
- [#30](https://github.com/nautobot/nautobot-plugin-nornir/issues/30) Use .get and return empty dict when getting PLUGIN_CFG in constants.py 

### Fixed

- [#31](https://github.com/nautobot/nautobot-plugin-nornir/issues/31) Correct module names to nornir_nautobot in the dispatcher_mapping section of README.md

## [v0.9.4] - 2021-09

### Added

- [#25](https://github.com/nautobot/nautobot-plugin-nornir/issues/25) Switch to GH Actions
- [#26](https://github.com/nautobot/nautobot-plugin-nornir/issues/26) Fail gracefully from empty queryset and missing platform, update dev env to celery

## [v0.9.3] - 2021-07

### Fixed

- [#22](https://github.com/nautobot/nautobot-plugin-nornir/issues/22) Loosen nautobot dep

## [v0.9.2] - 2021-06

### Added

- [#20](https://github.com/nautobot/nautobot-plugin-nornir/issues/20) Added changelog
- [#20](https://github.com/nautobot/nautobot-plugin-nornir/issues/20) Add Travis deployment
- [#20](https://github.com/nautobot/nautobot-plugin-nornir/issues/20) Add Dynamic dispatcher