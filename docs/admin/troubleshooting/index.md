# Troubleshooting Overview

In an effort to help with troubleshooting, each expected error, will now emit an error ID, in the format of `E2XXX`, such as `E2004: Platform network_driver missing from device {device.name}, preemptively failed.`. The idea will be to define the error, the error message and some recommended troubleshooting steps or even potentially some fixes.

This is an ongoing effort, but the foundation has been built.

Within the Nautobot ecosystem, you may see various errors, they are distributed between 3 libraries as followed.

| Error Range | App Docs |
| ----------- | ----------- |
| E1001-E1999 | [Nornir Nautobot](https://docs.nautobot.com/projects/nornir-nautobot/en/latest/task/troubleshooting/) |
| E2001-E2999 | [Nautobot App Nornir](https://docs.nautobot.com/projects/plugin-nornir/en/latest/admin/troubleshooting/) |
| E3001-E3999 | [Nautobot Golden Config](https://docs.nautobot.com/projects/golden-config/en/latest/admin/troubleshooting/) |