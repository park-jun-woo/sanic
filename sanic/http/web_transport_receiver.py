# ff:type feature=http type=handler
# ff:what Placeholder WebTransport receiver for HTTP/3 WebTransport connections
from sanic.http.receiver import Receiver


class WebTransportReceiver(Receiver):  # noqa
    """WebTransport receiver implementation."""

    async def run(self): ...
