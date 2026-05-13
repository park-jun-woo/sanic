# ff:type feature=response type=model
# ff:what Compatibility layer for streaming HTTP responses bridging deprecated

from __future__ import annotations

from collections.abc import Coroutine
from typing import Any, Callable, TypeVar

from sanic.compat import Header
from sanic.cookies import CookieJar
from sanic.exceptions import ServerError
from sanic.response.base_http_response import BaseHTTPResponse
from sanic.response.http_response import HTTPResponse

Request = TypeVar("Request")


class ResponseStream:
    """A compat layer to bridge the gap after the deprecation of StreamingHTTPResponse.

    It will be removed when:
    - file_stream is moved to new style streaming
    - file and file_stream are combined into a single API
    """  # noqa: E501

    __slots__ = (
        "_cookies",
        "content_type",
        "headers",
        "request",
        "response",
        "status",
        "streaming_fn",
    )

    def __init__(
        self,
        streaming_fn: Callable[
            [BaseHTTPResponse | "ResponseStream"],
            Coroutine[Any, Any, None],
        ],
        status: int = 200,
        headers: Header | dict[str, str] | None = None,
        content_type: str | None = None,
    ):
        if headers is None:
            headers = Header()
        elif not isinstance(headers, Header):
            headers = Header(headers)
        self.streaming_fn = streaming_fn
        self.status = status
        self.headers = headers or Header()
        self.content_type = content_type
        self.request: Request | None = None
        self._cookies: CookieJar | None = None

    async def write(self, message: str):
        await self.response.send(message)

    async def stream(self) -> HTTPResponse:
        if not self.request:
            raise ServerError("Attempted response to unknown request")
        self.response = await self.request.respond(
            headers=self.headers,
            status=self.status,
            content_type=self.content_type,
        )
        await self.streaming_fn(self)
        return self.response

    async def eof(self) -> None:
        await self.response.eof()

    @property
    def cookies(self) -> CookieJar:
        if self._cookies is None:
            self._cookies = CookieJar(self.headers)
        return self._cookies

    @property
    def processed_headers(self):
        return self.response.processed_headers

    @property
    def body(self):
        return self.response.body

    def __call__(self, request: Request) -> "ResponseStream":
        self.request = request
        return self

    def __await__(self):
        return self.stream().__await__()
