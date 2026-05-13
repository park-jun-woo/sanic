# ff:type feature=model type=protocol
# ff:what Protocol defining content range properties for partial HTTP responses

from __future__ import annotations

from typing import Protocol


class Range(Protocol):
    start: int | None
    end: int | None
    size: int | None
    total: int | None
    __slots__ = ()
