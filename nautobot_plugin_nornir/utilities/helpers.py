from nautobot.core.utils.data import render_jinja2
from nautobot.dcim.filters import DeviceFilterSet
from nautobot.dcim.models import Device
from nautobot.extras.models import Job
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

    # Handle case where object is from single device run all.
    if data.get("device") and isinstance(data["device"], Device):
        query.update({"id": [str(data["device"].pk)]})
    elif data.get("device"):
        query.update({"id": data["device"].values_list("pk", flat=True)})

    raw_qs = Q()
    # If scope is set to {} do not loop as all devices are in scope.
    if not models.GoldenConfigSetting.objects.filter(dynamic_group__filter__iexact="{}").exists():
        for obj in models.GoldenConfigSetting.objects.all():
            raw_qs = raw_qs | obj.dynamic_group.generate_query()

    base_qs = Device.objects.filter(raw_qs)

    if not base_qs.exists():
        raise NornirNautobotException(
            "`E3015:` The base queryset didn't find any devices. Please check the Golden Config Setting scope."
        )

    devices_filtered = DeviceFilterSet(data=query, queryset=base_qs)

    if not devices_filtered.qs.exists():
        raise NornirNautobotException(
            "`E3016:` The provided job parameters didn't match any devices detected by the Golden Config scope. Please check the scope defined within Golden Config Settings or select the correct job parameters to correctly match devices."
        )
    devices_no_platform = devices_filtered.qs.filter(platform__isnull=True)
    if devices_no_platform.exists():
        raise NornirNautobotException(
            f"`E3017:` The following device(s) {', '.join([device.name for device in devices_no_platform])} have no platform defined. Platform is required."
        )

    return devices_filtered.qs
