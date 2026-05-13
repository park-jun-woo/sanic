# ff:func feature=cli type=handler control=sequence
# ff:what Check if a daemon process is running and clean up stale pidfile
from __future__ import annotations

import os
import sys

from contextlib import suppress
from pathlib import Path


def status_daemon(pid: int, pidfile: Path | None = None) -> bool:
    """
    Check if a daemon process is running.

    Args:
        pid: Process ID to check
        pidfile: Optional pidfile path to clean up if stale

    Returns:
        True if running, False otherwise (exits with code 1 if not)
    """
    try:
        os.kill(pid, 0)
        running = True
    except ProcessLookupError:
        running = False
    except PermissionError:
        running = True

    if running:
        print(f"Process {pid} is running")
        return True

    print(f"Process {pid} is NOT running")
    if pidfile and pidfile.exists():
        with suppress(OSError):
            pidfile.unlink()
            print(f"Removed stale PID file: {pidfile}")
    sys.exit(1)
