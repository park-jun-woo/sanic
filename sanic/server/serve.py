# ff:func feature=server type=runner control=sequence
# ff:what Start asynchronous HTTP server dispatching to HTTP/1 or HTTP/3 handle
from __future__ import annotations

import asyncio
import sys

from ssl import SSLContext
from typing import TYPE_CHECKING

from sanic.http.constants import HTTP
from sanic.logging.setup import setup_logging
from sanic.models.server_types import Signal
from sanic.server.protocols.http_protocol import HttpProtocol

if TYPE_CHECKING:
    import socket

    from sanic.app import Sanic


def serve(
    host,
    port,
    app: Sanic,
    ssl: SSLContext | None = None,
    sock: socket.socket | None = None,
    unix: str | None = None,
    reuse_port: bool = False,
    loop=None,
    protocol: type[asyncio.Protocol] = HttpProtocol,
    backlog: int = 100,
    register_sys_signals: bool = True,
    run_multiple: bool = False,
    run_async: bool = False,
    connections=None,
    signal=Signal(),
    state=None,
    asyncio_server_kwargs=None,
    version=HTTP.VERSION_1,
):
    """Start asynchronous HTTP Server on an individual process.

    Args:
        host (str): Address to host on
        port (int): Port to host on
        app (Sanic): Sanic app instance
        ssl (Optional[SSLContext], optional): SSLContext. Defaults to `None`.
        sock (Optional[socket.socket], optional): Socket for the server to
            accept connections from. Defaults to `None`.
        unix (Optional[str], optional): Unix socket to listen on instead of
            TCP port. Defaults to `None`.
        reuse_port (bool, optional): `True` for multiple workers. Defaults
            to `False`.
        loop: asyncio compatible event loop. Defaults
            to `None`.
        protocol (Type[asyncio.Protocol], optional): Protocol to use. Defaults
            to `HttpProtocol`.
        backlog (int, optional): The maximum number of queued connections
            passed to socket.listen(). Defaults to `100`.
        register_sys_signals (bool, optional): Register SIGINT and SIGTERM.
            Defaults to `True`.
        run_multiple (bool, optional): Run multiple workers. Defaults
            to `False`.
        run_async (bool, optional): Return an AsyncServer object.
            Defaults to `False`.
        connections: Connections. Defaults to `None`.
        signal (Signal, optional): Signal. Defaults to `Signal()`.
        state: State. Defaults to `None`.
        asyncio_server_kwargs (Optional[Dict[str, Union[int, float]]], optional):
            key-value args for asyncio/uvloop create_server method. Defaults
            to `None`.
        version (str, optional): HTTP version. Defaults to `HTTP.VERSION_1`.

    Raises:
        ServerError: Cannot run HTTP/3 server without aioquic installed.

    Returns:
        AsyncioServer: AsyncioServer object if `run_async` is `True`.
    """  # noqa: E501
    if not run_async and not loop:
        # create new event_loop after fork
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    setup_logging(app.debug, app.config.NO_COLOR, app.config.LOG_EXTRA)

    if app.debug:
        loop.set_debug(app.debug)

    app.asgi = False

    _runners = sys.modules.get("sanic.server.runners")

    if version is HTTP.VERSION_3:
        from sanic.server._serve_http_3 import (
            _serve_http_3 as _default_serve_http_3,
        )

        _serve_http_3 = (
            getattr(_runners, "_serve_http_3", _default_serve_http_3)
            if _runners
            else _default_serve_http_3
        )
        return _serve_http_3(host, port, app, loop, ssl)

    from sanic.server._serve_http_1 import (
        _serve_http_1 as _default_serve_http_1,
    )

    _serve_http_1 = (
        getattr(_runners, "_serve_http_1", _default_serve_http_1)
        if _runners
        else _default_serve_http_1
    )
    return _serve_http_1(
        host,
        port,
        app,
        ssl,
        sock,
        unix,
        reuse_port,
        loop,
        protocol,
        backlog,
        register_sys_signals,
        run_multiple,
        run_async,
        connections,
        signal,
        state,
        asyncio_server_kwargs,
    )
