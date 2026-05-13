# Re-export daemon classes and functions for backward compatibility
from pathlib import Path  # noqa: F401

from sanic.compat import OS_IS_WINDOWS  # noqa: F401
from sanic.worker._get_default_runtime_dir import _get_default_runtime_dir
from sanic.worker._is_sanic_process import _is_sanic_process
from sanic.worker._process_exists import _process_exists
from sanic.worker._sanitize_name import _sanitize_name
from sanic.worker.daemon_class import Daemon
from sanic.worker.daemon_error import DaemonError
from sanic.worker.pidfile_info import PidfileInfo

__all__ = (
    "Daemon",
    "DaemonError",
    "PidfileInfo",
    "_get_default_runtime_dir",
    "_is_sanic_process",
    "_process_exists",
    "_sanitize_name",
)
