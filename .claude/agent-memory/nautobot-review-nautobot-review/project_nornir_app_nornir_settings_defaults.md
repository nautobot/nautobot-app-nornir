---
name: project-nornir-app-nornir-settings-defaults
description: Ongoing work (branch jw-napps-953-default-settings, issue #278) moving nornir_settings defaults into NautobotPluginNornirConfig.default_settings
metadata:
  type: project
---

Branch `jw-napps-953-default-settings` (Jira NAPPS-953, GitHub issue #278) in
`nautobot-app-nornir` moves the app's `nornir_settings` fallback defaults
(inventory class, credentials class, threaded runner w/ 20 workers) out of a
private `_NORNIR_SETTINGS` dict in `constants.py` and into
`NautobotPluginNornirConfig.default_settings` in `nautobot_plugin_nornir/__init__.py`,
so `PLUGINS_CONFIG["nautobot_plugin_nornir"]` is no longer required at all.

**Why:** Centralizes defaults in the one place Nautobot's own plugin-loading
convention expects (`default_settings`), rather than duplicating them ad hoc
in application code — see [[reference-default-settings-merge]] for the
mechanics. As a side effect, this fixes a latent gap: the old fallback dict's
`runner` key never included `"plugin": "threaded"` (only `options.num_workers`),
so `db_management.RUNNER_SETTINGS.get("plugin") == "threaded"` was always
False for any deployment that relied on the fallback — meaning idle DB
connection cleanup silently never ran for those deployments, even though
Nornir itself defaults its own runner to `"threaded"` internally.

**How to apply:** When reviewing follow-up PRs on this branch/ticket, expect
further iteration on `docs/admin/install.md`, `app-config-schema.json`, and
`tests/test_app_config.py` — the working tree has shown multiple rounds of
self-revision (test consolidated to fewer structural assertions, schema
`description` fields added, doc warning condensed) even after the initial
commit landed. Check `git diff HEAD` (not just `git diff develop...HEAD`) for
this branch, since uncommitted amendments have consistently trailed the last
commit — don't assume the committed diff is the final state.
