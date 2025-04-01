# from django.utils.module_loading import import_string
# from nautobot.core.celery import nautobot_task

# # lassnornir.core.task.Task(task: Callable[[...], Any], nornir: Nornir, global_dry_run: bool, processors: Processors, name: str | None = None, severity_level: int = 20, parent_task: Task | None = None, **kwargs: str)


# @nautobot_task(soft_time_limit=1800, time_limit=2000)
# def run_nornir_packaged_task(nornir_task, hosts) -> dict:
#     print(f"Running task: {nornir_task}")
#     print(f"Hosts: {hosts}")
#     task_func = import_string("nautobot_plugin_nornir.jobs.hello_world")
#     print(f"Task Func: {type(task_func)}")
#     result = {}
#     for host in hosts:
#         mr = task_func.copy().start(host)
#         result[host.name] = mr
#     return result
