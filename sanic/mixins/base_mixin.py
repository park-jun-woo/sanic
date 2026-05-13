# ff:type feature=mixin type=mixin
# ff:what Base mixin class providing name generation for handlers and routes

from __future__ import annotations

from sanic.base.meta import SanicMeta
from sanic.mixins.dunder_name_protocol import DunderNameProtocol
from sanic.mixins.name_protocol import NameProtocol


class BaseMixin(metaclass=SanicMeta):
    """Base class for various mixins."""

    name: str
    strict_slashes: bool | None

    def _generate_name(
        self, *objects: NameProtocol | DunderNameProtocol | str
    ) -> str:
        name: str | None = None
        for obj in objects:
            if not obj:
                continue
            if isinstance(obj, str):
                name = obj
            else:
                name = getattr(obj, "name", getattr(obj, "__name__", None))

            if name:
                break
        if not name or not isinstance(name, str):
            raise ValueError("Could not generate a name for handler")

        if not name.startswith(f"{self.name}."):
            name = f"{self.name}.{name}"

        return name

    def generate_name(self, *objects) -> str:
        return self._generate_name(*objects)
