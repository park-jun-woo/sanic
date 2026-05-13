# ff:func feature=server type=handler control=sequence
# ff:what Remove a dead Unix socket file during server exit
from __future__ import annotations

import socket
import stat

from pathlib import Path


def remove_unix_socket(path: Path | str | None) -> None:
    """Remove dead unix socket during server exit."""
    if not path:
        return
    try:
        path = Path(path)
        if stat.S_ISSOCK(path.lstat().st_mode):
            # Is it actually dead (doesn't belong to a new server instance)?
            with socket.socket(socket.AF_UNIX) as testsock:
                try:
                    testsock.connect(path.as_posix())
                except ConnectionRefusedError:
                    path.unlink()
    except FileNotFoundError:
        pass
