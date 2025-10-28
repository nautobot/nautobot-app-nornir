"""Jobs for nautobot-plugin-nornir debugging."""

from datetime import datetime

import yaml
from nautobot.apps.jobs import BooleanVar, Job, MultiObjectVar, register_jobs
from nautobot.dcim.filters import DeviceFilterSet
from nautobot.dcim.models import Device, DeviceType, Location, Manufacturer, Platform, Rack, RackGroup
from nautobot.extras.models import Role, Status, Tag
from nautobot.tenancy.models import Tenant, TenantGroup
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir_nautobot.exceptions import NornirNautobotException
from nornir_nautobot.plugins.tasks.dispatcher import dispatcher

from nautobot_plugin_nornir.constants import FIELDS_NAME, FIELDS_PK, NORNIR_SETTINGS
from nautobot_plugin_nornir.logger import NornirLogger
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory
from nautobot_plugin_nornir.plugins.processors.processor import ProcessNornirResults

InventoryPluginRegister.register("nautobot-inventory", NautobotORMInventory)


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


class DebugInventoryJob(Job):
    """Job to debug Nornir Inventory."""

    # Device only instead of FormEntry to limit scope as this can be very verbose.
    device = MultiObjectVar(model=Device, required=True)

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta object boilerplate for compliance."""

        name = "Debug Nornir Inventory"
        description = "Prints inventory details per host, group, defaults."
        has_sensitive_variables = True
        hidden = True

    def run(self, *args, **kwargs):  # pylint: disable=too-many-branches
        """Run config compliance report script."""
        now = datetime.now()
        qs = get_job_filter(data=kwargs)
        after_qs = datetime.now()
        self.logger.info("Queryset Took\n%s", after_qs - now)
        self.logger.info("Queryset Count\n%s", qs.count())
        try:
            now = datetime.now()
            with InitNornir(
                runner=NORNIR_SETTINGS.get("runner"),
                logging={"enabled": False},
                inventory={
                    "plugin": "nautobot-inventory",
                    "options": {
                        "credentials_class": NORNIR_SETTINGS.get("credentials"),
                        "params": NORNIR_SETTINGS.get("inventory_params"),
                        "queryset": qs,
                        "defaults": {"now": datetime.now()},
                    },
                },
            ) as nornir_obj:
                after_qs = datetime.now()
                self.logger.info("Nornir Init Took\n%s", after_qs - now)
                for host, data in nornir_obj.inventory.hosts.items():
                    self.logger.info(
                        "#### %s\n```yaml\n%s```",
                        host,
                        yaml.dump(nornir_obj.inventory.hosts[host], default_flow_style=False),
                        extra={"object": Device.objects.get(id=data.data["id"])},
                    )
                    self.logger.info(
                        "#### %s Data\n```yaml\n%s```",
                        host,
                        yaml.dump(data.dict(), default_flow_style=False),
                        extra={"object": Device.objects.get(id=data.data["id"])},
                    )
                self.logger.info(
                    "#### Default Data\n```yaml\n%s```",
                    yaml.dump(nornir_obj.inventory.defaults.data, default_flow_style=False),
                )
        except Exception as err:
            self.logger.info("%s", err)
            raise


class ConnectivityCheckTask(FormEntry, Job):  # pylint: disable=too-many-instance-attributes
    """Nautobot Job for validating connectivity and authentication."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Job Meta Attributes."""

        name = "Nornir Connectivity and Authentication Check"
        description = "Runs Netutils tcp_ping function, attempts authentication and report status."
        has_sensitive_variables = False
        hidden = True

    def run(self, *args, **kwargs):
        """Run connectivity check and authentication tests."""
        logger = NornirLogger(self.job_result, self.logger.getEffectiveLevel())
        qs = get_job_filter(data=kwargs)
        try:
            with InitNornir(
                runner=NORNIR_SETTINGS.get("runner"),
                logging={"enabled": False},
                inventory={
                    "plugin": "nautobot-inventory",
                    "options": {
                        "credentials_class": NORNIR_SETTINGS.get("credentials"),
                        "params": NORNIR_SETTINGS.get("inventory_params"),
                        "queryset": qs,
                        "defaults": {"now": datetime.now()},
                    },
                },
            ) as nornir_obj:
                nr_with_processors = nornir_obj.with_processors([ProcessNornirResults(logger)])
                connectivity_agg_result = nr_with_processors.run(
                    task=dispatcher,
                    logger=logger,
                    obj=None,
                    name="TEST CONNECTIVITY DISPATCHER",
                    method="check_connectivity",
                    framework="netmiko",
                )
                for host, multi_result in connectivity_agg_result.items():
                    self.logger.info(
                        "Task name: %s  Task Failed: %s",
                        multi_result[-1].name,
                        multi_result[-1].failed,
                        extra={"object": Device.objects.get(name=host)},
                    )
                auth_check_agg_result = nr_with_processors.run(
                    task=dispatcher,
                    logger=logger,
                    obj=None,
                    name="AUTHENTICATION DISPATCHER",
                    method="get_command",
                    framework="netmiko",
                    command=chr(13),
                    # Don't run this task if connectivity check failed
                    on_good=True,
                )
                for host, multi_result in auth_check_agg_result.items():
                    self.logger.info(
                        "Task name: %s  Task Failed: %s",
                        multi_result[-1].name,
                        multi_result[-1].failed,
                        extra={"object": Device.objects.get(name=host)},
                    )
            if not connectivity_agg_result.failed_hosts and not auth_check_agg_result.failed_hosts:
                self.logger.info("All devices passed connectivity and authentication checks.")
                return
            if connectivity_agg_result.failed_hosts:
                self.logger.info(
                    "The following devices failed connectivity checks: %s",
                    ", ".join(list(connectivity_agg_result.failed_hosts.keys())),
                )
            if auth_check_agg_result.failed_hosts:
                self.logger.info(
                    "The following devices failed authentication checks: %s",
                    ", ".join(list(auth_check_agg_result.failed_hosts.keys())),
                )
        except Exception as err:
            self.logger.info("%s", err)
            raise


jobs = [ConnectivityCheckTask, DebugInventoryJob]

register_jobs(*jobs)
