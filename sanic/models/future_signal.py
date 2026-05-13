# ff:type feature=model type=model
# ff:what NamedTuple representing a future signal registration with handler, ev

from typing import NamedTuple

from sanic.models.handler_types import SignalHandler


class FutureSignal(NamedTuple):
    handler: SignalHandler
    event: str
    condition: dict[str, str] | None
    exclusive: bool
    priority: int
