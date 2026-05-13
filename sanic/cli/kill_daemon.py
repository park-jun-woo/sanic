# ff:func feature=cli type=handler control=sequence
# ff:what Force kill a daemon process with SIGKILL
from __future__ import annotations

import signal

from pathlib import Path

from sanic.cli._terminate_process import _terminate_process


def kill_daemon(pid: int, pidfile: Path | None = None) -> None:
    """Force kill a daemon process with SIGKILL."""
    _terminate_process(pid, signal.SIGKILL, pidfile)
