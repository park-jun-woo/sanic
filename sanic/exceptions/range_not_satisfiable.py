# ff:type feature=error type=exception
# ff:what HTTP 416 Range Not Satisfiable exception
from typing import Any

from sanic.exceptions.http_exception import HTTPException
from sanic.models.protocol_types import Range


class RangeNotSatisfiable(HTTPException):
    """416 Range Not Satisfiable

    Args:
        message (Optional[Union[str, bytes]], optional): The message to be sent to the client. If `None`
            then the HTTP status 'Range Not Satisfiable' will be sent. Defaults to `None`.
        content_range (Optional[ContentRange], optional): An object meeting the :class:`.ContentRange` protocol
            that has a `total` property. Defaults to `None`.
        quiet (Optional[bool], optional): When `True`, the error traceback will be suppressed
            from the logs. Defaults to `None`.
        context (Optional[Dict[str, Any]], optional): Additional mapping of key/value data that will be
            sent to the client upon exception. Defaults to `None`.
        extra (Optional[Dict[str, Any]], optional): Additional mapping of key/value data that will NOT be
            sent to the client when in PRODUCTION mode. Defaults to `None`.
        headers (Optional[Dict[str, Any]], optional): Additional headers that should be sent with the HTTP
            response. Defaults to `None`.
    """  # noqa: E501

    status_code = 416
    quiet = True

    def __init__(
        self,
        message: str | bytes | None = None,
        content_range: Range | None = None,
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
        if content_range is not None:
            self.headers = {
                **self.headers,
                "Content-Range": f"bytes */{content_range.total}",
            }


ContentRangeError = RangeNotSatisfiable
