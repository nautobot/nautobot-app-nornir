"""Unit Tests for NautobotORM Inventory."""
from django.test import TestCase
from nautobot.dcim.models import Device, DeviceType, Manufacturer, Platform, LocationType, Location
from nautobot.extras.models.roles import ContentType, Role
from nautobot.extras.models.statuses import Status
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory


class NautobotORMInventoryTests(TestCase):
    """Test cases for ensuring the NautobotORM Inventory is working properly."""

    def setUp(self):
        """Create a superuser and token for API calls."""
        device_content_type = ContentType.objects.get(model="device")
        self.location_type = LocationType.objects.create(name="Site")
        self.location_type.content_types.set([device_content_type])
        active = Status.objects.get(name="Active")
        self.site1 = Location.objects.create(name="USWEST", location_type_id=self.location_type.id, status_id=active.id)
        self.manufacturer1 = Manufacturer.objects.create(name="Juniper")
        self.platform = Platform.objects.create(name="Cisco IOS", network_driver="junos", napalm_driver="junos")
        self.device_type1 = DeviceType.objects.create(model="SRX3600", manufacturer=self.manufacturer1)
        self.device_role1 = Role.objects.create(name="Firewall")
        self.device_role1.content_types.set([device_content_type])
        self.device_role2 = Role.objects.create(name="Switch")
        self.device_role2.content_types.set([device_content_type])

        Device.objects.create(
            name="device1",
            location=self.site1,
            device_type=self.device_type1,
            platform=self.platform,
            role=self.device_role1,
            status_id=active.id,
        )

        Device.objects.create(
            name="device2",
            location=self.site1,
            device_type=self.device_type1,
            platform=self.platform,
            role=self.device_role2,
            status_id=active.id,
        )

    def test_init_default(self):
        """Ensure inventory is working properly with default settings."""
        inv = NautobotORMInventory().load()
        self.assertEqual(len(inv.hosts), 2)

    def test_init_queryset(self):
        """Ensure the inventory is working properly when a queryset is provided."""
        queryset = Device.objects.filter(name="device1")
        inv = NautobotORMInventory(queryset=queryset).load()
        self.assertEqual(len(inv.hosts), 1)

    def test_init_filters(self):
        """Ensure the inventory is working properly when a filters dict is provided."""
        inv = NautobotORMInventory(filters={"name": "device1"}).load()
        self.assertEqual(len(inv.hosts), 1)
