from celery import signature
from celery.result import AsyncResult  # Import AsyncResult
from celery.utils.nodenames import gethostname
from nautobot.core.celery import app

# from celery_tasks import app  # import the celery app
from nornir.core.task import AggregatedResult, MultiResult, Result


class CeleryTaskRunner:
    """Celery Queue Runner for Nornir Tasks."""

    def __init__(self) -> None:
        pass

    def run(self, task, hosts, **kwargs):
        multi_result = MultiResult(task.name)
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
            async_result = AsyncResult(task_id, app=app)  # create a new AsyncResult object from the task id.
            try:
                result_data = async_result.get()  # get the result from the backend.
                result = Result(host="self.inventory.hosts[hostname]", result=result_data)
                multi_result.append(result)
            except Exception as e:
                result = Result(
                    host="self.inventory.hosts[hostname]", result=f"Error retrieving result: {e}", failed=True
                )
                multi_result.append(result)

        return AggregatedResult(task.name, kwargs=multi_result)

    # def run(self, task: Task, hosts: List[Host]) -> AggregatedResult:
    #     print("Running task in Celery")
    #     # print(f"Task: {task}")
    #     # print(f"Hosts: {hosts}")
    #     # print(type(task))
    #     # print(dir(task))
    #     result = AggregatedResult(task.name)
    #     for host in hosts:
    #         sig = signature(
    #             "nautobot_plugin_nornir.jobs.run_nornir_packaged_task",
    #             args=(task.name, dict(host)),
    #             kwargs={},
    #             routing_key="default",
    #             hostname=gethostname(),
    #         ).delay()
    #         print(sig)
    #         result[host.name] = sig.id
    #     print(result)

    # print(type(result))
    # print(dir(result))
    # return dict(result)

    # def run(self, task: Task, hosts: List[Host]) -> AggregatedResult:
    #     print("Running task in Celery")
    #     print(f"Task: {task}")
    #     print(f"Hosts: {hosts}")
    #     result = AggregatedResult(task.name)
    #     # group_of_tasks = [signature(task.copy().start(host)) for host in hosts]
    #     for host in hosts:
    #         sig = signature(
    #             "nautobot_plugin_nornir.jobs.run_nornir_packaged_task",
    #             args=(task, dict(host)),
    #             kwargs={},
    #             routing_key="default",
    #             hostname=gethostname(),
    #         ).delay()
    #         print(f"Signature: {sig}")
    #         result[host.name] = sig.id
    #     # group_of_tasks = [
    #     #     signature(
    #     #         "nautobot_plugin_nornir.jobs.run_nornir_packaged_task",
    #     #         args=(dict(host),),
    #     #         kwargs={},
    #     #         routing_key="default",
    #     #         hostname=gethostname(),
    #     #     )
    #     #     for host in hosts
    #     # ]
    #     celery_group = group(group_of_tasks)
    #     group_tasks = celery_group.apply_async()
    #     while not group_tasks.ready():
    #         print("Waiting for results")
    #         print(group_tasks.ready())
    #         time.sleep(1)
    #     print("Group results are ready")
    #     group_result = group_tasks.results
    #     # <class 'celery.result.AsyncResult'>
    #     for index, host in enumerate(hosts):
    #         mr = task.copy().start(host)
    #         print(mr)  # <class 'nornir.core.task.MultiResult'>
    #         result[host.name] = mr.namegroup_result[index].id
    #     return result


# ['TimeoutError', 'class', 'copy', 'del', 'delattr', 'dict', 'dir', 'doc',
# 'eq', 'format', 'ge', 'getattribute', 'getstate', 'gt', 'hash', 'init',
# 'init_subclass', 'le', 'lt', 'module', 'ne', 'new', 'reduce', 'reduce_args',
# 'reduce_ex', 'repr', 'setattr', 'sizeof', 'str', 'subclasshook', 'weakref',
# '_cache', '_get_task_meta', '_ignored', '_iter_meta', '_maybe_reraise_parent_error',
# '_maybe_set_cache', '_on_fulfilled', '_parents', '_set_cache', '_to_remote_traceback',
# 'app', 'args', 'as_list', 'as_tuple', 'backend', 'build_graph', 'children', 'collect',
# 'date_done', 'failed', 'forget', 'get', 'get_leaf', 'graph', 'id', 'ignored', 'info',
# 'iterdeps', 'kwargs', 'maybe_reraise', 'maybe_throw', 'name', 'on_ready', 'parent',
# 'queue', 'ready', 'result', 'retries', 'revoke', 'revoke_by_stamped_headers', 'state',
#  'status', 'successful', 'supports_native_join', 'task_id', 'then', 'throw', 'traceback',
# 'wait', 'worker']
