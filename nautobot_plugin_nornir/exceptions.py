"""Nautobot App Nornir Exceptions."""


class NautobotAppNornirException(Exception):
    """Base exception for Nautobot App Nornir."""


class CommandRunnerException(NautobotAppNornirException):
    """Exception for command runner errors."""


class ConfigApplyException(NautobotAppNornirException):
    """Exception for config apply errors."""
