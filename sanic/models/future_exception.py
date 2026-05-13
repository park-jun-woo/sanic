# ff:type feature=model type=model
# ff:what NamedTuple representing a future exception handler registration

from typing import NamedTuple

from sanic.models.handler_types import ErrorMiddlewareType


class FutureException(NamedTuple):
    handler: ErrorMiddlewareType
    exceptions: list[BaseException]
