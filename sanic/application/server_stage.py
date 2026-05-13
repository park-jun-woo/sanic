# ff:type feature=core type=constant
# ff:what Server lifecycle stage enum (STOPPED, PARTIAL, SERVING)

from enum import IntEnum, auto


class ServerStage(IntEnum):
    """Server stages."""

    STOPPED = auto()
    PARTIAL = auto()
    SERVING = auto()
