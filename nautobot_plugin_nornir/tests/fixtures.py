"""Fixtures for reusable test code."""
from nautobot.dcim.models import Device, DeviceType, Manufacturer, Platform, LocationType, Location
from nautobot.extras.models.roles import ContentType, Role
from nautobot.extras.models.statuses import Status


def create_pre_req_data():
    """Create the data that all tests need."""
    device_content_type = ContentType.objects.get(model="device")
    location_type_region = LocationType.objects.create(name="Region")
    location_type = LocationType.objects.create(name="Site")
    location_type.content_types.set([device_content_type])
    active = Status.objects.get(name="Active")
    location_us = Location.objects.create(
        name="US",
        location_type=location_type_region,
        status_id=active.id,
    )
    Location.objects.create(
        name="USWEST",
        parent=location_us,
        location_type_id=location_type.id,
        status_id=active.id,
    )
    manufacturer1 = Manufacturer.objects.create(name="Juniper")
    Platform.objects.create(name="Juniper Junos", network_driver="juniper_junos", napalm_driver="junos")

    DeviceType.objects.create(model="SRX3600", manufacturer=manufacturer1)
    device_role1 = Role.objects.create(name="Firewall")
    device_role1.content_types.set([device_content_type])
    device_role2 = Role.objects.create(name="Switch")
    device_role2.content_types.set([device_content_type])


def create_test_data():
    """Create test data."""
    create_pre_req_data()
    location = Location.objects.get(name="USWEST")
    device_type1 = DeviceType.objects.get(model="SRX3600")
    platform = Platform.objects.get(name="Juniper Junos")
    device_role1 = Role.objects.get(name="Firewall")
    device_role2 = Role.objects.get(name="Switch")
    active = Status.objects.get(name="Active")
    Device.objects.create(
        name="device1",
        location=location,
        device_type=device_type1,
        platform=platform,
        role=device_role1,
        status_id=active.id,
    )
    Device.objects.create(
        name="device2",
        location=location,
        device_type=device_type1,
        platform=platform,
        role=device_role2,
        status_id=active.id,
    )
