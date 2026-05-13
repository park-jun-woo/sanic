# ff:type feature=core type=constant
# ff:what Server mode enum (PRODUCTION, DEBUG)

from enum import auto

from sanic.application.str_enum import StrEnum


class Mode(StrEnum):
    """Server modes."""

    PRODUCTION = auto()
    DEBUG = auto()
