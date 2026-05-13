# ff:type feature=http type=handler
# ff:what HTTP/3 receiver handling request/response cycle with header preparati
from __future__ import annotations

from typing import TYPE_CHECKING

from sanic.exceptions import PayloadTooLarge, ServerError
from sanic.helpers import has_message_body
from sanic.http.constants import Stage
from sanic.http.receiver import Receiver
from sanic.http.stream import Stream
from sanic.log import Colors, logger

if TYPE_CHECKING:
    from sanic.response import BaseHTTPResponse


class HTTPReceiver(Receiver, Stream):
    """HTTP/3 receiver implementation."""

    stage: Stage
    # request inherited from Receiver

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.request_body = None
        self.stage = Stage.IDLE
        self.headers_sent = False
        self.response: BaseHTTPResponse | None = None
        self.request_max_size = self.protocol.request_max_size
        self.request_bytes = 0

    async def run(self, exception: Exception | None = None):
        """Handle the request and response cycle."""
        self.stage = Stage.HANDLER
        self.head_only = self.request.method.upper() == "HEAD"

        if exception:
            logger.info(  # no cov
                f"{Colors.BLUE}[exception]: "
                f"{Colors.RED}{exception}{Colors.END}",
                exc_info=True,
                extra={"verbosity": 1},
            )
            await self.error_response(exception)
        else:
            try:
                logger.info(  # no cov
                    f"{Colors.BLUE}[request]:{Colors.END} {self.request}",
                    extra={"verbosity": 1},
                )
                await self.protocol.request_handler(self.request)
            except Exception as e:  # no cov
                # This should largely be handled within the request handler.
                # But, just in case...
                await self.run(e)
        self.stage = Stage.IDLE

    async def error_response(self, exception: Exception) -> None:
        """Handle response when exception encountered"""
        # From request and handler states we can respond, otherwise be silent
        app = self.protocol.app

        await app.handle_exception(self.request, exception)

    def _prepare_headers(
        self, response: BaseHTTPResponse
    ) -> list[tuple[bytes, bytes]]:
        size = len(response.body) if response.body else 0
        headers = response.headers
        status = response.status

        if not has_message_body(status) and (
            size
            or "content-length" in headers
            or "transfer-encoding" in headers
        ):
            headers.pop("content-length", None)
            headers.pop("transfer-encoding", None)
            logger.warning(  # no cov
                f"Message body set in response on {self.request.path}. "
                f"A {status} response may only have headers, no body."
            )
        elif "content-length" not in headers:
            if size:
                headers["content-length"] = size
            else:
                headers["transfer-encoding"] = "chunked"

        headers = [
            (b":status", str(response.status).encode()),
            *response.processed_headers,
        ]
        return headers

    def send_headers(self) -> None:
        """Send response headers to client"""
        logger.debug(  # no cov
            f"{Colors.BLUE}[send]: {Colors.GREEN}HEADERS{Colors.END}",
            extra={"verbosity": 2},
        )
        if not self.response:
            raise RuntimeError("no response")

        response = self.response
        headers = self._prepare_headers(response)

        self.protocol.connection.send_headers(
            stream_id=self.request.stream_id,
            headers=headers,
        )
        self.headers_sent = True
        self.stage = Stage.RESPONSE

        if self.response.body and not self.head_only:
            self._send(self.response.body, False)
        elif self.head_only:
            self.future.cancel()

    def respond(self, response: BaseHTTPResponse) -> BaseHTTPResponse:
        """Prepare response to client"""
        logger.debug(  # no cov
            f"{Colors.BLUE}[respond]:{Colors.END} {response}",
            extra={"verbosity": 2},
        )

        if self.stage is not Stage.HANDLER:
            self.stage = Stage.FAILED
            raise RuntimeError("Response already started")

        # Disconnect any earlier but unused response object
        if self.response is not None:
            self.response.stream = None

        self.response, response.stream = response, self

        return response

    def receive_body(self, data: bytes) -> None:
        """Receive request body from client"""
        self.request_bytes += len(data)
        if self.request_bytes > self.request_max_size:
            raise PayloadTooLarge("Request body exceeds the size limit")

        self.request.body += data

    async def send(self, data: bytes, end_stream: bool) -> None:
        """Send data to client"""
        logger.debug(  # no cov
            f"{Colors.BLUE}[send]: {Colors.GREEN}data={data.decode()} "
            f"end_stream={end_stream}{Colors.END}",
            extra={"verbosity": 2},
        )
        self._send(data, end_stream)

    def _send(self, data: bytes, end_stream: bool) -> None:
        if not self.headers_sent:
            self.send_headers()
        if self.stage is not Stage.RESPONSE:
            raise ServerError(f"not ready to send: {self.stage}")

        # Chunked
        if (
            self.response
            and self.response.headers.get("transfer-encoding") == "chunked"
        ):
            size = len(data)
            if end_stream:
                data = (
                    b"%x\r\n%b\r\n0\r\n\r\n" % (size, data)
                    if size
                    else b"0\r\n\r\n"
                )
            elif size:
                data = b"%x\r\n%b\r\n" % (size, data)

        logger.debug(  # no cov
            f"{Colors.BLUE}[transmitting]{Colors.END}",
            extra={"verbosity": 2},
        )
        self.protocol.connection.send_data(
            stream_id=self.request.stream_id,
            data=data,
            end_stream=end_stream,
        )
        self.transmit()

        if end_stream:
            self.stage = Stage.IDLE
