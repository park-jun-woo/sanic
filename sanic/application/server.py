# ff:type feature=core type=constant
# ff:what Server type enum (SANIC, ASGI)

from enum import auto

from sanic.application.str_enum import StrEnum


class Server(StrEnum):
    """Server types."""

    SANIC = auto()
    ASGI = auto()
