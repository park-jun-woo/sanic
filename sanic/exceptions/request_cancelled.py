# ff:type feature=error type=exception
# ff:what Exception raised when a request is cancelled
from asyncio import CancelledError


class RequestCancelled(CancelledError):
    quiet = True
