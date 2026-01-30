"""Jobs for nautobot-plugin-nornir debugging."""

from datetime import datetime

import yaml
from nautobot.apps.jobs import MultiObjectVar, register_jobs

# from nautobot.dcim.filters import DeviceFilterSet
from nautobot.dcim.models import Device  # , DeviceType, Location, Manufacturer, Platform, Rack, RackGroup

# from nautobot.extras.models import Role, Status, Tag
# from nautobot.tenancy.models import Tenant, TenantGroup
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister

# from nornir_nautobot.exceptions import NornirNautobotException
from nornir_nautobot.plugins.tasks.dispatcher import dispatcher

from nautobot_plugin_nornir.constants import NORNIR_SETTINGS
from nautobot_plugin_nornir.contrib.jobs import NornirBaseJob
from nautobot_plugin_nornir.logger import NornirLogger
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory
from nautobot_plugin_nornir.plugins.processors.processor import ProcessNornirResults

InventoryPluginRegister.register("nautobot-inventory", NautobotORMInventory)


class DebugInventoryJob(NornirBaseJob):
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
        qs = self.get_device_queryset(data=kwargs)
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


class ConnectivityCheckTask(NornirBaseJob):  # pylint: disable=too-many-instance-attributes
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
        qs = self.get_device_queryset(data=kwargs)
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
