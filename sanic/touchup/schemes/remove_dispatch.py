# ff:type feature=touchup type=model
# ff:what AST node transformer that removes dispatch calls for unregistered sig

from ast import Attribute, Await, Expr, NodeTransformer
from typing import Any

from sanic.log import logger


class RemoveDispatch(NodeTransformer):
    def __init__(self, registered_events) -> None:
        self._registered_events = registered_events

    def visit_Expr(self, node: Expr) -> Any:
        call = node.value
        if isinstance(call, Await):
            call = call.value

        func = getattr(call, "func", None)
        args = getattr(call, "args", None)
        if not func or not args:
            return node

        if isinstance(func, Attribute) and func.attr == "dispatch":
            event = args[0]
            event_name = getattr(event, "value", None)
            if event_name and self._not_registered(event_name):
                logger.debug(
                    f"Disabling event: {event_name}",
                    extra={"verbosity": 2},
                )
                return None
        return node

    def _not_registered(self, event_name):
        dynamic = []
        for event in self._registered_events:
            if event.endswith(">"):
                namespace_concern, _ = event.rsplit(".", 1)
                dynamic.append(namespace_concern)

        namespace_concern, _ = event_name.rsplit(".", 1)
        return (
            event_name not in self._registered_events
            and namespace_concern not in dynamic
        )
