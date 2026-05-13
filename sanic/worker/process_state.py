# ff:type feature=worker type=constant
# ff:what Worker process lifecycle state enum

from enum import IntEnum, auto


class ProcessState(IntEnum):
    """Process states."""

    NONE = auto()
    IDLE = auto()
    RESTARTING = auto()
    STARTING = auto()
    STARTED = auto()
    ACKED = auto()
    JOINED = auto()
    TERMINATED = auto()
    FAILED = auto()
    COMPLETED = auto()
