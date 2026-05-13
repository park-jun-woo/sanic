# ff:type feature=error type=exception
# ff:what Exception raised when a config file cannot be executed
from typing import Any

from sanic.exceptions.sanic_exception import SanicException


class PyFileError(SanicException):
    def __init__(
        self,
        file,
        status_code: int | None = None,
        *,
        quiet: bool | None = None,
        context: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
    ):
        super().__init__(
            "could not execute config file %s" % file,
            status_code=status_code,
            quiet=quiet,
            context=context,
            extra=extra,
            headers=headers,
        )
