---
name: reference-default-settings-merge
description: How Nautobot's AppConfig.default_settings merge actually works (shallow, top-level only) — verified from nautobot source
metadata:
  type: reference
---

Nautobot's `PluginConfig.validate(user_config, nautobot_version)` (in
`nautobot/extras/plugins/__init__.py`) merges `default_settings` into
`PLUGINS_CONFIG[app_name]` with a **shallow, top-level-only** merge:

```python
for setting, value in cls.default_settings.items():
    if setting not in user_config and setting not in cls.constance_config:
        user_config[setting] = value
```

Key implications for reviewing any app's `default_settings`:
- If a user supplies the top-level key at all (e.g. `nornir_settings`), the
  *entire* default value for that key is skipped — nested keys are never
  merged in. A user who overrides `nornir_settings` with only `{"credentials": ...}`
  silently loses every other nested default (`inventory`, `runner`, etc.).
  This is a platform-wide behavior, not specific to any one app, so it's
  correct/expected for an app's docs to call this out with a warning rather
  than trying to implement a deep-merge workaround in the app itself.
- `settings.PLUGINS_CONFIG[app_name]` is guaranteed to exist by the time
  `validate()` runs — `load_plugin()` in `nautobot/extras/plugins/utils.py`
  does `if plugin_name not in settings.PLUGINS_CONFIG: settings.PLUGINS_CONFIG[plugin_name] = {}`
  before calling `validate()`. So app code (e.g. `ready()`) can safely index
  `settings.PLUGINS_CONFIG[app_name]` without `.get()`.
- This merge happens during Nautobot's plugin-loading phase (before Django
  app registry `ready()` and before any app submodule that reads
  `settings.PLUGINS_CONFIG` at import time), so module-level constants built
  from `PLUGINS_CONFIG.get(...)` (e.g. a `constants.py` pattern) see the
  merged defaults correctly.

Also relevant: `invoke generate-app-config-schema` (via
`development/app_config_schema.py`) fully overwrites `app-config-schema.json`
from whatever is in the *current runtime* `PLUGINS_CONFIG` — it only infers
schema properties for keys actually present in that dict (enriched with
`default_settings`/`required_settings` for those keys). Any config key that
isn't set anywhere (dev config *and* not in `default_settings`) silently
disappears from the regenerated schema. Treat this file as hand-maintained;
diff/merge generator output rather than accepting it wholesale.

See [[project-nornir-app-nornir-settings-defaults]] for the PR that surfaced this.
