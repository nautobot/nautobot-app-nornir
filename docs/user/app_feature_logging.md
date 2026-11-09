# Job Logging

The App provides two helpers in `nautobot_plugin_nornir.logger` for Jobs that run Nornir plays: `NornirLogger`, which writes Nornir play messages to the Job Result, and `DebugLoggingMixin`, which only records debug messages when the Job's `debug` input is enabled.

## NornirLogger

`NornirLogger` takes the same calls as a standard Python logger (`debug`, `info`, `warning`, `error`, `critical`) and writes each message both to the console and to the Job Result. Pass it to Nornir tasks and processors that run outside the Job's own `self.logger`.

Messages below the level passed to `NornirLogger` are dropped, for both the console and the Job Result. Pass an explicit level such as `logging.INFO`, or the Job logger's effective level as shown below.

!!! warning
    `logging.NOTSET` (`0`) does not mean "log everything". The logger then uses the root logger's level, which is often `WARNING`, so `info` messages would be dropped too. Use `logging.INFO` when debug is off.

The optional `extra` argument links an entry to an object and places it in a group on the Job Result:

```python
logger.info("Backup completed.", extra={"object": device, "grouping": "Backup"})
```

Without a `grouping`, entries go in the `main` group.

## DebugLoggingMixin

Nautobot sets Job loggers to `DEBUG`, so every `self.logger.debug(...)` call is recorded in the Job Result whether or not the user asked for debug output. `DebugLoggingMixin` sets the Job logger to `DEBUG` when the Job's `debug` input is enabled and to `INFO` otherwise, and restores the original level when the Job finishes. Jobs from the same module share one logger within a worker process, so the restore keeps the level from carrying over to the next Job.

List the mixin before `Job` in the Job's bases, add a `debug` input, and build `NornirLogger` from the Job logger's effective level so Nornir plays follow the same setting:

```python
from nautobot.apps.jobs import BooleanVar, Job

from nautobot_plugin_nornir.logger import DebugLoggingMixin, NornirLogger


class BackupJob(DebugLoggingMixin, Job):
    debug = BooleanVar(description="Enable for more verbose debug logging")

    def run(self, *args, **kwargs):
        logger = NornirLogger(self.job_result, self.logger.getEffectiveLevel())
        ...
```

If a Job overrides `before_start` or `after_return`, it must call `super()` so the mixin still runs.
