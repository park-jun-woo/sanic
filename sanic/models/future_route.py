# ff:type feature=model type=model
# ff:what NamedTuple representing a future route registration with handler, URI

from collections.abc import Iterable
from typing import NamedTuple

from sanic.types import HashableDict


class FutureRoute(NamedTuple):
    handler: str
    uri: str
    methods: Iterable[str] | None
    host: str | list[str]
    strict_slashes: bool
    stream: bool
    version: int | None
    name: str
    ignore_body: bool
    websocket: bool
    subprotocols: list[str] | None
    unquote: bool
    static: bool
    version_prefix: str
    error_format: str | None
    route_context: HashableDict
