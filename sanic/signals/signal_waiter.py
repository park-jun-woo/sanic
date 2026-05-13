# ff:type feature=core type=model
# ff:what Dataclass representing a future waiting for a signal dispatch
from __future__ import annotations

import asyncio

from dataclasses import dataclass

from sanic.signals.signal import Signal


@dataclass
class SignalWaiter:
    """A record representing a future waiting for a signal"""

    signal: Signal
    event_definition: str
    trigger: str = ""
    requirements: dict[str, str] | None = None
    exclusive: bool = True

    future: asyncio.Future | None = None

    async def wait(self):
        """Block until the signal is next dispatched.

        Return the context of the signal dispatch, if any.
        """
        loop = asyncio.get_running_loop()
        self.future = loop.create_future()
        self.signal.ctx.waiters.append(self)
        try:
            return await self.future
        finally:
            self.signal.ctx.waiters.remove(self)

    def matches(self, event, condition):
        return (
            (condition is None and not self.exclusive)
            or (condition is None and not self.requirements)
            or condition == self.requirements
        ) and (self.trigger or event == self.event_definition)
