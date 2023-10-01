"""Credentials class designed to work with Nautobot ORM."""


class NautobotORMCredentials:
    """Abstract Credentials Class designed to work with Nautobot ORM."""

    def get_device_creds(self, device):  # pylint: disable=unused-argument
        """Return the credentials for a given device.

        Args:
            device (dcim.models.Device): Nautobot device object

        Return:
            username (string):
            password (string):
            secret (string):
        """
        return (None, None, None)

    def get_group_creds(self, group_name):  # pylint: disable=unused-argument
        """Return the credentials for a given group.

        Args:
            group_name (string): Name of the group

        Return:
            string: username
            string: password
            string: secret
        """
        return (None, None, None)


class MixinNautobotORMCredentials(NautobotORMCredentials):
    """Abstract Credentials Class mixin, to provide base get_device_creds functionality."""

    def get_device_creds(self, device):
        """Return the credentials for a given device.

        Args:
            device (dcim.models.Device): Nautobot device object

        Return:
            username (string):
            password (string):
            secret (string):
        """
        return (self.username, self.password, self.secret)  # pylint: disable=no-member
