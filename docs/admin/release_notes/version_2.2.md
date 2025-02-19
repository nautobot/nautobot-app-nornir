
# v2.2 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Major features or milestones
- Changes to compatibility with Nautobot and/or other apps, libraries etc.

## [v2.2.0 (2025-02-18)](https://github.com/nautobot/nautobot-app-nornir/releases/tag/v2.2.0)

### Added

- [#2](https://github.com/nautobot/nautobot-app-nornir/issues/2) - Add initial set of unittest.

### Fixed

- [#162](https://github.com/nautobot/nautobot-app-nornir/issues/162) - Augment SecretAccessType to support both HTTP(S) with HTTP in _get_secret_value
- [#189](https://github.com/nautobot/nautobot-app-nornir/issues/189) - Drop Python3.8 support.
- [#189](https://github.com/nautobot/nautobot-app-nornir/issues/189) - Bump nornir-nautobot to newest version 3.3.0.
- [#189](https://github.com/nautobot/nautobot-app-nornir/issues/189) - Update CI testing to remove Python3.8 from testing.

### Documentation

- [#164](https://github.com/nautobot/nautobot-app-nornir/issues/164) - Documentation for use_config_context within development config.

### Housekeeping

- [#0](https://github.com/nautobot/nautobot-app-nornir/issues/0) - Rebaked from the cookie `nautobot-app-v2.4.0`.
- [#1](https://github.com/nautobot/nautobot-app-nornir/issues/1) - Rebaked from the cookie `nautobot-app-v2.4.1`.
- [#178](https://github.com/nautobot/nautobot-app-nornir/issues/178) - Fixed release workflow to publish binaries to GitHub.
- [#185](https://github.com/nautobot/nautobot-app-nornir/issues/185) - Fixes two broken links in README.md
