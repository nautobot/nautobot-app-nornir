"""Unit Tests for NautobotORM Inventory."""
from unittest.mock import patch
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
        location_type_region = LocationType.objects.create(name="Region")
        self.location_type = LocationType.objects.create(name="Site")
        self.location_type.content_types.set([device_content_type])
        active = Status.objects.get(name="Active")
        location_us = Location.objects.create(
            name="US",
            location_type=location_type_region,
            status_id=active.id,
        )
        self.location = Location.objects.create(
            name="USWEST",
            parent=location_us,
            location_type_id=self.location_type.id,
            status_id=active.id,
        )
        self.manufacturer1 = Manufacturer.objects.create(name="Juniper")
        self.platform = Platform.objects.create(
            name="Juniper Junos", network_driver="juniper_junos", napalm_driver="junos"
        )
        self.device_type1 = DeviceType.objects.create(model="SRX3600", manufacturer=self.manufacturer1)
        self.device_role1 = Role.objects.create(name="Firewall")
        self.device_role1.content_types.set([device_content_type])
        self.device_role2 = Role.objects.create(name="Switch")
        self.device_role2.content_types.set([device_content_type])

        Device.objects.create(
            name="device1",
            location=self.location,
            device_type=self.device_type1,
            platform=self.platform,
            role=self.device_role1,
            status_id=active.id,
        )

        Device.objects.create(
            name="device2",
            location=self.location,
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

    def test_init_filters_device(self):
        """Ensure the inventory is working properly when a filters dict is provided."""
        inv = NautobotORMInventory(filters={"name": "device1"}).load()
        self.assertEqual(len(inv.hosts), 1)

    def test_hosts_platform(self):
        """Ensure platform is assigned to hosts."""
        inv = NautobotORMInventory().load()
        self.assertEqual(inv.hosts["device1"]["connection_options"]["napalm"]["platform"], self.platform.napalm_driver)
        self.assertEqual(inv.hosts["device2"]["connection_options"]["napalm"]["platform"], self.platform.napalm_driver)

    def test_get_all_devices_to_parent_mapping(self):
        """Ensure the mapping of devices to parents is correct."""
        self.assertEqual(
            NautobotORMInventory().get_all_devices_to_parent_mapping(),
            {
                "device1": ["location__USWEST", "location__US"],
                "device2": ["location__USWEST", "location__US"],
            },
        )

    @patch("nautobot_plugin_nornir.plugins.inventory.nautobot_orm.ALLOWED_LOCATION_TYPES", ["Region"])
    def test_get_all_devices_to_parent_mapping_allowed(self):
        """Ensure the mapping of devices to parents is correct with allowed locations."""
        self.assertEqual(
            NautobotORMInventory().get_all_devices_to_parent_mapping(),
            {
                "device1": ["location__US"],
                "device2": ["location__US"],
            },
        )

    @patch("nautobot_plugin_nornir.plugins.inventory.nautobot_orm.DENIED_LOCATION_TYPES", ["Site"])
    def test_get_all_devices_to_parent_mapping_denied(self):
        """Ensure the mapping of devices to parents is correct with denied locations."""
        self.assertEqual(
            NautobotORMInventory().get_all_devices_to_parent_mapping(),
            {
                "device1": ["location__US"],
                "device2": ["location__US"],
            },
        )
