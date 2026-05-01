# v3.2 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Updates nornir-nautobot to a version that includes get_facts.

<!-- towncrier release notes start -->

## [v3.2.1 (2026-04-29)](https://github.com/nautobot/nautobot-app-nornir/releases/tag/v3.2.1)

### Added

- Added `@functools.wraps(func)` to the `close_threaded_db_connections` decorator to preserve the metadata of the wrapped function.

### Fixed

- [#245](https://github.com/nautobot/nautobot-app-nornir/issues/245) - Fixed `close_threaded_db_connections` decorator silently discarding the return value of the wrapped function.

## [v3.2.0 (2026-04-13)](https://github.com/nautobot/nautobot-app-nornir/releases/tag/v3.2.0)

### Dependencies

- [#262](https://github.com/nautobot/nautobot-app-nornir/issues/262) - Update nornir-nautobot to 4.2.0 as floor.
