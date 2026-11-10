"""Unit tests for nautobot_plugin_nornir.logger."""

import logging
from unittest import TestCase, mock

from nautobot_plugin_nornir.logger import LOGGER, DebugLoggingMixin, NornirLogger


class NornirLoggerTests(TestCase):
    """Tests for NornirLogger level filtering and job result fields."""

    def setUp(self):
        self.addCleanup(LOGGER.setLevel, LOGGER.level)
        self.job_result = mock.MagicMock()

    def test_messages_below_log_level_are_not_recorded(self):
        logger = NornirLogger(self.job_result, logging.INFO)

        logger.debug("debug message")
        logger.info("info message")

        self.job_result.log.assert_called_once_with("info message", level_choice="info", obj=None, grouping="main")

    def test_debug_messages_recorded_at_debug_level(self):
        logger = NornirLogger(self.job_result, logging.DEBUG)

        logger.debug("debug message")

        self.job_result.log.assert_called_once_with("debug message", level_choice="debug", obj=None, grouping="main")

    def test_object_and_grouping_passed_to_job_result(self):
        logger = NornirLogger(self.job_result, logging.INFO)
        device = object()

        logger.warning("warning message", extra={"object": device, "grouping": "Backup"})

        self.job_result.log.assert_called_once_with(
            "warning message", level_choice="warning", obj=device, grouping="Backup"
        )


class _BaseJob:
    """Stand-in for `nautobot.apps.jobs.Job` lifecycle hooks."""

    def __init__(self, logger):
        self.logger = logger

    def before_start(self, task_id, args, kwargs):
        """No-op, like `Job.before_start`."""

    def after_return(self, status, retval, task_id, args, kwargs, einfo):  # pylint: disable=too-many-arguments
        """No-op, like `Job.after_return`."""


class _DebugJob(DebugLoggingMixin, _BaseJob):
    pass


class DebugLoggingMixinTests(TestCase):
    """Tests for DebugLoggingMixin setting and restoring the job logger level."""

    def setUp(self):
        self.logger = logging.getLogger("nautobot_plugin_nornir.tests.debug_logging_mixin")
        self.addCleanup(self.logger.setLevel, logging.NOTSET)
        self.logger.setLevel(logging.NOTSET)

    def test_job_logger_level_follows_debug_input_and_is_restored(self):
        for debug, expected_level in ((True, logging.DEBUG), (False, logging.INFO)):
            with self.subTest(debug=debug):
                job = _DebugJob(self.logger)

                job.before_start("task-id", (), {"debug": debug})
                self.assertEqual(self.logger.level, expected_level)

                job.after_return("SUCCESS", None, "task-id", (), {"debug": debug}, None)
                self.assertEqual(self.logger.level, logging.NOTSET)

    def test_job_without_debug_input_logs_at_info(self):
        job = _DebugJob(self.logger)

        job.before_start("task-id", (), {})

        self.assertEqual(self.logger.level, logging.INFO)
