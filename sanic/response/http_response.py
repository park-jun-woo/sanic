# ff:type feature=response type=model
# ff:what Standard HTTP response with body encoding, status, headers, and async

from __future__ import annotations

from typing import Any

from sanic.compat import Header
from sanic.response.base_http_response import BaseHTTPResponse


class HTTPResponse(BaseHTTPResponse):
    """HTTP response to be sent back to the client.

    Args:
        body (Optional[Any], optional): The body content to be returned. Defaults to `None`.
        status (int, optional): HTTP response number. Defaults to `200`.
        headers (Optional[Union[Header, Dict[str, str]]], optional): Headers to be returned. Defaults to `None`.
        content_type (Optional[str], optional): Content type to be returned (as a header). Defaults to `None`.
    """  # noqa: E501

    __slots__ = ()

    def __init__(
        self,
        body: Any = None,
        status: int = 200,
        headers: Header | dict[str, str] | None = None,
        content_type: str | None = None,
    ):
        super().__init__()

        self.content_type: str | None = content_type
        self.body = self._encode_body(body)
        self.status = status
        self.headers = Header(headers or {})
        self._cookies = None

    async def eof(self):
        """Send a EOF (End of File) message to the client."""
        await self.send("", True)

    async def __aenter__(self):
        return self.send

    async def __aexit__(self, *_):
        await self.eof()
