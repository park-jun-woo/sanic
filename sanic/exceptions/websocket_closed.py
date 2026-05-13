# ff:type feature=error type=exception
# ff:what Exception raised when a websocket connection is closed
from sanic.exceptions.sanic_exception import SanicException


class WebsocketClosed(SanicException):
    """Exception raised when a websocket is closed."""

    quiet = True
    message = "Client has closed the websocket connection"
