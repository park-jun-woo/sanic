# ff:type feature=http type=handler
# ff:what HTTP/3 event dispatcher managing receivers and request creation for Q
from __future__ import annotations

import asyncio

from typing import TYPE_CHECKING, Callable, cast

from sanic.compat import Header
from sanic.exceptions import BadRequest
from sanic.http.http3_transport import HTTP3Transport
from sanic.http.http_receiver import HTTPReceiver
from sanic.http.receiver import Receiver
from sanic.log import Colors, logger
from sanic.models.server_types import ConnInfo

try:
    from aioquic.h3.events import (
        DatagramReceived,
        DataReceived,
        H3Event,
        HeadersReceived,
        WebTransportStreamDataReceived,
    )

    HTTP3_AVAILABLE = True
except ModuleNotFoundError:  # no cov
    HTTP3_AVAILABLE = False

if TYPE_CHECKING:
    from sanic.request import Request
    from sanic.server.protocols.http_protocol import Http3Protocol


class Http3:
    """Internal helper for managing the HTTP/3 request/response cycle"""

    if HTTP3_AVAILABLE:
        HANDLER_PROPERTY_MAPPING = {
            DataReceived: "stream_id",
            HeadersReceived: "stream_id",
            DatagramReceived: "flow_id",
            WebTransportStreamDataReceived: "session_id",
        }

    def __init__(
        self,
        protocol: Http3Protocol,
        transmit: Callable[[], None],
    ) -> None:
        self.protocol = protocol
        self.transmit = transmit
        self.receivers: dict[int, Receiver] = {}

    def http_event_received(self, event: H3Event) -> None:
        logger.debug(  # no cov
            f"{Colors.BLUE}[http_event_received]: "
            f"{Colors.YELLOW}{event}{Colors.END}",
            extra={"verbosity": 2},
        )
        receiver, created_new = self.get_or_make_receiver(event)
        receiver = cast(HTTPReceiver, receiver)

        if isinstance(event, HeadersReceived) and created_new:
            receiver.future = asyncio.ensure_future(receiver.run())
        elif isinstance(event, DataReceived):
            try:
                receiver.receive_body(event.data)
            except Exception as e:
                receiver.future.cancel()
                receiver.future = asyncio.ensure_future(receiver.run(e))
        else:
            ...  # Intentionally here to help out Touchup
            logger.debug(  # no cov
                f"{Colors.RED}DOING NOTHING{Colors.END}",
                extra={"verbosity": 2},
            )

    def get_or_make_receiver(self, event: H3Event) -> tuple[Receiver, bool]:
        if (
            isinstance(event, HeadersReceived)
            and event.stream_id not in self.receivers
        ):
            request = self._make_request(event)
            receiver = HTTPReceiver(self.transmit, self.protocol, request)
            request.stream = receiver

            self.receivers[event.stream_id] = receiver
            return receiver, True
        else:
            ident = getattr(event, self.HANDLER_PROPERTY_MAPPING[type(event)])
            return self.receivers[ident], False

    def get_receiver_by_stream_id(self, stream_id: int) -> Receiver:
        return self.receivers[stream_id]

    def _make_request(self, event: HeadersReceived) -> Request:
        try:
            headers = Header(
                (
                    (k.decode("ASCII"), v.decode(errors="surrogateescape"))
                    for k, v in event.headers
                )
            )
        except UnicodeDecodeError:
            raise BadRequest(
                "Header names may only contain US-ASCII characters."
            )
        method = headers[":method"]
        path = headers[":path"]
        scheme = headers.pop(":scheme", "")
        authority = headers.pop(":authority", "")

        if authority:
            headers["host"] = authority

        try:
            url_bytes = path.encode("ASCII")
        except UnicodeEncodeError:
            raise BadRequest("URL may only contain US-ASCII characters.")

        transport = HTTP3Transport(self.protocol)
        request = self.protocol.request_class(
            url_bytes,
            headers,
            "3",
            method,
            transport,
            self.protocol.app,
            b"",
        )
        request.conn_info = ConnInfo(transport)
        request._stream_id = event.stream_id
        request._scheme = scheme

        return request
