"""Error codes used in Stacktrace and generated docs."""

from collections import namedtuple

ErrorCode = namedtuple("ErrorCode", ["troubleshooting", "description", "error_message", "recommendation"])

ERROR_CODES = {
    "E2XXX": ErrorCode(
        troubleshooting="Find the error code in the traceback, and search for it in the codebase.",
        description="This means a code snippet was calling get_error_code() with an error code that is not registered.",
        error_message="Un-Registered Error Code used.",
        recommendation="Add the error code to the constants.py file.",
    ),
    "E2001": ErrorCode(
        troubleshooting="""There was no device found in the inventory that matched the query, which includes what you inputted into the form as well what is the dynamic group(s).

        - Please review your dynamic groups and ensure there is devices assigned.
        - If you have any inputs that would further filter, either check them more thoroughly or remove altogether.
        - Ensure that you have a full understanding of the complex query that is being run and implied usage and|or on the query itself.
        """,
        description="No devices were found after initial inventory scoping and form combined for a master filter.",
        error_message="There was no matching results from the query.",
        recommendation="Ensure that you have devices in the inventory that match the query.",
    ),
    "E2002": ErrorCode(
        troubleshooting="The credentials class path is not importable. Review the credentials class path and ensure that it is importable. This must be importable by Django's import_string function, which may not be the same as your local shell environment, depending on how your setup your system.",
        description="The credentials class path is not importable.",
        error_message="A valid credentials class path (as defined by Django's import_string function) is required, but got {credentials_class} which is not importable. See https://github.com/nautobot/nautobot-plugin-nornir#credentials for details.",
        recommendation="Ensure that the credentials class path is importable from the nautobot and worker service.",
    ),
    "E2003": ErrorCode(
        troubleshooting="The device in question is missing the platform attribute. Review the device object and ensure that the platform attribute is set.",
        description="No platform set for the device.",
        error_message="(Platform missing from device {device.name}, preemptively failed.",
        recommendation="In Nautobot, set the platform attribute for the device.",
    ),
    "E2004": ErrorCode(
        troubleshooting="The device in question is using a platform, that is missing the network_driver attribute. Review the platform object and ensure that the network_driver attribute is set.",
        description="The platform object is missing the network_driver attribute.",
        error_message="Platform network_driver missing from device {device.name}, preemptively failed..",
        recommendation="In Nautobot, set the network_driver attribute for the platform.",
    ),
    "E2005": ErrorCode(
        troubleshooting="Review the config context for the specific device that you received thee error on. Ensure that there is the a dictionary key called `nautobot_plugin_nornir`, and a dictionary key within there called `secret_access_type`.",
        description="The device object does not have the expected config context.",
        error_message="Configured to use secrets based on config context, the device {device_obj} does not have any value in `config_context.nautobot_plugin_nornir.secret_access_type`.",
        recommendation="Review then address the config context for the device.",
    ),
    "E2006": ErrorCode(
        troubleshooting="The configuration context for the device should be a string. Review the config context for the specific device that you received the error on.",
        description="The device object does not have the expected config context as a string value.",
        error_message="Configured to use secrets based on config context, the device {device_obj} did not return a string for value {str(access_type_str)}.",
        recommendation="Review then address the config context for the device is in fact a string.",
    ),
}
