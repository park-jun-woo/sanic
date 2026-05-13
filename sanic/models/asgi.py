from collections.abc import Awaitable, MutableMapping
from typing import Any, Callable

from sanic.models.mock_protocol import MockProtocol
from sanic.models.mock_transport import MockTransport

ASGIScope = MutableMapping[str, Any]
ASGIMessage = MutableMapping[str, Any]
ASGISend = Callable[[ASGIMessage], Awaitable[None]]
ASGIReceive = Callable[[], Awaitable[ASGIMessage]]


__all__ = (
    "ASGIScope",
    "ASGIMessage",
    "ASGISend",
    "ASGIReceive",
    "MockProtocol",
    "MockTransport",
)
