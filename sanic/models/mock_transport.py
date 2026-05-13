# ff:type feature=asgi type=protocol
# ff:what Mock transport for ASGI providing scope, send/receive, and websocket

from __future__ import annotations

import asyncio

from sanic.exceptions import BadRequest
from sanic.models.mock_protocol import MockProtocol
from sanic.models.protocol_types import TransportProtocol
from sanic.server.websockets.connection import WebSocketConnection

ASGIScope = dict
ASGIMessage = dict
ASGISend = object
ASGIReceive = object


class MockTransport(TransportProtocol):  # no cov
    _protocol: MockProtocol | None

    def __init__(self, scope, receive, send) -> None:
        self.scope = scope
        self._receive = receive
        self._send = send
        self._protocol = None
        self.loop: asyncio.AbstractEventLoop | None = None

    def get_protocol(self) -> MockProtocol:  # type: ignore
        if not self._protocol:
            self._protocol = MockProtocol(self, self.loop)
        return self._protocol

    def get_extra_info(self, info: str, default=None) -> str | bool | None:
        if info == "peername":
            return self.scope.get("client")
        elif info == "sslcontext":
            return self.scope.get("scheme") in ["https", "wss"]
        return default

    def get_websocket_connection(self) -> WebSocketConnection:
        try:
            return self._websocket_connection
        except AttributeError:
            raise BadRequest("Improper websocket connection.")

    def create_websocket_connection(
        self, send, receive
    ) -> WebSocketConnection:
        self._websocket_connection = WebSocketConnection(
            send, receive, self.scope.get("subprotocols", [])
        )
        return self._websocket_connection

    def add_task(self) -> None:
        raise NotImplementedError

    async def send(self, data) -> None:
        # TODO:
        # - Validation on data and that it is formatted properly and is valid
        await self._send(data)

    async def receive(self):
        return await self._receive()
