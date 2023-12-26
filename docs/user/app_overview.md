# App Overview

This document provides an overview of the App including critical information and import considerations when applying it to your Nautobot environment.

!!! note
    Throughout this documentation, the terms "app" and "plugin" will be used interchangeably.

## Description

A app for [Nautobot](https://github.com/nautobot/nautobot), that intends to be a small shim layer between [nornir-nautobot](https://github.com/nautobot/nornir-nautobot) and other apps. The primary abilities that the app provides is a native Nornir ORM based inventory and a credential manager.

![Architecture Overview](../images/architecture-overview.png)

As of the writing of this readme, the only app leveraging this app is the [golden-config](https://github.com/nautobot/nautobot-app-golden-config). However, future apps are planned, such as the "network importer".

That being said, there is currently little reason to install this app by itself, without an enabler, which can be seen represented as the white rectangles inside the yellow rectangle in the diagram above. An enabler could be a App, Job, or another piece of code like a Chatops command.

## Audience (User Personas) - Who should use this App?

* App developers - looking to create integrations via Nautobot with Nornir
* Users - looking to leverage those apps
* Users - looking to run Nornir via an API and UI (via Nautobot Jobs)

## Authors and Maintainers

* itdependsnetworks
* jeffkala

## Nautobot Features Used

### Extras
