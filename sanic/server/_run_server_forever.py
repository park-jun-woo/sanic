# ff:func feature=server type=runner control=sequence
# ff:what Run the event loop forever with cleanup, signal removal, and shutdown
import sys

from signal import SIGINT, SIGTERM

from sanic.log import server_logger
from sanic.server._run_shutdown_coro import _run_shutdown_coro
from sanic.server.socket import remove_unix_socket


def _run_server_forever(loop, before_stop, after_stop, cleanup, unix, pid):
    _runners = sys.modules.get("sanic.server.runners")
    _remove_unix_socket = (
        getattr(_runners, "remove_unix_socket", remove_unix_socket)
        if _runners
        else remove_unix_socket
    )

    try:
        server_logger.info("Worker ready [%s]", pid)
        loop.run_forever()
    finally:
        server_logger.info("Stopping worker [%s]", pid)

        for _signal in [SIGINT, SIGTERM]:
            try:
                loop.remove_signal_handler(_signal)
            except (NotImplementedError, OSError):
                pass

        _run_shutdown_coro(loop, before_stop)

        if cleanup:
            cleanup()

        _run_shutdown_coro(loop, after_stop)

        _remove_unix_socket(unix)
        loop.close()
        server_logger.info("Worker complete [%s]", pid)
