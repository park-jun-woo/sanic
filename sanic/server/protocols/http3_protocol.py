# ff:type feature=server type=protocol
# ff:what HTTP/3 QUIC protocol implementation handling QUIC events and H3 conne
from __future__ import annotations

from typing import TYPE_CHECKING

from sanic.http.constants import HTTP
from sanic.http.http3 import Http3
from sanic.server.protocols.http_protocol_mixin import HttpProtocolMixin

if TYPE_CHECKING:
    from sanic.app import Sanic

from sanic.log import Colors, logger

ConnectionProtocol = type("ConnectionProtocol", (), {})
try:
    from aioquic.asyncio import QuicConnectionProtocol
    from aioquic.h3.connection import H3_ALPN, H3Connection
    from aioquic.quic.events import (
        DatagramFrameReceived,
        ProtocolNegotiated,
        QuicEvent,
    )

    ConnectionProtocol = QuicConnectionProtocol
except ModuleNotFoundError:  # no cov
    ...


class Http3Protocol(HttpProtocolMixin, ConnectionProtocol):  # type: ignore
    HTTP_CLASS = Http3
    __version__ = HTTP.VERSION_3

    def __init__(self, *args, app: Sanic, **kwargs) -> None:
        self.app = app
        super().__init__(*args, **kwargs)
        self._setup()
        self._connection: H3Connection | None = None

    def quic_event_received(self, event: QuicEvent) -> None:
        logger.debug(
            f"{Colors.BLUE}[quic_event_received]: "
            f"{Colors.PURPLE}{event}{Colors.END}",
            extra={"verbosity": 2},
        )
        if isinstance(event, ProtocolNegotiated):
            self._setup_connection(transmit=self.transmit)
            if event.alpn_protocol in H3_ALPN:
                self._connection = H3Connection(
                    self._quic, enable_webtransport=True
                )
        elif isinstance(event, DatagramFrameReceived):
            if event.data == b"quack":
                self._quic.send_datagram_frame(b"quack-ack")

        #  pass event to the HTTP layer
        if self._connection is not None:
            for http_event in self._connection.handle_event(event):
                self._http.http_event_received(http_event)

    @property
    def connection(self) -> H3Connection | None:
        return self._connection
