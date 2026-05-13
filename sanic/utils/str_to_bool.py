# ff:func feature=util type=util control=sequence
# ff:what Converts a string to boolean using human-readable truth values

_TRUE_VALUES = {
    "y",
    "yes",
    "yep",
    "yup",
    "t",
    "true",
    "on",
    "enable",
    "enabled",
    "1",
}

_FALSE_VALUES = {
    "n",
    "no",
    "f",
    "nope",
    "false",
    "off",
    "disable",
    "disabled",
    "0",
}


def str_to_bool(val: str) -> bool:
    """Takes string and tries to turn it into bool as human would do.

    If val is in case insensitive (
        "y", "yes", "yep", "yup", "t",
        "true", "on", "enable", "enabled", "1"
    ) returns True.
    If val is in case insensitive (
        "n", "no", "f", "nope", "false", "off", "disable", "disabled", "0"
    ) returns False.
    Else Raise ValueError."""

    val = val.lower()
    if val in _TRUE_VALUES:
        return True
    elif val in _FALSE_VALUES:
        return False
    else:
        raise ValueError(f"Invalid truth value {val}")
