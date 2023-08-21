"""Unit Tests for NautobotORM Inventory."""
from django.test import TestCase
from nautobot.dcim.models import Device, DeviceType, Manufacturer, Location
from nautobot.extras.models.roles import Role
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory


class NautobotORMInventoryTests(TestCase):
    """Test cases for ensuring the NautobotORM Inventory is working properly."""

    def setUp(self):
        """Create a superuser and token for API calls."""
        self.site1 = Location.objects.create(name="USWEST")
        self.manufacturer1 = Manufacturer.objects.create(name="Juniper")
        self.device_type1 = DeviceType.objects.create(model="SRX3600", manufacturer=self.manufacturer1)
        self.device_role1 = Role.objects.create(name="Firewall")
        self.device_role2 = Role.objects.create(name="Switch")

        Device.objects.create(
            name="device1",
            location=self.site1,
            device_type=self.device_type1,
            role=self.device_role1,
        )

        Device.objects.create(
            name="device2",
            location=self.site1,
            device_type=self.device_type1,
            role=self.device_role2,
        )

    def test_init_default(self):
        """Ensure inventory is working properly with default settings."""
        inv = NautobotORMInventory()
        self.assertEqual(len(inv.hosts), 2)

    def test_init_queryset(self):
        """Ensure the inventory is working properly when a queryset is provided."""
        queryset = Device.objects.filter(name="device1")
        inv = NautobotORMInventory(queryset=queryset)
        self.assertEqual(len(inv.hosts), 1)

    def test_init_filters(self):
        """Ensure the inventory is working properly when a filters dict is provided."""
        inv = NautobotORMInventory(filters={"name": "device1"})
        self.assertEqual(len(inv.hosts), 1)
