# Re-export socket functions for backward compatibility
from sanic.server.bind_socket import bind_socket
from sanic.server.bind_unix_socket import bind_unix_socket
from sanic.server.configure_socket import configure_socket
from sanic.server.remove_unix_socket import remove_unix_socket

__all__ = (
    "bind_socket",
    "bind_unix_socket",
    "configure_socket",
    "remove_unix_socket",
)
