"""Utility function for the plugin."""

from typing import Any

from nautobot_plugin_nornir.error_codes import ERROR_CODES


def verify_setting(obj, dotted_dictionary, message):
    """Helper function to ensure known problematic settings never happen."""
    keys = dotted_dictionary.split(".")

    current_obj = obj
    for key in keys:
        if key in current_obj:
            current_obj = current_obj[key]
        else:
            return

    raise ValueError(message)


def get_error_message(error_code: str, **kwargs: Any) -> str:
    """Get the error message for a given error code.

    Args:
        error_code (str): The error code.
        **kwargs: Any additional context data to be interpolated in the error message.

    Returns:
        str: The constructed error message.
    """
    try:
        error_message = ERROR_CODES.get(error_code, ERROR_CODES["E2XXX"]).error_message.format(**kwargs)
    except KeyError as missing_kwarg:
        error_message = f"Error Code was found, but failed to format, message expected kwarg `{missing_kwarg}`."
    except Exception:  # pylint: disable=broad-except
        error_message = "Error Code was found, but failed to format message, unknown cause."
    return f"{error_code}: {error_message}"
