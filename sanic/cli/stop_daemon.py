# ff:func feature=cli type=handler control=sequence
# ff:what Stop a daemon process gracefully with SIGTERM or forcefully with SIGK
from __future__ import annotations

import signal

from pathlib import Path

from sanic.cli._terminate_process import _terminate_process


def stop_daemon(
    pid: int, pidfile: Path | None = None, force: bool = False
) -> None:
    """Stop a daemon process gracefully (SIGTERM) or forcefully (SIGKILL)."""
    sig = signal.SIGKILL if force else signal.SIGTERM
    _terminate_process(pid, sig, pidfile)
