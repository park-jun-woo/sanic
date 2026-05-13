# ff:type feature=core type=model
# ff:what Route subclass representing a signal dispatch target
from __future__ import annotations

from sanic_routing import Route


class Signal(Route):
    """A `Route` that is used to dispatch signals to handlers"""
