# ff:func feature=server type=handler control=sequence
# ff:what Handle DaemonError exceptions during startup by logging the error mes

from sanic.log import error_logger
from sanic.worker.daemon import DaemonError


def _handle_daemon_error(exc: Exception) -> bool:
    if not isinstance(exc, DaemonError):
        return False

    error_logger.error(f"Daemon error: {exc}")
    return True
