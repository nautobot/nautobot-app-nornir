"""Processor used by nornir plays to catch unknown errors."""

from nornir.core.inventory import Host
from nornir.core.task import MultiResult, Task
from nornir_nautobot.exceptions import NornirNautobotException
from nornir_nautobot.plugins.processors import BaseLoggingProcessor


class NautobotAppNornirProcessor(BaseLoggingProcessor):
    """Processor class for Nautobot App Nornir."""

    def __init__(self, logger):
        """Set logging facility."""
        self.logger = logger

    def task_instance_started(self, task: Task, host: Host) -> None:
        """Processor for Logging on Task Start."""
        self.logger.info(f"Starting {task.name}.", extra={"object": task.host.data["obj"]})

    def subtask_instance_started(self, task: Task, host: Host) -> None:
        """Processor for Logging on SubTask Start."""
        self.logger.info(f"Subtask starting {task.name}.", extra={"object": task.host.data["obj"]})

    def task_instance_completed(self, task: Task, host: Host, result: MultiResult) -> None:
        """Nornir processor task completion for Nautobot App Nornir.

        Args:
            task (Task): Nornir task individual object
            host (Host): Host object with Nornir
            result (MultiResult): Result from Nornir task

        Returns:
            None
        """
        # Complex logic to see if the task exception is expected, which is depicted by
        # a sub task raising a NornirNautobotException.
        if result.failed:
            for level_1_result in result:
                if hasattr(level_1_result, "exception") and hasattr(level_1_result.exception, "result"):
                    for level_2_result in level_1_result.exception.result:
                        if isinstance(level_2_result.exception, NornirNautobotException):
                            return
            self.logger.critical(f"{task.name} failed: {result.exception}", extra={"object": task.host.data["obj"]})
        else:
            self.logger.info(
                f"Task Name: {task.name} Task Result: {result.result}", extra={"object": task.host.data["obj"]}
            )

    def subtask_instance_completed(self, task: Task, host: Host, result: MultiResult) -> None:
        """Processor for Logging on SubTask Completed."""
        self.logger.info(f"Subtask completed {task.name}.", extra={"object": task.host.data["obj"]})
