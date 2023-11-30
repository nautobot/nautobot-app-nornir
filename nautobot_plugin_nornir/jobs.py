from datetime import datetime

from django.db.models import Q
from nautobot.core.celery import register_jobs
from nautobot.dcim.filters import DeviceFilterSet
from nautobot.dcim.models import Device, DeviceType, Location, Manufacturer, Platform, Rack, RackGroup
from nautobot.extras.jobs import Job, MultiObjectVar
from nautobot.extras.models import Status, Tag
from nautobot.tenancy.models import Tenant, TenantGroup
from nautobot_plugin_nornir.constants import NORNIR_SETTINGS
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory
from nautobot_plugin_nornir.utilities.helpers import get_job_filter
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister

InventoryPluginRegister.register("nautobot-inventory", NautobotORMInventory)


class DebugInventoryJob(Job):
    """Job to debug stuff."""
    devices = MultiObjectVar(model=Device, required=False)
    tenant_group = MultiObjectVar(model=TenantGroup, required=False)
    tenant = MultiObjectVar(model=Tenant, required=False)
    location = MultiObjectVar(model=Location, required=False)
    rack_group = MultiObjectVar(model=RackGroup, required=False)
    rack = MultiObjectVar(model=Rack, required=False)
    manufacturer = MultiObjectVar(model=Manufacturer, required=False)
    platform = MultiObjectVar(model=Platform, required=False)
    device_type = MultiObjectVar(model=DeviceType, required=False, display_field="display_name")
    tag = MultiObjectVar(model=Tag, required=False)
    status = MultiObjectVar(model=Status, required=False)

    def run(self, *args, **data):  # pylint: disable=too-many-branches
        """Run config compliance report script."""
        # pylint: disable=unused-argument
        qs = get_job_filter(data)
        # self.log_info("data", data)
        # self.log_info("type of device", type(data['devices']))
        self.logger.info("qs %s", list(qs.values_list('name')))
        query = {}
        query.update({"id": data["devices"].values_list("pk", flat=True)})
        raw_qs = Q()
        base_qs = Device.objects.filter(raw_qs)
        devices_filtered = DeviceFilterSet(data=query, queryset=base_qs)
        try:
            with InitNornir(
                runner=NORNIR_SETTINGS.get("runner"),
                logging={"enabled": False},
                inventory={
                    "plugin": "nautobot-inventory",
                    "options": {
                        "credentials_class": NORNIR_SETTINGS.get("credentials"),
                        "params": NORNIR_SETTINGS.get("inventory_params"),
                        "queryset": devices_filtered.qs,
                        "defaults": {"now": datetime.now()},
                    },
                },
            ) as nornir_obj:
                self.logger.info('defaults: %s', nornir_obj.inventory.defaults)
                self.logger.info('dict: %s', nornir_obj.inventory.dict())
                self.logger.info('groups: %s', nornir_obj.inventory.groups)
                self.logger.info('hosts: %s', nornir_obj.inventory.hosts)

        except Exception as err:
            self.logger.info('%s', err)
            raise


jobs = [DebugInventoryJob]

register_jobs(*jobs)
