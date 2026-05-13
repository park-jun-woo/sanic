# ff:type feature=model type=protocol
# ff:what Extended base transport protocol with ASGI scope and HTTP version

from __future__ import annotations

from asyncio import BaseTransport
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sanic.http.constants import HTTP
    from sanic.models.asgi import ASGIScope


class TransportProtocol(BaseTransport):
    scope: ASGIScope
    version: HTTP
    __slots__ = ()
