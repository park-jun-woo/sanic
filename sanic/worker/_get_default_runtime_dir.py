# ff:func feature=worker type=resolver control=sequence
# ff:what Determine the default runtime directory for PID and lock files
from __future__ import annotations

import os

from pathlib import Path


def _get_default_runtime_dir() -> Path:
    """
    Default directory for auto-generated runtime artifacts (pid/lock/log).

    Priority:
      1) XDG_RUNTIME_DIR/sanic  (preferred, runtime-only)
      2) ~/.local/state/sanic   (persistent state, modern default)
      3) ~/.cache/sanic         (fallback)
      4) cwd                    (last resort)
    """
    xdg_runtime = os.environ.get("XDG_RUNTIME_DIR")
    if xdg_runtime:
        path = Path(xdg_runtime) / "sanic"
        try:
            path.mkdir(mode=0o700, parents=True, exist_ok=True)
            return path
        except OSError:
            pass

    state_dir = Path.home() / ".local" / "state" / "sanic"
    try:
        state_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        return state_dir
    except OSError:
        pass

    cache_dir = Path.home() / ".cache" / "sanic"
    try:
        cache_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        return cache_dir
    except OSError:
        pass

    return Path.cwd()
