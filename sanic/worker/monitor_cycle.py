# ff:type feature=worker type=constant
# ff:what Worker monitor loop control enum (BREAK, CONTINUE)

from enum import IntEnum, auto


class MonitorCycle(IntEnum):
    BREAK = auto()
    CONTINUE = auto()
