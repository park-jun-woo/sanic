# ff:type feature=asgi type=protocol
# ff:what Mock protocol for ASGI transport providing pause/resume writing and d

from __future__ import annotations

import asyncio

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sanic.models.mock_transport import MockTransport


class MockProtocol:  # no cov
    def __init__(self, transport: MockTransport, loop):
        self.transport = transport
        self._not_paused = asyncio.Event()
        self._not_paused.set()
        self._complete = asyncio.Event()

    def pause_writing(self) -> None:
        self._not_paused.clear()

    def resume_writing(self) -> None:
        self._not_paused.set()

    async def complete(self) -> None:
        self._not_paused.set()
        await self.transport.send(
            {"type": "http.response.body", "body": b"", "more_body": False}
        )

    @property
    def is_complete(self) -> bool:
        return self._complete.is_set()

    async def push_data(self, data: bytes) -> None:
        if not self.is_complete:
            await self.transport.send(
                {"type": "http.response.body", "body": data, "more_body": True}
            )

    async def drain(self) -> None:
        await self._not_paused.wait()
