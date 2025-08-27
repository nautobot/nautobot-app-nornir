"""Task for running commands with prompts."""

import logging
import re
from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir.core.task import Result, Task
from nornir_nautobot.exceptions import NornirNautobotException
from nornir_nautobot.plugins.tasks.dispatcher import dispatcher

from nautobot_plugin_nornir.constants import NORNIR_SETTINGS
from nautobot_plugin_nornir.exceptions import CommandRunnerException
from nautobot_plugin_nornir.logger import NornirLogger
from nautobot_plugin_nornir.nornir_plays.processor import NautobotAppNornirProcessor
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory

InventoryPluginRegister.register("nautobot-inventory", NautobotORMInventory)


def run_command(
    task: Task,
    logger: logging.Logger,
    command: str,
    expected_pattern: str = None,
    prompts: dict[str, str] = None,
    **kwargs,
) -> Result:
    """Run a command and return the result."""
    obj = task.host.data["obj"]
    logger.debug(f"Running command: {command}", extra={"object": obj})
    try:
        task_kwargs = {
            "task": dispatcher,
            "method": "get_command",
            "logger": logger,
            "obj": obj,
            "framework": "netmiko",
            "name": "RUN COMMAND",
            "command": command,
            **kwargs,
        }
        if prompts:
            task_kwargs["method"] = "get_command_with_prompts"
            task_kwargs["prompts"] = prompts
            # Setting netmiko's read_timeout to 0 will wait indefinitely until there are no more lines being read.
            task_kwargs["read_timeout"] = 0
            # Wait for 5 seconds of no change in output before failing.
            task_kwargs["last_read"] = 5.0
        result = task.run(**task_kwargs)[1]
        task_result, task_failed = result.result, result.failed
    except Exception as exc:
        logger.error(f"Error running command: {command}: {exc}", extra={"object": obj})
        return Result(host=task.host, result=exc, failed=True)
    if task_failed:
        raise CommandRunnerException()
    logger.debug(f"Task result: {task_result}")
    if expected_pattern:
        command_output = task_result["output"][command]
        logger.debug(f"Command output: {command_output}")
        if not re.search(expected_pattern, command_output):
            raise CommandRunnerException(f"Pattern {expected_pattern} did not match command output: {command_output}")
    return Result(host=task.host, result=task_result)


def command_runner(
    job,
    device_qs,
    command: str,
    expected_pattern: str = None,
    prompts: dict[str, str] = None,
) -> Result:
    """Nornir play to run a command and optionally verify the output."""
    now = make_aware(datetime.now())
    logger = NornirLogger(job.job_result, job.logger.getEffectiveLevel())

    logger.debug("Starting command runner")
    User = get_user_model()
    job.request.user = User.objects.get(id=job.celery_kwargs["nautobot_job_user_id"])
    try:
        with InitNornir(
            runner=NORNIR_SETTINGS.get("runner"),
            logging={"enabled": False},
            inventory={
                "plugin": "nautobot-inventory",
                "options": {
                    "credentials_class": NORNIR_SETTINGS.get("credentials"),
                    "params": NORNIR_SETTINGS.get("inventory_params"),
                    "queryset": device_qs,
                    "defaults": {"now": now},
                },
            },
        ) as nornir_obj:
            nr_with_processors = nornir_obj.with_processors([NautobotAppNornirProcessor(logger)])
            task_kwargs = {
                "task": run_command,
                "name": "RUN COMMAND",
                "logger": logger,
                "command": command,
                "expected_pattern": expected_pattern,
                "prompts": prompts,
            }
            results = nr_with_processors.run(**task_kwargs)
    except Exception as error:
        error_msg = f"Error running command: {command}: {error}"
        logger.error(error_msg)
        raise NornirNautobotException(error_msg) from error

    if results.failed:
        raise CommandRunnerException()
    logger.debug("Completed command runner")
    return results
