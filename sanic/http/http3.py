# Re-export HTTP/3 classes and functions for backward compatibility
from sanic.http.get_config import get_config
from sanic.http.http3_class import Http3
from sanic.http.http3_transport import HTTP3Transport
from sanic.http.http_receiver import HTTPReceiver
from sanic.http.receiver import Receiver
from sanic.http.session_ticket_store import SessionTicketStore
from sanic.http.web_transport_receiver import WebTransportReceiver
from sanic.http.websocket_receiver import WebsocketReceiver

__all__ = (
    "HTTP3Transport",
    "HTTPReceiver",
    "Http3",
    "Receiver",
    "SessionTicketStore",
    "WebTransportReceiver",
    "WebsocketReceiver",
    "get_config",
)
