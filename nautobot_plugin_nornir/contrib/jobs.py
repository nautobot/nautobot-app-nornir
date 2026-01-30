"""Job Helpers to use with Nautobot Nornir Jobs."""

from nautobot.apps.jobs import BooleanVar, Job, MultiObjectVar
from nautobot.dcim.filters import DeviceFilterSet
from nautobot.dcim.models import Device, DeviceType, Location, Manufacturer, Platform, Rack, RackGroup
from nautobot.extras.models import Role, Status, Tag
from nautobot.tenancy.models import Tenant, TenantGroup
from nornir_nautobot.exceptions import NornirNautobotException

from nautobot_plugin_nornir.contrib.constants import FIELDS_NAME, FIELDS_PK


def get_job_filter(data=None):
    """Helper function to return a the filterable list of OS's based on platform.name and a specific custom value."""
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

    if data.get("device") and isinstance(data["device"], Device):
        query.update({"id": [str(data["device"].pk)]})
    elif data.get("device"):
        query.update({"id": data["device"].values_list("pk", flat=True)})

    base_qs = Device.objects.filter()
    devices_filtered = DeviceFilterSet(data=query, queryset=base_qs)
    devices_no_platform = devices_filtered.qs.filter(platform__isnull=True)
    if devices_no_platform.exists():
        raise NornirNautobotException(
            f"`E3017:` The following device(s) {', '.join([device.name for device in devices_no_platform])} have no platform defined. Platform is required."
        )

    return devices_filtered.qs


class FormEntry:  # pylint: disable=too-few-public-methods
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


class NornirBaseJob(FormEntry, Job):  # pylint: disable=too-many-instance-attributes
    """Base Job class for Nornir Jobs."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Job Meta Attributes."""

        name = "Nornir Base Job"
        description = "Base Job for Nornir Jobs."
        has_sensitive_variables = False
        hidden = False

    def get_device_queryset(self, data=None):
        """Return filtered device queryset based on form entries."""
        return get_job_filter(data=data)
