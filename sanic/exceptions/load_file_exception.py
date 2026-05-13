# ff:type feature=error type=exception
# ff:what Exception raised when a file cannot be loaded
from sanic.exceptions.sanic_exception import SanicException


class LoadFileException(SanicException):
    """Exception raised when a file cannot be loaded."""
