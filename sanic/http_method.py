# ff:type feature=core type=constant
# ff:what HTTP method enum constants (GET, POST, PUT, etc.)

from enum import auto

from sanic.compat import UpperStrEnum


class HTTPMethod(UpperStrEnum):
    """HTTP methods that are commonly used."""

    GET = auto()
    POST = auto()
    PUT = auto()
    HEAD = auto()
    OPTIONS = auto()
    PATCH = auto()
    DELETE = auto()
