# ff:type feature=http type=handler
# ff:what Abstract base receiver for HTTP/3 event handling
from __future__ import annotations

import asyncio

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sanic.request import Request


class Receiver(ABC):
    """HTTP/3 receiver base class."""

    future: asyncio.Future

    def __init__(self, transmit, protocol, request: Request) -> None:
        self.transmit = transmit
        self.protocol = protocol
        self.request = request

    @abstractmethod
    async def run(self):  # no cov
        ...
