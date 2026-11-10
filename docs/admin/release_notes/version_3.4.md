# v3.4 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Major features or milestones
- Changes to compatibility with Nautobot and/or other apps, libraries etc.

<!-- towncrier release notes start -->

## [v3.4.0 (2026-11-10)](https://github.com/nautobot/nautobot-app-nornir/releases/tag/v3.4.0)

### Added

- [#297](https://github.com/nautobot/nautobot-app-nornir/issues/297) - Added `DebugLoggingMixin` to only record Job debug messages when the `debug` input is enabled.

### Fixed

- [#297](https://github.com/nautobot/nautobot-app-nornir/issues/297) - Fixed `NornirLogger` recording debug messages in the Job Result when its log level was above `DEBUG`.
- [#297](https://github.com/nautobot/nautobot-app-nornir/issues/297) - Fixed `NornirLogger` dropping the `object` and `grouping` values passed in `extra`.
