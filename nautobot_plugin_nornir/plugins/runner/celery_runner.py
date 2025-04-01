from typing import List

from celery import group, signature
from celery.utils.nodenames import gethostname
from nornir.core.inventory import Host
from nornir.core.task import AggregatedResult, Task


class CeleryTaskRunner:
    """Celery Queue Runner for Nornir Tasks."""

    def __init__(self) -> None:
        pass

    def run(self, task: Task, hosts: List[Host]) -> AggregatedResult:
        print("Running task in Celery")
        print(f"Task: {task}")
        print(f"Hosts: {hosts}")
        # print(dir(hosts[0]))
        result = AggregatedResult(task.name)
        group_of_tasks = [
            signature(
                "nautobot_plugin_nornir.jobs.hello_world",
                args=(dict(host),),
                kwargs={},
                routing_key="default",
                hostname=gethostname(),
            )
            for host in hosts
        ]
        g = group(group_of_tasks)
        res = g()
        # result[host.name] = task.copy().start(host)
        for gr in res.results:
            print(gr.status)
        for host in hosts:
            result[host.name] = gr.result
        return result
