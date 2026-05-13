# ff:type feature=error type=exception
# ff:what HTTP 405 Method Not Allowed exception
from collections.abc import Sequence
from typing import Any

from sanic.exceptions.http_exception import HTTPException


class MethodNotAllowed(HTTPException):
    """405 Method Not Allowed

    Args:
        message (Optional[Union[str, bytes]], optional): The message to be sent to the client. If `None`
            then the HTTP status 'Method Not Allowed' will be sent. Defaults to `None`.
        method (Optional[str], optional): The HTTP method that was used. Defaults to an empty string.
        allowed_methods (Optional[Sequence[str]], optional): The HTTP methods that can be used instead of the
            one that was attempted.
        quiet (Optional[bool], optional): When `True`, the error traceback will be suppressed
            from the logs. Defaults to `None`.
        context (Optional[Dict[str, Any]], optional): Additional mapping of key/value data that will be
            sent to the client upon exception. Defaults to `None`.
        extra (Optional[Dict[str, Any]], optional): Additional mapping of key/value data that will NOT be
            sent to the client when in PRODUCTION mode. Defaults to `None`.
        headers (Optional[Dict[str, Any]], optional): Additional headers that should be sent with the HTTP
            response. Defaults to `None`.
    """  # noqa: E501

    status_code = 405
    quiet = True

    def __init__(
        self,
        message: str | bytes | None = None,
        method: str = "",
        allowed_methods: Sequence[str] | None = None,
        *,
        quiet: bool | None = None,
        context: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ):
        super().__init__(
            message,
            quiet=quiet,
            context=context,
            extra=extra,
            headers=headers,
        )
        if allowed_methods:
            self.headers = {
                **self.headers,
                "Allow": ", ".join(allowed_methods),
            }
        self.method = method
        self.allowed_methods = allowed_methods


MethodNotSupported = MethodNotAllowed
