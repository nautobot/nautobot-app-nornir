"""Unit tests for the close_threaded_db_connections decorator (issue #245)."""

from unittest import mock

from django.test import TestCase

from nautobot_plugin_nornir import db_management
from nautobot_plugin_nornir.db_management import close_threaded_db_connections


class CloseThreadedDBConnectionsTests(TestCase):
    """Tests for close_threaded_db_connections decorator return semantics and cleanup."""

    @mock.patch.object(db_management.connections, "close_all")
    @mock.patch.dict(db_management.RUNNER_SETTINGS, {"plugin": "threaded"}, clear=True)
    def test_returns_wrapped_value_when_threaded(self, mock_close_all):
        @close_threaded_db_connections
        def task():
            return {"payload": "data"}

        self.assertEqual(task(), {"payload": "data"})
        mock_close_all.assert_called_once()

    @mock.patch.object(db_management.connections, "close_all")
    @mock.patch.dict(db_management.RUNNER_SETTINGS, {"plugin": "serial"}, clear=True)
    def test_returns_wrapped_value_when_not_threaded(self, mock_close_all):
        @close_threaded_db_connections
        def task():
            return 42

        self.assertEqual(task(), 42)
        mock_close_all.assert_not_called()

    @mock.patch.object(db_management.connections, "close_all")
    @mock.patch.dict(db_management.RUNNER_SETTINGS, {"plugin": "threaded"}, clear=True)
    def test_exception_propagates_and_connections_closed(self, mock_close_all):
        @close_threaded_db_connections
        def task():
            raise ValueError("boom")

        with self.assertRaises(ValueError):
            task()
        mock_close_all.assert_called_once()

    def test_wraps_preserves_metadata(self):
        @close_threaded_db_connections
        def my_task():
            """My task docstring."""

        self.assertEqual(my_task.__name__, "my_task")
        self.assertEqual(my_task.__doc__, "My task docstring.")
