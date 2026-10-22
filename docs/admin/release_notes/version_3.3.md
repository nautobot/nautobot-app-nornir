# v3.3 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Add support for nornir-nautobot 5.0.0 major release.
- Supports the change to nornir-nautobot making Scrapli dependencies optional. This requires Scrapli users of nornir-nautobot to install with "scrapli" extras; e.g. `pip install "nautobot-plugin-nornir[scrapli]"`.

<!-- towncrier release notes start -->

## [v3.3.0 (2026-10-22)](https://github.com/nautobot/nautobot-app-nornir/releases/tag/v3.3.0)

### Dependencies

- Add new nornir-nautobot major version 5.0.0 as supported, which supports scrapli changing to optional dependency.

### Housekeeping

- Migrated `pyproject.toml` to the Poetry v2 / PEP 621 `[project]` table syntax.
