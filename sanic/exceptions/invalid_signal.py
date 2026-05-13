# ff:type feature=error type=exception
# ff:what Exception raised when an invalid signal is sent
from sanic.exceptions.sanic_exception import SanicException


class InvalidSignal(SanicException):
    """Exception raised when an invalid signal is sent."""
