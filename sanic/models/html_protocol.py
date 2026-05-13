# ff:type feature=model type=protocol
# ff:what Protocol for objects that can render themselves as HTML

from __future__ import annotations

from typing import Protocol


class HTMLProtocol(Protocol):
    def __html__(self) -> str | bytes: ...

    def _repr_html_(self) -> str | bytes: ...
