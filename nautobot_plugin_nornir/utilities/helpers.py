"""Helper functions."""
# pylint: disable=raise-missing-from
from django.db.models import Q
from nautobot.dcim.filters import DeviceFilterSet
from nautobot.dcim.models import Device, DeviceType, Location, Manufacturer, Platform, Rack, RackGroup
from nautobot.extras.jobs import BooleanVar, MultiObjectVar
from nautobot.extras.models import Role, Status, Tag
from nautobot.tenancy.models import Tenant, TenantGroup
from nornir_nautobot.exceptions import NornirNautobotException

FIELDS_PK = {
    "platform",
    "tenant_group",
    "tenant",
    "location",
    "role",
    "rack",
    "rack_group",
    "manufacturer",
    "device_type",
}

FIELDS_NAME = {"tags", "status"}


def get_job_filter(data=None, raw_qs=Q()):
    """
    Helper function to return a the filterable list of OS's based on platform.name and a specific custom value.

    Args:
        data: Job data from input form.
        raw_qs: Can be used to to filter out non-scoped devices. E.g. GC filtering out device not in dynamic group scope.
    """
    if not data:
        data = {}
    query = {}

    # Translate instances from FIELDS set to list of primary keys
    for field in FIELDS_PK:
        if data.get(field):
            query[field] = data[field].values_list("pk", flat=True)

    # Translate instances from FIELDS set to list of names
    for field in FIELDS_NAME:
        if data.get(field):
            query[field] = data[field].values_list("name", flat=True)

    # Handle case where object is from single device run all.
    if data.get("device") and isinstance(data["device"], Device):
        query.update({"id": [str(data["device"].pk)]})
    elif data.get("device"):
        query.update({"id": data["device"].values_list("pk", flat=True)})

    base_qs = Device.objects.filter(raw_qs)

    if not base_qs.exists():
        raise NornirNautobotException(
            "`E3015:` The base queryset didn't find any devices. Please check the job inputs or any additonal scopes."
        )

    devices_filtered = DeviceFilterSet(data=query, queryset=base_qs)

    if not devices_filtered.qs.exists():
        raise NornirNautobotException(
            "`E3016:` The provided job parameters didn't match any devices. Please check ay scope(s) defined or select the correct job parameters to correctly match devices."
        )
    devices_no_platform = devices_filtered.qs.filter(platform__isnull=True)
    if devices_no_platform.exists():
        raise NornirNautobotException(
            f"`E3017:` The following device(s) {', '.join([device.name for device in devices_no_platform])} have no platform defined. Platform is required."
        )

    return devices_filtered.qs


class FormEntry:  # pylint disable=too-few-public-method
    """Class definition to use as Mixin for form definitions."""

    tenant_group = MultiObjectVar(model=TenantGroup, required=False)
    tenant = MultiObjectVar(model=Tenant, required=False)
    location = MultiObjectVar(model=Location, required=False)
    rack_group = MultiObjectVar(model=RackGroup, required=False)
    rack = MultiObjectVar(model=Rack, required=False)
    role = MultiObjectVar(model=Role, required=False)
    manufacturer = MultiObjectVar(model=Manufacturer, required=False)
    platform = MultiObjectVar(model=Platform, required=False)
    device_type = MultiObjectVar(model=DeviceType, required=False, display_field="display_name")
    device = MultiObjectVar(model=Device, required=False)
    tags = MultiObjectVar(
        model=Tag, required=False, display_field="name", query_params={"content_types": "dcim.device"}
    )
    status = MultiObjectVar(
        model=Status,
        required=False,
        query_params={"content_types": Device._meta.label_lower},
        display_field="label",
        label="Device Status",
    )
    debug = BooleanVar(description="Enable for more verbose debug logging")
