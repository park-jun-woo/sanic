# ff:type feature=mixin type=model
# ff:what Protocol defining objects that have a name attribute

from __future__ import annotations

from typing import Protocol


class NameProtocol(Protocol):
    name: str
