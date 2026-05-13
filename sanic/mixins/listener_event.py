# ff:type feature=mixin type=constant
# ff:what Enum defining lifecycle event names for server listeners

from __future__ import annotations

from enum import Enum, auto


class ListenerEvent(str, Enum):
    def _generate_next_value_(name: str, *args) -> str:  # type: ignore
        return name.lower()

    BEFORE_SERVER_START = "server.init.before"
    AFTER_SERVER_START = "server.init.after"
    BEFORE_SERVER_STOP = "server.shutdown.before"
    AFTER_SERVER_STOP = "server.shutdown.after"
    MAIN_PROCESS_START = auto()
    MAIN_PROCESS_READY = auto()
    MAIN_PROCESS_STOP = auto()
    RELOAD_PROCESS_START = auto()
    RELOAD_PROCESS_STOP = auto()
    BEFORE_RELOAD_TRIGGER = auto()
    AFTER_RELOAD_TRIGGER = auto()
