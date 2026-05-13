# ff:func feature=server type=handler control=sequence
# ff:what Handle OS errors during startup by logging address-in-use or general

import errno

from sanic.log import error_logger


def _handle_os_error(exc: Exception) -> bool:
    if not isinstance(exc, OSError):
        return False

    if exc.errno == errno.EADDRINUSE:
        error_logger.error(
            "Startup failed: Address already in use. \n\n"
            "Ensure no other process is using the same address and port, "
            "or configure the server to use a different port."
        )
    else:
        error_logger.error(
            "Startup failed due to OS error: %s (errno %s)",
            exc.strerror,
            exc.errno,
        )
    return True
