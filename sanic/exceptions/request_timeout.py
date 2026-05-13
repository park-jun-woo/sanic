# ff:type feature=error type=exception
# ff:what HTTP 408 Request Timeout exception
from sanic.exceptions.http_exception import HTTPException


class RequestTimeout(HTTPException):
    """408 Request Timeout

    The Web server (running the Web site) thinks that there has been too
    long an interval of time between 1) the establishment of an IP
    connection (socket) between the client and the server and
    2) the receipt of any data on that socket, so the server has dropped
    the connection. The socket connection has actually been lost - the Web
    server has 'timed out' on that particular socket connection.

    This is an internal exception thrown by Sanic and should not be used
    directly.

    Args:
        message (Optional[Union[str, bytes]], optional): The message to be sent to the client. If `None`
            then the HTTP status 'Bad Request' will be sent. Defaults to `None`.
        quiet (Optional[bool], optional): When `True`, the error traceback will be suppressed
            from the logs. Defaults to `None`.
        context (Optional[Dict[str, Any]], optional): Additional mapping of key/value data that will be
            sent to the client upon exception. Defaults to `None`.
        extra (Optional[Dict[str, Any]], optional): Additional mapping of key/value data that will NOT be
            sent to the client when in PRODUCTION mode. Defaults to `None`.
        headers (Optional[Dict[str, Any]], optional): Additional headers that should be sent with the HTTP
            response. Defaults to `None`.
    """  # noqa: E501

    status_code = 408
    quiet = True
