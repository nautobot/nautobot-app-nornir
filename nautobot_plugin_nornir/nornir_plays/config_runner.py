"""Task for applying configuration to a device."""

import logging
from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware
from nornir import InitNornir
from nornir.core.plugins.inventory import InventoryPluginRegister
from nornir.core.task import Result, Task
from nornir_nautobot.exceptions import NornirNautobotException
from nornir_nautobot.plugins.tasks.dispatcher import dispatcher

from nautobot_plugin_nornir.constants import NORNIR_SETTINGS
from nautobot_plugin_nornir.exceptions import ConfigApplyException
from nautobot_plugin_nornir.logger import NornirLogger
from nautobot_plugin_nornir.nornir_plays.processor import NautobotAppNornirProcessor
from nautobot_plugin_nornir.plugins.inventory.nautobot_orm import NautobotORMInventory

InventoryPluginRegister.register("nautobot-inventory", NautobotORMInventory)


def apply_config(task: Task, logger: logging.Logger, config: str) -> Result:
    """Task to apply configuration to a device."""
    obj = task.host.data["obj"]
    logger.debug(f"Applying config: {config}", extra={"object": obj})
    try:
        task_kwargs = {
            "task": dispatcher,
            "method": "merge_config",
            "logger": logger,
            "obj": obj,
            "framework": "netmiko",
            "name": "APPLY CONFIG",
            "config": config,
        }
        result = task.run(**task_kwargs)[1]
        task_result, task_failed = result.result, result.failed
    except Exception as exc:
        logger.error(f"Error applying config: {config}: {exc}", extra={"object": obj})
        return Result(host=task.host, result=exc, failed=True)
    if task_failed:
        raise ConfigApplyException()
    logger.debug(f"Config apply result: {task_result}")
    return Result(host=task.host, result=task_result)


def config_apply_runner(job, device_qs, config):
    """Nornir play to apply configuration to a device."""
    now = make_aware(datetime.now())
    logger = NornirLogger(job.job_result, job.logger.getEffectiveLevel())

    logger.debug("Starting config apply runner")
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
                "task": apply_config,
                "name": "APPLY CONFIG",
                "logger": logger,
                "config": config,
            }
            results = nr_with_processors.run(**task_kwargs)
    except Exception as error:
        error_msg = f"Error applying config: {config}: {error}"
        logger.error(error_msg)
        raise NornirNautobotException(error_msg) from error

    if results.failed:
        raise ConfigApplyException()
    logger.debug("Completed config apply runner")
    return results
