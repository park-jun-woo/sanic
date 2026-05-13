# ff:type feature=http type=protocol
# ff:what HTTP/3 transport wrapper providing extra info access for QUIC connect
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from sanic.models.protocol_types import TransportProtocol

if TYPE_CHECKING:
    from sanic.server.protocols.http_protocol import Http3Protocol


class HTTP3Transport(TransportProtocol):
    """HTTP/3 transport implementation."""

    __slots__ = ("_protocol",)

    def __init__(self, protocol: Http3Protocol):
        self._protocol = protocol

    def get_protocol(self) -> Http3Protocol:
        return self._protocol

    def get_extra_info(self, info: str, default: Any = None) -> Any:
        if (
            info in ("socket", "sockname", "peername")
            and self._protocol._transport
        ):
            return self._protocol._transport.get_extra_info(info, default)
        elif info == "network_paths":
            return self._protocol._quic._network_paths
        elif info == "ssl_context":
            return self._protocol.app.state.ssl
        return default
