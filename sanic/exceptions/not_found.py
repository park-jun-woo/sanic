# ff:type feature=error type=exception
# ff:what HTTP 404 Not Found exception
from sanic.exceptions.http_exception import HTTPException


class NotFound(HTTPException):
    """A base class for other exceptions and should not be called directly.

    Args:
        message (Optional[Union[str, bytes]], optional): The message to be sent to the client. If `None`,
            then the appropriate HTTP response status message will be used instead. Defaults to `None`.
        quiet (Optional[bool], optional): When `True`, the error traceback will be suppressed from the logs.
            Defaults to `None`.
        context (Optional[Dict[str, Any]], optional): Additional mapping of key/value data that will be
            sent to the client upon exception. Defaults to `None`.
        extra (Optional[Dict[str, Any]], optional): Additional mapping of key/value data that will NOT be
            sent to the client when in PRODUCTION mode. Defaults to `None`.
        headers (Optional[Dict[str, Any]], optional): Additional headers that should be sent with the HTTP
            response. Defaults to `None`.
    """  # noqa: E501

    status_code = 404
    quiet = True
