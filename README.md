# Nautobot Plugin Nornir

<p align="center">
  <img src="https://raw.githubusercontent.com/nautobot/nautobot-plugin-nornir/develop/docs/images/icon-NautobotPluginNornir.png" class="logo" height="200px">
  <br>
  <a href="https://github.com/nautobot/nautobot-plugin-nornir/actions"><img src="https://github.com/nautobot/nautobot-plugin-nornir/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://docs.nautobot.com/projects/plugin-nornir/en/latest"><img src="https://readthedocs.org/projects/nautobot-plugin-nornir/badge/"></a>
  <a href="https://pypi.org/project/nautobot-plugin-nornir/"><img src="https://img.shields.io/pypi/v/nautobot-plugin-nornir"></a>
  <a href="https://pypi.org/project/nautobot-plugin-nornir/"><img src="https://img.shields.io/pypi/dm/nautobot-plugin-nornir"></a>
  <br>
  An App for <a href="https://github.com/nautobot/nautobot">Nautobot</a>.
</p>

## Overview

A plugin for [Nautobot](https://github.com/nautobot/nautobot), that intends to be a small shim layer between [nornir-nautobot](https://github.com/nautobot/nornir-nautobot) and other plugins. The primary abilities that the plugin provides is a native Nornir ORM based inventory and a credential manager.

![Architecture Overview](https://raw.githubusercontent.com/nautobot/nautobot-plugin-nornir/develop/docs/images/architecture-overview.png)

As of the writing of this readme, the only plugin leveraging this plugin is the [golden-config](https://github.com/nautobot/nautobot-plugin-golden-config). However, future plugins are planned, such as the "network importer".

That being said, there is currently little reason to install this plugin by itself, without an enabler, which can be seen represented as the white rectangles inside the yellow rectangle in the diagram above. An enabler could be a Plugin, Job, or another piece of code like a Chatops command.

### Screenshots

As previously mentioned, the plugin is mostly a shim layer, here is an example of how Nautobot Golden Config uses a Nornir Job.

![Backup Job](https://raw.githubusercontent.com/nautobot/nautobot-plugin-nornir/develop/docs/images/nornir-backup-job.png)

## Try it out!

This App is installed in the Nautobot Community Sandbox found over at [demo.nautobot.com](https://demo.nautobot.com/)! This is used within the Nautobot Golden Config plugin, when the tasks of generating config, running backup of configs, or comparing configs.

> For a full list of all the available always-on sandbox environments, head over to the main page on [networktocode.com](https://www.networktocode.com/nautobot/sandbox-environments/).

## Documentation

Full web-based HTML documentation for this app can be found over on the [Nautobot Docs](https://docs.nautobot.com/projects/plugin-nornir/en/latest/) website:

- [User Guide](https://docs.nautobot.com/projects/plugin-nornir/en/latest/user/app_overview/) - Overview, Using the App, Getting Started.
- [Administrator Guide](https://docs.nautobot.com/projects/plugin-nornir/en/latest/admin/admin_install/) - How to Install, Configure, Upgrade, or Uninstall the App.
- [Developer Guide](https://docs.nautobot.com/projects/plugin-nornir/en/latest/dev/dev_contributing/) - Extending the App, Code Reference, Contribution Guide.
- [Release Notes / Changelog](https://docs.nautobot.com/projects/plugin-nornir/en/latest/admin/release_notes/).
- [Frequently Asked Questions](https://docs.nautobot.com/projects/plugin-nornir/en/latest/user/app_faq/).

### Contributing to the Docs

You can find all the Markdown source for the App documentation under the [docs](https://github.com/nautobot/nautobot-plugin-nornir/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient - clone the repository and edit away.

If you need to view the fully generated documentation site, you can build it with [mkdocs](https://www.mkdocs.org/). A container hosting the docs will be started using the invoke commands (details in the [Development Environment Guide](https://docs.nautobot.com/projects/plugin-nornir/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). As your changes are saved, the live docs will be automatically reloaded.

Any PRs with fixes or improvements are very welcome!

## Questions

For any questions or comments, please check the [FAQ](https://docs.nautobot.com/projects/plugin-nornir/en/latest/user/app_faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#nautobot`), sign up [here](http://slack.networktocode.com/) if you don't have an account.
