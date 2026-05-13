# ff:type feature=model type=model
# ff:what NamedTuple representing a future listener registration with event and

from typing import NamedTuple

from sanic.models.handler_types import ListenerType


class FutureListener(NamedTuple):
    listener: ListenerType
    event: str
    priority: int
