# Re-export base protocol for backward compatibility
from sanic.server.protocols.sanic_protocol import (
    SanicProtocol,
    _async_protocol_transport_close,
)

__all__ = (
    "SanicProtocol",
    "_async_protocol_transport_close",
)
