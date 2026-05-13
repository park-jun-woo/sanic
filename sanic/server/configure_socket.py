# ff:func feature=server type=config control=sequence
# ff:what Create or configure a listening socket based on server settings
from __future__ import annotations

import socket

from pathlib import Path
from typing import Any

from sanic.http.constants import HTTP
from sanic.server.bind_socket import bind_socket
from sanic.server.bind_unix_socket import bind_unix_socket


def configure_socket(
    server_settings: dict[str, Any],
) -> socket.SocketType | None:
    # Create a listening socket or use the one in settings
    if server_settings.get("version") is HTTP.VERSION_3:
        return None
    sock = server_settings.get("sock")
    unix = server_settings["unix"]
    backlog = server_settings["backlog"]
    if unix:
        unix = Path(unix).absolute()
        sock = bind_unix_socket(unix, backlog=backlog)
        server_settings["unix"] = unix
    if sock is None:
        sock = bind_socket(
            server_settings["host"],
            server_settings["port"],
            backlog=backlog,
        )
        sock.set_inheritable(True)
        server_settings["sock"] = sock
        server_settings["host"] = None
        server_settings["port"] = None
    return sock
