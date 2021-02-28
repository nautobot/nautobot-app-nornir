"""Unit Tests for NautobotORM Inventory."""
from unittest import skip

from django.test import TestCase
from nautobot.dcim.models import Device, Manufacturer, Site, DeviceType, DeviceRole
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory


class NautobotORMInventoryTests(TestCase):
    """Test cases for ensuring the NautobotORM Inventory is working properly."""

    def setUp(self):
        """Create a superuser and token for API calls."""
        self.site1 = Site.objects.create(name="USWEST", slug="uswest")
        self.manufacturer1 = Manufacturer.objects.create(name="Juniper", slug="juniper")
        self.device_type1 = DeviceType.objects.create(slug="srx3600", model="SRX3600", manufacturer=self.manufacturer1)
        self.device_role1 = DeviceRole.objects.create(name="Firewall", slug="firewall")
        self.device_role2 = DeviceRole.objects.create(name="Switch", slug="switch")

        Device.objects.create(
            name="device1",
            site=self.site1,
            device_type=self.device_type1,
            device_role=self.device_role1,
        )

        Device.objects.create(
            name="device2",
            site=self.site1,
            device_type=self.device_type1,
            device_role=self.device_role2,
        )

    @staticmethod
    @skip("Starter skip")
    def test_init_default():
        """Ensure inventory is working properly with default settings."""
        inv = NautobotORMInventory()
        assert len(inv.hosts) == 2  # pylint: disable=no-member

    @staticmethod
    @skip("Starter skip")
    def test_init_queryset():
        """Ensure the inventory is working properly when a queryset is provided."""
        queryset = Device.objects.filter(name="device1")
        inv = NautobotORMInventory(queryset=queryset)
        assert len(inv.hosts) == 1  # pylint: disable=no-member

    @staticmethod
    @skip("Starter skip")
    def test_init_filters():
        """Ensure the inventory is working properly when a filters dict is provided."""
        inv = NautobotORMInventory(filters=dict(name="device1"))
        assert len(inv.hosts) == 1  # pylint: disable=no-member
