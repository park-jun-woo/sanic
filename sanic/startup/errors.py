from typing import Callable

from sanic.startup._handle_daemon_error import _handle_daemon_error
from sanic.startup._handle_os_error import _handle_os_error
from sanic.startup._handle_server_error import _handle_server_error
from sanic.startup.maybe_handle_startup_error import (
    EXCEPTION_HANDLERS,
    maybe_handle_startup_error,
)

ExceptionHandler = Callable[[Exception], bool]


__all__ = (
    "ExceptionHandler",
    "EXCEPTION_HANDLERS",
    "maybe_handle_startup_error",
    "_handle_os_error",
    "_handle_server_error",
    "_handle_daemon_error",
)
