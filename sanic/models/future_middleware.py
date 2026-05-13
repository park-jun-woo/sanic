# ff:type feature=model type=model
# ff:what NamedTuple representing a future middleware registration with attach

from typing import NamedTuple

from sanic.models.handler_types import MiddlewareType


class FutureMiddleware(NamedTuple):
    middleware: MiddlewareType
    attach_to: str
