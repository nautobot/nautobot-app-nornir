import json

from nautobot.apps.jobs import BooleanVar, Job, ObjectVar, register_jobs
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

# lassnornir.core.task.Task(task: Callable[[...], Any], nornir: Nornir, global_dry_run: bool, processors: Processors, name: str | None = None, severity_level: int = 20, parent_task: Task | None = None, **kwargs: str)


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
    print(f"In hello_world task: {host}")
    result = Result(host=host, result=f"{task} says hello world!", failed=False)
    meh = vars(result)
    meh["host"]["obj"] = meh["host"]["obj"].name
    print(json.dumps(meh))
    return json.dumps(meh)


# {'result': 'hello_world says hello world!', 'host': {'id': '5f4122f3-0f64-4d96-abd7-bad15ab1a1fa', 'type': 'CSR1000v', 'location': 'site-1_09ea', 'role': 'router', 'config_context': {}, 'custom_field_data': {}, 'obj': <SimpleLazyObject: <Device: csr-0>>, 'ansible_driver': 'cisco.ios.ios', 'hier_config_driver': 'ios', 'napalm_driver': 'ios', 'netmiko_driver': 'cisco_ios', 'netutils_parser_driver': 'cisco_ios', 'ntc_templates_driver': 'cisco_ios', 'pyats_driver': 'iosxe', 'pyntc_driver': 'cisco_ios_ssh', 'scrapli_driver': 'cisco_iosxe', 'connection_options': {'napalm': {'extras': {'optional_args': {'global_delay_factor': 1, 'secret': 'cisco'}}, 'platform': 'ios'}, 'netmiko': {'extras': {'global_delay_factor': 1, 'secret': 'cisco'}, 'platform': 'cisco_ios'}, 'scrapli': {'platform': 'cisco_iosxe'}, 'pyntc': {'platform': 'cisco_ios_ssh'}}, 'now': 'now'}, 'changed': False, 'diff': '', 'failed': False, 'exception': None, 'name': None, 'severity_level': 20, 'stdout': None, 'stderr': None}


class NornirFunTask(Job):  # pylint: disable=too-many-instance-attributes
    """Nautobot Job for checking a tcp port is 'opened'."""

    device = ObjectVar(model=Device, required=True)
    debug = BooleanVar(description="Enable for more verbose debug logging")

    class Meta:
        """Meta object for Nornir Learning."""

        name = "Execute Nornir in Celery Runner - Single Device"
        description = "Celery Runner Fun."
        has_sensitive_variables = False

    def run(self, *args, **kwargs):
        """Process tcp_ping task from job."""
        self.logger.info(f"{kwargs['device']}")
        qs = Device.objects.filter(id=kwargs["device"].id)
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
        # print(nr.inventory.hosts)
        agg_result = nr.run(task=hello_world)
        # return agg_result


register_jobs(NornirFunTask)
