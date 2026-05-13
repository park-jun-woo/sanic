# ff:func feature=server type=runner control=sequence
# ff:what Set up and run an HTTP/1.1 server with connection management and life
from __future__ import annotations

import asyncio
import os
import socket

from functools import partial

from sanic.application.ext import setup_ext
from sanic.compat import OS_IS_WINDOWS
from sanic.log import error_logger, server_logger
from sanic.server._build_protocol_kwargs import _build_protocol_kwargs
from sanic.server._run_server_forever import _run_server_forever
from sanic.server._setup_system_signals import _setup_system_signals
from sanic.server.async_server import AsyncioServer
from sanic.server.socket import bind_unix_socket


def _serve_http_1(
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
):
    connections = connections if connections is not None else set()
    protocol_kwargs = _build_protocol_kwargs(protocol, app.config)
    server = partial(
        protocol,
        loop=loop,
        connections=connections,
        signal=signal,
        app=app,
        state=state,
        unix=unix,
        **protocol_kwargs,
    )
    asyncio_server_kwargs = (
        asyncio_server_kwargs if asyncio_server_kwargs else {}
    )
    if OS_IS_WINDOWS and sock:
        pid = os.getpid()
        sock = sock.share(pid)
        sock = socket.fromshare(sock)
    # UNIX sockets are always bound by us (to preserve semantics between modes)
    elif unix:
        sock = bind_unix_socket(unix, backlog=backlog)
    server_coroutine = loop.create_server(
        server,
        None if sock else host,
        None if sock else port,
        ssl=ssl,
        reuse_port=reuse_port,
        sock=sock,
        backlog=backlog,
        **asyncio_server_kwargs,
    )

    setup_ext(app)
    if run_async:
        return AsyncioServer(
            app=app,
            loop=loop,
            serve_coro=server_coroutine,
            connections=connections,
        )

    pid = os.getpid()
    server_logger.info("Starting worker [%s]", pid)
    loop.run_until_complete(app._startup())
    loop.run_until_complete(app._server_event("init", "before"))
    app.ack()

    try:
        http_server = loop.run_until_complete(server_coroutine)
    except BaseException:
        error_logger.exception("Unable to start server", exc_info=True)
        return

    def _cleanup():
        # Wait for event loop to finish and all connections to drain
        http_server.close()
        loop.run_until_complete(http_server.wait_closed())

        # Complete all tasks on the loop
        signal.stopped = True
        for connection in connections:
            connection.close_if_idle()

        # Gracefully shutdown timeout.
        # We should provide graceful_shutdown_timeout,
        # instead of letting connection hangs forever.
        # Let's roughly calcucate time.
        graceful = app.config.GRACEFUL_SHUTDOWN_TIMEOUT
        start_shutdown: float = 0
        while connections and (start_shutdown < graceful):
            loop.run_until_complete(asyncio.sleep(0.1))
            start_shutdown = start_shutdown + 0.1

        app.shutdown_tasks(graceful - start_shutdown)

        # Force close non-idle connection after waiting for
        # graceful_shutdown_timeout
        for conn in connections:
            if hasattr(conn, "websocket") and conn.websocket:
                conn.websocket.fail_connection(code=1001)
            else:
                conn.abort()

        try:
            app.set_serving(False)
        except (BrokenPipeError, ConnectionResetError, EOFError):
            pass

    _setup_system_signals(app, run_multiple, register_sys_signals, loop)
    loop.run_until_complete(app._server_event("init", "after"))
    app.set_serving(True)
    _run_server_forever(
        loop,
        partial(app._server_event, "shutdown", "before"),
        partial(app._server_event, "shutdown", "after"),
        _cleanup,
        unix,
        pid,
    )
