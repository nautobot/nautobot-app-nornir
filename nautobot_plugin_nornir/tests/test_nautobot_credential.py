"""Tests Nautobot credential."""
import unittest

from nautobot_plugin_nornir.plugins.credentials.env_vars import CredentialsEnvVars


class TestCredentialsEnvVars(unittest.TestCase):
    """Test of the CredentialEnvVars."""

    def test_empty_vars(self):
        """Tests empty var set."""
        params = {}
        test_class = CredentialsEnvVars(params=params)
        self.assertIsNone(test_class.username)
        self.assertIsNone(test_class.password)
        self.assertIsNone(test_class.secret)

    def test_set_vars(self):
        """Tests environment vars being set."""
        params = {
            "username": "test_username",
            "password": "test_password",
            "secret": "test_secret",
        }
        test_class = CredentialsEnvVars(params=params)
        self.assertEqual(test_class.username, "test_username")
        self.assertEqual(test_class.password, "test_password")
        self.assertEqual(test_class.secret, "test_secret")
