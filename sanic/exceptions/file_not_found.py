# ff:type feature=error type=exception
# ff:what HTTP 404 exception for missing files on the file system
from os import PathLike
from typing import Any

from sanic.exceptions.not_found import NotFound


class FileNotFound(NotFound):
    """404 Not Found

    A specific form of :class:`.NotFound` that is specifically when looking
    for a file on the file system at a known path.

    Args:
        message (Optional[Union[str, bytes]], optional): The message to be sent to the client. If `None`
            then the HTTP status 'Not Found' will be sent. Defaults to `None`.
        path (Optional[PathLike], optional): The path, if any, to the file that could not
            be found. Defaults to `None`.
        relative_url (Optional[str], optional): A relative URL of the file. Defaults to `None`.
        quiet (Optional[bool], optional): When `True`, the error traceback will be suppressed
            from the logs. Defaults to `None`.
        context (Optional[Dict[str, Any]], optional): Additional mapping of key/value data that will be
            sent to the client upon exception. Defaults to `None`.
        extra (Optional[Dict[str, Any]], optional): Additional mapping of key/value data that will NOT be
            sent to the client when in PRODUCTION mode. Defaults to `None`.
        headers (Optional[Dict[str, Any]], optional): Additional headers that should be sent with the HTTP
            response. Defaults to `None`.
    """  # noqa: E501

    def __init__(
        self,
        message: str | bytes | None = None,
        path: PathLike | None = None,
        relative_url: str | None = None,
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
        self.path = path
        self.relative_url = relative_url
