# ff:func feature=cli type=resolver control=sequence
# ff:what Resolve a daemon PID from either a direct PID or a pidfile path
from __future__ import annotations

import sys

from pathlib import Path

from sanic.worker.daemon import Daemon


def resolve_target(
    pid: int | None, pidfile: str | None
) -> tuple[int, Path | None]:
    """
    Resolve a PID from either a direct PID or a pidfile path.

    Returns:
        Tuple of (pid, pidfile_path or None)

    Raises:
        SystemExit: If pidfile not found or invalid
    """
    if pid:
        return pid, None

    pidfile_path = Path(pidfile)  # type: ignore[arg-type]
    if not pidfile_path.exists():
        print(f"PID file not found: {pidfile_path}", file=sys.stderr)
        sys.exit(1)

    resolved_pid = Daemon.read_pidfile(pidfile_path)
    if resolved_pid is None:
        print(f"Invalid PID file: {pidfile_path}", file=sys.stderr)
        sys.exit(1)

    return resolved_pid, pidfile_path
