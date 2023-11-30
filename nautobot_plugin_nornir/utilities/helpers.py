"""Helper functions."""
# pylint: disable=raise-missing-from
from django.db.models import Q
from jinja2 import exceptions as jinja_errors
from nautobot.dcim.filters import DeviceFilterSet
from nautobot.dcim.models import Device
from nornir_nautobot.exceptions import NornirNautobotException

FIELDS = {
    "platform",
    "tenant_group",
    "tenant",
    "region",
    "site",
    "role",
    "rack",
    "rack_group",
    "manufacturer",
    "device_type",
}


def get_job_filter(data=None):
    """Helper function to return a the filterable list of OS's based on platform.slug and a specific custom value."""
    if not data:
        data = {}
    query = {}

    # Translate instances from FIELDS set to list of primary keys
    for field in FIELDS:
        if data.get(field):
            query[f"{field}_id"] = data[field].values_list("pk", flat=True)

    # Build tag query based on slug values for each instance
    if data.get("tag"):
        query.update({"tag": data["tag"].values_list("slug", flat=True)})

    # Build tag query based on slug values for each instance
    if data.get("status"):
        query.update({"status": data["status"].values_list("slug", flat=True)})

    # Handle case where object is from single device run all.
    if data.get("device") and isinstance(data["device"], Device):
        query.update({"id": [str(data["device"].pk)]})
    elif data.get("device"):
        query.update({"id": data["device"].values_list("pk", flat=True)})

    # query:{'site_id': <RestrictedQuerySet [UUID('b366a518-ef20-46ba-b1f2-c03fcfb99c16')]>, 'platform_id': <RestrictedQuerySet [UUID('4f88d73d-e2fa-45c4-938b-7fcfbb02efc5')]>}
    raw_qs = Q()

    # base_qs is basically all devices should/will be limited by scope later (in GC plugin at least)
    base_qs = Device.objects.filter(raw_qs)

    print(f"====\n\nBASEQS: {base_qs}\n\n")
    print(f"====\n\nQUERY: {query}\n\n")

    if not base_qs.exists():
        raise NornirNautobotException(
            "The base queryset didn't find any devices. Please check the Golden Config Setting scope."
        )
    devices_filtered = DeviceFilterSet(data=query, queryset=base_qs)
    if not devices_filtered.qs.exists():
        raise NornirNautobotException(
            "The provided job parameters didn't match any devices detected by the Golden Config scope. Please check the scope defined within Golden Config Settings or select the correct job parameters to correctly match devices."
        )
    devices_no_platform = devices_filtered.qs.filter(platform__isnull=True)
    if devices_no_platform.exists():
        raise NornirNautobotException(
            f"The following device(s) {', '.join([device.name for device in devices_no_platform])} have no platform defined. Platform is required."
        )

    return devices_filtered.qs
