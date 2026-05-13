# ff:func feature=server type=runner control=sequence
# ff:what Set up and run an HTTP/3 server using QUIC protocol with session tick
from __future__ import annotations

import os

from functools import partial

from sanic.exceptions import ServerError
from sanic.http.http3 import SessionTicketStore, get_config
from sanic.http.tls import get_ssl_context
from sanic.log import server_logger
from sanic.server._run_server_forever import _run_server_forever
from sanic.server._setup_system_signals import _setup_system_signals
from sanic.server.async_server import AsyncioServer
from sanic.server.protocols.http_protocol import Http3Protocol

try:
    from aioquic.asyncio import serve as quic_serve

    HTTP3_AVAILABLE = True
except ModuleNotFoundError:  # no cov
    HTTP3_AVAILABLE = False


def _serve_http_3(
    host,
    port,
    app,
    loop,
    ssl,
    register_sys_signals: bool = True,
    run_multiple: bool = False,
):
    if not HTTP3_AVAILABLE:
        raise ServerError(
            "Cannot run HTTP/3 server without aioquic installed. "
        )
    pid = os.getpid()
    server_logger.info("Starting worker [%s]", pid)
    protocol = partial(Http3Protocol, app=app)
    ticket_store = SessionTicketStore()
    ssl_context = get_ssl_context(app, ssl)
    config = get_config(app, ssl_context)
    coro = quic_serve(
        host,
        port,
        configuration=config,
        create_protocol=protocol,
        session_ticket_fetcher=ticket_store.pop,
        session_ticket_handler=ticket_store.add,
    )
    server = AsyncioServer(app, loop, coro, [])
    loop.run_until_complete(server.startup())
    loop.run_until_complete(server.before_start())
    app.ack()
    loop.run_until_complete(server)
    _setup_system_signals(app, run_multiple, register_sys_signals, loop)
    loop.run_until_complete(server.after_start())

    # TODO: Create connection cleanup and graceful shutdown
    cleanup = None
    _run_server_forever(
        loop, server.before_stop, server.after_stop, cleanup, None, pid
    )
