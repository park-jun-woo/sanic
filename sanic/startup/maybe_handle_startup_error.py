# ff:func feature=server type=handler control=iteration dimension=1
# ff:what Iterate through registered exception handlers and exit on match, othe

import sys

from sanic.startup._handle_daemon_error import _handle_daemon_error
from sanic.startup._handle_os_error import _handle_os_error
from sanic.startup._handle_server_error import _handle_server_error

EXCEPTION_HANDLERS = (
    _handle_os_error,
    _handle_server_error,
    _handle_daemon_error,
)


def maybe_handle_startup_error(exc: Exception) -> None:
    for handler in EXCEPTION_HANDLERS:
        if handler(exc):
            sys.exit(1)
    raise exc
