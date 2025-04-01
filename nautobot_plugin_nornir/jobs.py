from nautobot.core.celery import nautobot_task
from nornir.core.task import Result


@nautobot_task(soft_time_limit=1800, time_limit=2000)
def hello_world(host) -> Result:
    return Result(host="hostname", result="says hello world!", failed=False)
