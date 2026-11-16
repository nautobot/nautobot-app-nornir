"""Custom logger to support writing to console and db."""

import logging
from typing import Any

LOGGER = logging.getLogger("NORNIR_LOGGER")

handler = logging.StreamHandler()
handler.setLevel(logging.NOTSET)
LOGGER.addHandler(handler)
LOGGER_ADAPTER = logging.LoggerAdapter(LOGGER, extra={})


class DebugLoggingMixin:  # pylint: disable=too-few-public-methods
    """Job mixin to only record debug log messages when the job's `debug` input is enabled.

    Nautobot sets job loggers to `DEBUG` so that every message reaches the job result. This mixin sets the job
    logger to `DEBUG` or `INFO` from the `debug` job input before the job runs, and restores the original level
    afterwards. List it before `Job` in the job's bases, and pass `self.logger.getEffectiveLevel()` to
    `NornirLogger` so Nornir plays follow the same level.
    """

    def before_start(self, task_id, args, kwargs):
        """Set the job logger level from the `debug` input."""
        # The job logger is shared by every job in its module within a worker process, so `after_return` restores it.
        # The logger object is kept as well, since code run by the job may replace `self.logger` before then.
        self._original_logger = self.logger  # pylint: disable=attribute-defined-outside-init
        self._original_log_level = self.logger.level  # pylint: disable=attribute-defined-outside-init
        super().before_start(task_id, args, kwargs)
        self.logger.setLevel(logging.DEBUG if kwargs.get("debug") else logging.INFO)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):  # pylint: disable=too-many-arguments
        """Restore the level saved in `before_start` on the logger it was saved from."""
        self._original_logger.setLevel(self._original_log_level)
        super().after_return(status, retval, task_id, args, kwargs, einfo)


class NornirLogger:
    """Logger that handles same signature as standard Python Library logging but also write to db."""

    def __init__(self, job_result, log_level: int):
        """Initialize the object."""
        self.job_result = job_result
        LOGGER.setLevel(log_level)

    def _logging_helper(self, attr: str, message: str, *args: Any, extra: Any = None):
        """Logger helper to set both db and console logs at once."""
        if not LOGGER.isEnabledFor(getattr(logging, attr.upper())):
            return
        if args:
            # Format the way the standard library does, only once the message is known to be logged.
            message = logging.LogRecord(LOGGER.name, logging.NOTSET, "", 0, message, args, None).getMessage()
        if not extra:
            extra = {}
        getattr(LOGGER_ADAPTER, attr)(message, extra=extra)
        self.job_result.log(message, level_choice=attr, obj=extra.get("object"), grouping=extra.get("grouping", "main"))

    def debug(self, message: str, *args: Any, extra: Any = None):
        """Match standard Python Library debug signature."""
        self._logging_helper("debug", message, *args, extra=extra)

    def info(self, message: str, *args: Any, extra: Any = None):
        """Match standard Python Library info signature."""
        self._logging_helper("info", message, *args, extra=extra)

    def warning(self, message: str, *args: Any, extra: Any = None):
        """Match standard Python Library warning signature."""
        self._logging_helper("warning", message, *args, extra=extra)

    def error(self, message: str, *args: Any, extra: Any = None):
        """Match standard Python Library error signature."""
        self._logging_helper("error", message, *args, extra=extra)

    def critical(self, message: str, *args: Any, extra: Any = None):
        """Match standard Python Library critical signature."""
        self._logging_helper("critical", message, *args, extra=extra)
