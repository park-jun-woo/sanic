# ff:type feature=core type=model
# ff:what RouteGroup subclass for grouping signal handlers
from __future__ import annotations

from sanic_routing import RouteGroup


class SignalGroup(RouteGroup):
    """A `RouteGroup` that is used to dispatch signals to handlers"""
