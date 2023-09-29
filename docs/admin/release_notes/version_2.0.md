# v2.0 Release Notes

This document describes all new features and changes in the release `2.0`. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

Updated `nautobot` to `2.0.0`.

## [v2.0.0] - 2023-09-29

### Changed

- Updated `nautobot` to `2.0.0`.
- `dispatcher_mapping` plugin config tracks `Platform.network_driver`, but previously tracked 
- Moved all references of `Platform.slug` to `Platform.network_driver`
- Removed references to `.slug` for Nautobot core models and changed to `.name`

### Added

- Plugin config `allowed_location_types` to limit the returned available locations to `LocationType.name`
- Plugin config `denied_location_types` to exclude the returned available locations to `LocationType.name`
