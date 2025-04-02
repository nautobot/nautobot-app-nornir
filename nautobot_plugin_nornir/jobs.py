import json

from nautobot.apps.jobs import BooleanVar, Job, MultiObjectVar, register_jobs
from nautobot.dcim.models import Device
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir.core.plugins.runners import RunnersPluginRegister
from nornir.core.task import Result, Task

from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory
from nautobot_plugin_nornir.plugins.runner.celery_runner import CeleryTaskRunner

InventoryPluginRegister.register("nautobot-inventory", NautobotORMInventory)
RunnersPluginRegister.register("celery-runner", CeleryTaskRunner)

from nautobot.core.celery import nautobot_task

# @nautobot_task(soft_time_limit=1800, time_limit=2000)
# def run_nornir_packaged_task(nornir_task, hosts) -> dict:
#     print(f"Running task: {nornir_task}")
#     print(f"Hosts: {hosts}")
#     task_func = import_string("nautobot_plugin_nornir.jobs.hello_world")
#     print(f"Task Func: {type(task_func)}")
#     # Task(task_func)
#     result = {}
#     for host in hosts:
#         mr = task_func.copy().start(host)
#         result[host.name] = mr
#     return result


@nautobot_task(soft_time_limit=1800, time_limit=2000)
def hello_world(task: Task, host) -> Result:
    result = Result(host=host, result=f"{task} says hello world!", failed=False)
    meh = vars(result)
    meh["host"]["obj"] = meh["host"]["obj"].name
    return json.dumps(meh)


class NornirFunTask(Job):  # pylint: disable=too-many-instance-attributes
    """Nautobot Job for checking a tcp port is 'opened'."""

    device = MultiObjectVar(model=Device, required=True)
    debug = BooleanVar(description="Enable for more verbose debug logging")

    class Meta:
        """Meta object for Nornir Learning."""

        name = "Execute Nornir in Celery Runner - Single Device"
        description = "Celery Runner Fun."
        has_sensitive_variables = False

    def run(self, *args, **kwargs):
        """Process tcp_ping task from job."""
        qs = Device.objects.filter(id__in=[dev.id for dev in kwargs["device"]])
        nr = InitNornir(
            runner={
                "plugin": "celery-runner",
            },
            logging={"enabled": False},
            inventory={
                "plugin": "nautobot-inventory",
                "options": {
                    "credentials_class": "nautobot_plugin_nornir.plugins.credentials.env_vars.CredentialsEnvVars",
                    "queryset": qs,
                    "defaults": {"now": "now"},
                },
            },
        )
        hw = nr.run(task=hello_world)
        for _, result in hw.items():
            print(result[0].result)


register_jobs(NornirFunTask)
