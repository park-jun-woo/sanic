# ff:func feature=server type=handler control=sequence
# ff:what Handle ServerError exceptions during startup by logging the error mes

from sanic.exceptions import ServerError
from sanic.log import error_logger


def _handle_server_error(exc: Exception) -> bool:
    if not isinstance(exc, ServerError):
        return False

    error_logger.error(f"Startup failed due to server error. {exc}")
    return True
