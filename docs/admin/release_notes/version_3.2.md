# v3.2 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Updates nornir-nautobot to a version that includes get_facts.

<!-- towncrier release notes start -->

## [v3.2.4 (2026-08-19)](https://github.com/nautobot/nautobot-app-nornir/releases/tag/v3.2.4)

### Changed

- [#278](https://github.com/nautobot/nautobot-app-nornir/issues/278) - Added default `nornir_settings` to the App configuration, so `PLUGINS_CONFIG` no longer requires a `nautobot_plugin_nornir` entry. A `nornir_settings` dictionary is now merged over the defaults, so it only needs the keys you want to change.

### Fixed

- [#278](https://github.com/nautobot/nautobot-app-nornir/issues/278) - Fixed idle database connection cleanup never running for deployments that supplied no `nornir_settings`. The previous fallback omitted the runner plugin, so the threaded check in `close_threaded_db_connections` was always false.

## [v3.2.3 (2026-08-14)](https://github.com/nautobot/nautobot-app-nornir/releases/tag/v3.2.3)

### Dependencies

- [#274](https://github.com/nautobot/nautobot-app-nornir/issues/274) - Changed the minimum version of nornir-nautobot to 4.4.0.

### Housekeeping

- Rebaked from the cookie `nautobot-app-v3.1.4`.

## [v3.2.2 (2026-07-17)](https://github.com/nautobot/nautobot-app-nornir/releases/tag/v3.2.2)

### Fixed

- [#267](https://github.com/nautobot/nautobot-app-nornir/issues/267) - Fixed YAML indentation in the Device Type Config Context example in the inventory documentation.

### Dependencies

- [#269](https://github.com/nautobot/nautobot-app-nornir/issues/269) - Changed the minimum required `nornir-nautobot` version to 4.3.0.

## [v3.2.1 (2026-04-29)](https://github.com/nautobot/nautobot-app-nornir/releases/tag/v3.2.1)

### Added

- Added `@functools.wraps(func)` to the `close_threaded_db_connections` decorator to preserve the metadata of the wrapped function.

### Fixed

- [#245](https://github.com/nautobot/nautobot-app-nornir/issues/245) - Fixed `close_threaded_db_connections` decorator silently discarding the return value of the wrapped function.

## [v3.2.0 (2026-04-13)](https://github.com/nautobot/nautobot-app-nornir/releases/tag/v3.2.0)

### Dependencies

- [#262](https://github.com/nautobot/nautobot-app-nornir/issues/262) - Update nornir-nautobot to 4.2.0 as floor.
