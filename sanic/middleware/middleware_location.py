# ff:type feature=middleware type=constant
# ff:what Enum defining middleware execution locations (request or response)
from __future__ import annotations

from enum import IntEnum, auto


class MiddlewareLocation(IntEnum):
    REQUEST = auto()
    RESPONSE = auto()
