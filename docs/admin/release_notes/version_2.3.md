
# v2.3 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Changed the minimum Nautobot version support to 2.4.2.
- Added a common Nornir logger for console and database logging.
- Fixed secret group "types" errors for HTTP and new SNMP types.

## [v2.3.0 (2025-10-03)](https://github.com/nautobot/nautobot-app-nornir/releases/tag/v2.3.0)

### Added

- [#215](https://github.com/nautobot/nautobot-app-nornir/issues/215) - Added a common Nornir logger to support writing to console and db.
- [#215](https://github.com/nautobot/nautobot-app-nornir/issues/215) - Added a helper decorator to close idle DB connections in a thread.

### Changed

- [#200](https://github.com/nautobot/nautobot-app-nornir/issues/200) - Build out process for and create actual error docs.

### Fixed

- [#198](https://github.com/nautobot/nautobot-app-nornir/issues/198) - Improved handling of errors when the using Secrets with config_context.
- [#212](https://github.com/nautobot/nautobot-app-nornir/issues/212) - Fixed incorrect secret group association choices "type" lookups.

### Documentation

- [#200](https://github.com/nautobot/nautobot-app-nornir/issues/200) - Update documentation on error codes to provide actual troubleshooting recommendations.

### Housekeeping

- [#202](https://github.com/nautobot/nautobot-app-nornir/issues/202) - Set minimum python version to 3.9.2 in line with Nautobot Core. This is necessary due to upstream `cryptography` constraints, see https://github.com/nautobot/nautobot/pull/7019.
- Rebaked from the cookie `nautobot-app-v2.4.2`.
- Rebaked from the cookie `nautobot-app-v2.5.0`.
- Rebaked from the cookie `nautobot-app-v2.5.1`.
- Rebaked from the cookie `nautobot-app-v2.6.0`.
