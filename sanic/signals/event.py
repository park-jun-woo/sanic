# ff:type feature=core type=constant
# ff:what Enum of all signal event names for the SignalRouter
from __future__ import annotations

from enum import Enum


class Event(Enum):
    """Event names for the SignalRouter"""

    SERVER_EXCEPTION_REPORT = "server.exception.report"
    SERVER_INIT_AFTER = "server.init.after"
    SERVER_INIT_BEFORE = "server.init.before"
    SERVER_SHUTDOWN_AFTER = "server.shutdown.after"
    SERVER_SHUTDOWN_BEFORE = "server.shutdown.before"
    HTTP_LIFECYCLE_BEGIN = "http.lifecycle.begin"
    HTTP_LIFECYCLE_COMPLETE = "http.lifecycle.complete"
    HTTP_LIFECYCLE_EXCEPTION = "http.lifecycle.exception"
    HTTP_LIFECYCLE_HANDLE = "http.lifecycle.handle"
    HTTP_LIFECYCLE_READ_BODY = "http.lifecycle.read_body"
    HTTP_LIFECYCLE_READ_HEAD = "http.lifecycle.read_head"
    HTTP_LIFECYCLE_REQUEST = "http.lifecycle.request"
    HTTP_LIFECYCLE_RESPONSE = "http.lifecycle.response"
    HTTP_ROUTING_AFTER = "http.routing.after"
    HTTP_ROUTING_BEFORE = "http.routing.before"
    HTTP_HANDLER_AFTER = "http.handler.after"
    HTTP_HANDLER_BEFORE = "http.handler.before"
    HTTP_LIFECYCLE_SEND = "http.lifecycle.send"
    HTTP_MIDDLEWARE_AFTER = "http.middleware.after"
    HTTP_MIDDLEWARE_BEFORE = "http.middleware.before"
    WEBSOCKET_HANDLER_AFTER = "websocket.handler.after"
    WEBSOCKET_HANDLER_BEFORE = "websocket.handler.before"
    WEBSOCKET_HANDLER_EXCEPTION = "websocket.handler.exception"


RESERVED_NAMESPACES = {
    "server": (
        Event.SERVER_EXCEPTION_REPORT.value,
        Event.SERVER_INIT_AFTER.value,
        Event.SERVER_INIT_BEFORE.value,
        Event.SERVER_SHUTDOWN_AFTER.value,
        Event.SERVER_SHUTDOWN_BEFORE.value,
    ),
    "http": (
        Event.HTTP_LIFECYCLE_BEGIN.value,
        Event.HTTP_LIFECYCLE_COMPLETE.value,
        Event.HTTP_LIFECYCLE_EXCEPTION.value,
        Event.HTTP_LIFECYCLE_HANDLE.value,
        Event.HTTP_LIFECYCLE_READ_BODY.value,
        Event.HTTP_LIFECYCLE_READ_HEAD.value,
        Event.HTTP_LIFECYCLE_REQUEST.value,
        Event.HTTP_LIFECYCLE_RESPONSE.value,
        Event.HTTP_ROUTING_AFTER.value,
        Event.HTTP_ROUTING_BEFORE.value,
        Event.HTTP_HANDLER_AFTER.value,
        Event.HTTP_HANDLER_BEFORE.value,
        Event.HTTP_LIFECYCLE_SEND.value,
        Event.HTTP_MIDDLEWARE_AFTER.value,
        Event.HTTP_MIDDLEWARE_BEFORE.value,
    ),
    "websocket": {
        Event.WEBSOCKET_HANDLER_AFTER.value,
        Event.WEBSOCKET_HANDLER_BEFORE.value,
        Event.WEBSOCKET_HANDLER_EXCEPTION.value,
    },
}

GENERIC_SIGNAL_FORMAT = "__generic__.__signal__.%s"
