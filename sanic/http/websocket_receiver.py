# ff:type feature=websocket type=handler
# ff:what Placeholder WebSocket receiver for HTTP/3 WebSocket connections
from sanic.http.receiver import Receiver


class WebsocketReceiver(Receiver):  # noqa
    """Websocket receiver implementation."""

    async def run(self): ...
