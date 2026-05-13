# ff:type feature=mixin type=model
# ff:what Protocol defining objects that have a __name__ attribute

from __future__ import annotations

from typing import Protocol


class DunderNameProtocol(Protocol):
    __name__: str
