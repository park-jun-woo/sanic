# Re-export runner functions for backward compatibility
from sanic.server._build_protocol_kwargs import _build_protocol_kwargs
from sanic.server._run_server_forever import _run_server_forever
from sanic.server._run_shutdown_coro import _run_shutdown_coro
from sanic.server._serve_http_1 import _serve_http_1
from sanic.server._serve_http_3 import _serve_http_3
from sanic.server._setup_system_signals import _setup_system_signals
from sanic.server.serve import serve
from sanic.server.socket import remove_unix_socket

__all__ = (
    "_build_protocol_kwargs",
    "_run_server_forever",
    "_run_shutdown_coro",
    "_serve_http_1",
    "_serve_http_3",
    "_setup_system_signals",
    "remove_unix_socket",
    "serve",
)
