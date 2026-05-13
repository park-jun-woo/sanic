# ff:func feature=worker type=util control=sequence
# ff:what Best-effort check if a process is a Sanic instance via /proc cmdline
import sys

from pathlib import Path


def _is_sanic_process(pid: int) -> bool:
    """
    Best-effort Sanic process identification.

    On Linux, checks /proc/<pid>/cmdline for 'sanic'. On other platforms,
    falls back to True if process exists (no strong identification).
    """
    _mod = sys.modules.get("sanic.worker.daemon") or sys.modules[__name__]
    _Path = getattr(_mod, "Path", Path)
    proc_cmdline = _Path(f"/proc/{pid}/cmdline")
    if proc_cmdline.exists():
        try:
            data = proc_cmdline.read_bytes()
            return b"sanic" in data
        except OSError:
            return False
    return True
