# ff:func feature=server type=builder control=sequence
# ff:what Build protocol keyword arguments based on websocket capability detect
from __future__ import annotations

import asyncio

from sanic.config import Config


def _build_protocol_kwargs(
    protocol: type[asyncio.Protocol], config: Config
) -> dict[str, int | float]:
    if hasattr(protocol, "websocket_handshake"):
        return {
            "websocket_max_size": config.WEBSOCKET_MAX_SIZE,
            "websocket_ping_timeout": config.WEBSOCKET_PING_TIMEOUT,
            "websocket_ping_interval": config.WEBSOCKET_PING_INTERVAL,
        }
    return {}
