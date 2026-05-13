# Re-export HTTP protocol classes for backward compatibility
from sanic.server.protocols.http3_protocol import Http3Protocol
from sanic.server.protocols.http_protocol_class import HttpProtocol
from sanic.server.protocols.http_protocol_mixin import HttpProtocolMixin

__all__ = (
    "Http3Protocol",
    "HttpProtocol",
    "HttpProtocolMixin",
)
