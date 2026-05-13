# ff:type feature=error type=exception
# ff:what Base HTTP exception class for all HTTP error responses
from typing import Any

from sanic.exceptions.sanic_exception import SanicException


class HTTPException(SanicException):
    """A base class for other exceptions and should not be called directly."""

    def __init__(
        self,
        message: str | bytes | None = None,
        *,
        quiet: bool | None = None,
        context: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            quiet=quiet,
            context=context,
            extra=extra,
            headers=headers,
        )
