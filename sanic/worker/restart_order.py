# ff:type feature=worker type=constant
# ff:what Worker restart order enum (SHUTDOWN_FIRST, STARTUP_FIRST)

from enum import auto

from sanic.compat import UpperStrEnum


class RestartOrder(UpperStrEnum):
    """Available restart orders."""

    SHUTDOWN_FIRST = auto()
    STARTUP_FIRST = auto()
