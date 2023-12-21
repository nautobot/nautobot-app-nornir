"""Jobs for nautobot-plugin-nornir debugging."""
from datetime import datetime

from nautobot.core.celery import register_jobs
from nautobot.dcim.models import Device
from nautobot.extras.jobs import Job
from nautobot_plugin_nornir.constants import NORNIR_SETTINGS
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory
from nautobot_plugin_nornir.utilities.helpers import FormEntry, get_job_filter
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister

InventoryPluginRegister.register("nautobot-inventory", NautobotORMInventory)


class DebugInventoryJob(Job, FormEntry):
    """Job to debug stuff."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta object boilerplate for compliance."""

        name = "Debug Nornir Inventory"
        description = "Prints inventory details per host, group, defaults."
        has_sensitive_variables = False
        hidden = True

    def run(self, *args, **data):  # pylint: disable=too-many-branches
        """Run config compliance report script."""
        # pylint: disable=unused-argument
        qs = get_job_filter(data)
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
                for host, data in nornir_obj.inventory.hosts.items():
                    self.logger.info(
                        "#### %s Data\n%s",
                        host,
                        "\n".join(f"{k}: {v}\n" for k, v in data.dict().items()),
                        extra={"object": Device.objects.get(id=data.data["id"])},
                    )
                self.logger.info(
                    "#### Default Data\n%s",
                    nornir_obj.inventory.defaults.data,
                )
                self.logger.info("Total In Scope Devices: %s", len(nornir_obj.inventory.hosts.items()))
        except Exception as err:
            self.logger.info("%s", err)
            raise


jobs = [DebugInventoryJob]

register_jobs(*jobs)
