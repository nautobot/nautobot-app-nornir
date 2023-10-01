"""Utility function for the plugin."""


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
