# ff:type feature=response type=model
# ff:what Base class for all HTTP responses with cookie management, header proc

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    AnyStr,
    TypeVar,
)

from sanic.compat import Header
from sanic.cookies import CookieJar
from sanic.cookies.cookie import Cookie, SameSite
from sanic.exceptions import SanicException, ServerError
from sanic.helpers import has_message_body, json_dumps
from sanic.http import Http

if TYPE_CHECKING:
    from sanic.asgi import ASGIApp
    from sanic.http.http3 import HTTPReceiver
    from sanic.request import Request
else:
    Request = TypeVar("Request")


class BaseHTTPResponse:
    """The base class for all HTTP Responses"""

    __slots__ = (
        "asgi",
        "body",
        "content_type",
        "stream",
        "status",
        "headers",
        "_cookies",
    )

    _dumps = json_dumps

    def __init__(self):
        self.asgi: bool = False
        self.body: bytes | None = None
        self.content_type: str | None = None
        self.stream: Http | ASGIApp | HTTPReceiver | None = None
        self.status: int = None
        self.headers = Header({})
        self._cookies: CookieJar | None = None

    def __repr__(self):
        class_name = self.__class__.__name__
        return f"<{class_name}: {self.status} {self.content_type}>"

    def _encode_body(self, data: str | bytes | None):
        if data is None:
            return b""
        return data.encode() if hasattr(data, "encode") else data  # type: ignore

    @property
    def cookies(self) -> CookieJar:
        """The response cookies.

        See [Cookies](/en/guide/basics/cookies.html)

        Returns:
            CookieJar: The response cookies
        """
        if self._cookies is None:
            self._cookies = CookieJar(self.headers)
        return self._cookies

    @property
    def processed_headers(self) -> Iterator[tuple[bytes, bytes]]:
        """Obtain a list of header tuples encoded in bytes for sending.

        Add and remove headers based on status and content_type.

        Returns:
            Iterator[Tuple[bytes, bytes]]: A list of header tuples encoded in bytes for sending
        """  # noqa: E501
        if has_message_body(self.status):
            self.headers.setdefault("content-type", self.content_type)
        # Encode headers into bytes
        return (
            (name.encode("ascii"), f"{value}".encode(errors="surrogateescape"))
            for name, value in self.headers.items()
        )

    async def send(
        self,
        data: AnyStr | None = None,
        end_stream: bool | None = None,
    ) -> None:
        """Send any pending response headers and the given data as body.

        Args:
            data (Optional[AnyStr], optional): str or bytes to be written. Defaults to `None`.
            end_stream (Optional[bool], optional): whether to close the stream after this block. Defaults to `None`.
        """  # noqa: E501
        if data is None and end_stream is None:
            end_stream = True
        if self.stream is None:
            raise SanicException(
                "No stream is connected to the response object instance."
            )
        if self.stream.send is None:
            if end_stream and not data:
                return
            raise ServerError(
                "Response stream was ended, no more response data is "
                "allowed to be sent."
            )
        data = data.encode() if hasattr(data, "encode") else data or b""  # type: ignore
        await self.stream.send(
            data,  # type: ignore
            end_stream=end_stream or False,
        )

    def add_cookie(
        self,
        key: str,
        value: str,
        *,
        path: str = "/",
        domain: str | None = None,
        secure: bool = True,
        max_age: int | None = None,
        expires: datetime | None = None,
        httponly: bool = False,
        samesite: SameSite | None = "Lax",
        partitioned: bool = False,
        comment: str | None = None,
        host_prefix: bool = False,
        secure_prefix: bool = False,
    ) -> Cookie:
        """Add a cookie to the CookieJar

        See [Cookies](/en/guide/basics/cookies.html)

        Args:
            key (str): The key to be added
            value (str): The value to be added
            path (str, optional): Path of the cookie. Defaults to `"/"`.
            domain (Optional[str], optional): Domain of the cookie. Defaults to `None`.
            secure (bool, optional): Whether the cookie is secure. Defaults to `True`.
            max_age (Optional[int], optional): Max age of the cookie. Defaults to `None`.
            expires (Optional[datetime], optional): Expiry date of the cookie. Defaults to `None`.
            httponly (bool, optional): Whether the cookie is http only. Defaults to `False`.
            samesite (Optional[SameSite], optional): SameSite policy of the cookie. Defaults to `"Lax"`.
            partitioned (bool, optional): Whether the cookie is partitioned. Defaults to `False`.
            comment (Optional[str], optional): Comment of the cookie. Defaults to `None`.
            host_prefix (bool, optional): Whether to add __Host- as a prefix to the key. This requires that path="/", domain=None, and secure=True. Defaults to `False`.
            secure_prefix (bool, optional): Whether to add __Secure- as a prefix to the key. This requires that secure=True. Defaults to `False`.

        Returns:
            Cookie: The cookie that was added
        """  # noqa: E501
        return self.cookies.add_cookie(
            key=key,
            value=value,
            path=path,
            domain=domain,
            secure=secure,
            max_age=max_age,
            expires=expires,
            httponly=httponly,
            samesite=samesite,
            partitioned=partitioned,
            comment=comment,
            host_prefix=host_prefix,
            secure_prefix=secure_prefix,
        )

    def delete_cookie(
        self,
        key: str,
        *,
        path: str = "/",
        domain: str | None = None,
        host_prefix: bool = False,
        secure_prefix: bool = False,
    ) -> None:
        """Delete a cookie

        This will effectively set it as Max-Age: 0, which a browser should
        interpret it to mean: "delete the cookie".

        Since it is a browser/client implementation, your results may vary
        depending upon which client is being used.

        See [Cookies](/en/guide/basics/cookies.html)

        Args:
            key (str): The key to be deleted
            path (str, optional): Path of the cookie. Defaults to `"/"`.
            domain (Optional[str], optional): Domain of the cookie. Defaults to `None`.
            host_prefix (bool, optional): Whether to add __Host- as a prefix to the key. This requires that path="/", domain=None, and secure=True. Defaults to `False`.
            secure_prefix (bool, optional): Whether to add __Secure- as a prefix to the key. This requires that secure=True. Defaults to `False`.
        """  # noqa: E501
        self.cookies.delete_cookie(
            key=key,
            path=path,
            domain=domain,
            host_prefix=host_prefix,
            secure_prefix=secure_prefix,
        )
