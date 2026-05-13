# ff:func feature=server type=builder control=sequence
# ff:what Create and bind a Unix domain socket with atomic rename for safety
from __future__ import annotations

import secrets
import socket
import stat

from pathlib import Path


def bind_unix_socket(
    path: Path | str, *, mode=0o666, backlog=100
) -> socket.socket:
    """Create unix socket.
    :param path: filesystem path
    :param backlog: Maximum number of connections to queue
    :return: socket.socket object
    """

    # Sanitise and pre-verify socket path
    path = Path(path)
    folder = path.parent
    if not folder.is_dir():
        raise FileNotFoundError(f"Socket folder does not exist: {folder}")
    try:
        if not stat.S_ISSOCK(path.lstat().st_mode):
            raise FileExistsError(f"Existing file is not a socket: {path}")
    except FileNotFoundError:
        pass
    # Create new socket with a random temporary name
    tmp_path = path.with_name(f"{path.name}.{secrets.token_urlsafe()}")
    sock = socket.socket(socket.AF_UNIX)
    try:
        # Critical section begins (filename races)
        sock.bind(tmp_path.as_posix())
        try:
            tmp_path.chmod(mode)
            # Start listening before rename to avoid connection failures
            sock.listen(backlog)
            tmp_path.rename(path)
        except:  # noqa: E722
            try:
                tmp_path.unlink()
            finally:
                raise
    except:  # noqa: E722
        try:
            sock.close()
        finally:
            raise
    return sock
