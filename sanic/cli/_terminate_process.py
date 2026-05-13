# ff:func feature=cli type=handler control=sequence
# ff:what Send a signal to terminate a process and clean up its pidfile
from __future__ import annotations

import os
import signal
import sys

from pathlib import Path


def _terminate_process(
    pid: int, sig: signal.Signals, pidfile: Path | None = None
) -> None:
    """Send a signal to terminate a process and clean up pidfile."""
    sig_name = sig.name

    try:
        os.kill(pid, sig)
        print(f"Sent {sig_name} to process {pid}")
    except ProcessLookupError:
        print(f"Process {pid} not found", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(
            f"Permission denied to signal process {pid}. "
            "Are you running as the correct user?",
            file=sys.stderr,
        )
        sys.exit(1)
    except OSError as e:
        print(f"Failed to signal process {pid}: {e}", file=sys.stderr)
        sys.exit(1)

    if pidfile:
        if pidfile.exists():
            try:
                pidfile.unlink()
                print(f"Removed PID file: {pidfile}")
            except OSError as e:
                print(
                    f"Warning: Could not remove PID file {pidfile}: {e}",
                    file=sys.stderr,
                )
        lockfile = pidfile.with_suffix(".lock")
        if lockfile.exists():
            try:
                lockfile.unlink()
            except OSError:
                pass
