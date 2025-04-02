import json
import time

from celery import signature
from celery.result import AsyncResult
from celery.utils.nodenames import gethostname
from nautobot.core.celery import app
from nornir.core.task import AggregatedResult, MultiResult, Result


class CeleryTaskRunner:
    """Celery Queue Runner for Nornir Tasks."""

    def __init__(self) -> None:
        pass

    def run(self, task, hosts, **kwargs):
        agg_res = AggregatedResult(task.name)
        async_results = {}
        # Dispatch Celery tasks
        for host in hosts:
            async_result = signature(
                "nautobot_plugin_nornir.jobs.hello_world",
                args=(task.name, dict(host)),
                kwargs={},
                routing_key="default",
                hostname=gethostname(),
            ).delay()
            async_results[host.name] = async_result.id  # store the task ID.

        # Retrieve results from the Celery backend
        for hostname, task_id in async_results.items():
            multi_result = MultiResult(task.name)
            async_result = AsyncResult(task_id, app=app)
            while not async_result.ready():
                # wait for the task to complete.
                time.sleep(1)
            try:
                deserialized_result = json.loads(async_result.result)
                result = Result(host=hostname, result=deserialized_result["result"], failed=async_result.failed())
                multi_result.append(result)
            except Exception as e:
                print(f"Error retrieving result for {hostname}: {e}")
            agg_res[hostname] = multi_result

        return agg_res
