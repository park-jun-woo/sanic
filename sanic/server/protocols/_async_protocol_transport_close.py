# ff:func feature=server type=handler control=sequence
# ff:what Async close checker for protocol transport cleanup

from __future__ import annotations

import asyncio

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sanic.server.protocols.sanic_protocol import SanicProtocol


def _async_protocol_transport_close(
    protocol: SanicProtocol,
    loop: asyncio.AbstractEventLoop,
    timeout: float,
):
    """
    This function is scheduled to be called after close() is called.
    It checks that the transport has shut down properly, or waits
    for any remaining data to be sent, and aborts after a timeout.
    This is required if the transport is closed while there is an async
    large async transport write operation in progress.
    This is observed when NGINX reverse-proxy is the client.
    """
    if protocol.transport is None:
        return
    elif protocol.conn_info is not None and protocol.conn_info.lost:
        protocol.transport = None
        return
    elif not protocol.transport.is_closing():
        raise RuntimeError(
            "You must call transport.close() before "
            "protocol._async_transport_close() runs."
        )

    write_is_paused = not protocol._can_write.is_set()
    try:
        data_left = protocol.transport.get_write_buffer_size()
    except (AttributeError, NotImplementedError):
        data_left = 0
    if write_is_paused or data_left > 0:
        if timeout <= 0:
            loop.call_soon(protocol.abort)
        else:
            next_check_interval = min(timeout, 0.1)
            next_check_timeout = timeout - next_check_interval
            loop.call_later(
                next_check_interval,
                _async_protocol_transport_close,
                protocol,
                loop,
                next_check_timeout,
            )
    else:
        loop.call_soon(protocol.abort)
