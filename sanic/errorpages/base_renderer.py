# ff:type feature=error type=formatter
# ff:what Base renderer class for formatting exception responses
from __future__ import annotations

import typing as t

from functools import partial

from sanic.exceptions import SanicException
from sanic.helpers import STATUS_CODES

dumps: t.Callable[..., str]
try:
    from ujson import dumps

    dumps = partial(dumps, escape_forward_slashes=False)
except ImportError:  # noqa
    from json import dumps

if t.TYPE_CHECKING:
    from sanic import HTTPResponse, Request

FALLBACK_TEXT = """\
The application encountered an unexpected error and could not continue.\
"""
FALLBACK_STATUS = 500


class BaseRenderer:
    """Base class that all renderers must inherit from.

    This class defines the structure for rendering objects, handling the core functionality that specific renderers may extend.

    Attributes:
        request (Request): The incoming request object that needs rendering.
        exception (Exception): Any exception that occurred and needs to be rendered.
        debug (bool): Flag indicating whether to render with debugging information.

    Methods:
        dumps: A static method that must be overridden by subclasses to define the specific rendering.

    Args:
        request (Request): The incoming request object that needs rendering.
        exception (Exception): Any exception that occurred and needs to be rendered.
        debug (bool): Flag indicating whether to render with debugging information.
    """  # noqa: E501

    dumps = staticmethod(dumps)

    def __init__(self, request: Request, exception: Exception, debug: bool):
        self.request = request
        self.exception = exception
        self.debug = debug

    @property
    def headers(self) -> t.Dict[str, str]:
        """The headers to be used for the response."""
        if isinstance(self.exception, SanicException):
            return getattr(self.exception, "headers", {})
        return {}

    @property
    def status(self):
        """The status code to be used for the response."""
        if isinstance(self.exception, SanicException):
            return getattr(self.exception, "status_code", FALLBACK_STATUS)
        return FALLBACK_STATUS

    @property
    def text(self):
        """The text to be used for the response."""
        if self.debug or isinstance(self.exception, SanicException):
            return str(self.exception)
        return FALLBACK_TEXT

    @property
    def title(self):
        """The title to be used for the response."""
        status_text = STATUS_CODES.get(self.status, b"Error Occurred").decode()
        return f"{self.status} — {status_text}"

    def render(self) -> HTTPResponse:
        """Outputs the exception as a response.

        Returns:
            HTTPResponse: The response object.
        """
        output = (
            self.full
            if self.debug and not getattr(self.exception, "quiet", False)
            else self.minimal
        )()
        output.status = self.status
        output.headers.update(self.headers)
        return output

    def minimal(self) -> HTTPResponse:  # noqa
        """Provide a formatted message that is meant to not show any sensitive data or details.

        This is the default fallback for production environments.

        Returns:
            HTTPResponse: The response object.
        """  # noqa: E501
        raise NotImplementedError

    def full(self) -> HTTPResponse:  # noqa
        """Provide a formatted message that has all details and is mean to be used primarily for debugging and non-production environments.

        Returns:
            HTTPResponse: The response object.
        """  # noqa: E501
        raise NotImplementedError
