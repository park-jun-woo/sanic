import asyncio
import os
import platform
import sys

from collections.abc import Awaitable

from sanic.compat.clear_function_annotate import (
    PYTHON_314_OR_LATER,
    clear_function_annotate,
)
from sanic.compat.ctrlc_workaround_for_windows import (
    ctrlc_workaround_for_windows,
)
from sanic.compat.enable_windows_color_support import (
    enable_windows_color_support,
)
from sanic.compat.header import Header
from sanic.compat.pypy_os_module_patch import pypy_os_module_patch
from sanic.compat.pypy_windows_set_console_cp_patch import (
    pypy_windows_set_console_cp_patch,
)
from sanic.compat.upper_str_enum import UpperStrEnum
from sanic.compat.use_context import StartMethod, use_context

OS_IS_WINDOWS = os.name == "nt"
PYPY_IMPLEMENTATION = platform.python_implementation() == "PyPy"
UVLOOP_INSTALLED = False

try:
    import uvloop  # type: ignore # noqa

    UVLOOP_INSTALLED = True
except ImportError:
    pass

use_trio = sys.argv[0].endswith("hypercorn") and "trio" in sys.argv

if use_trio:  # pragma: no cover
    import trio  # type: ignore

    def stat_async(path) -> Awaitable[os.stat_result]:
        return trio.Path(path).stat()

    open_async = trio.open_file
    CancelledErrors = tuple([asyncio.CancelledError, trio.Cancelled])
else:
    if PYPY_IMPLEMENTATION:
        pypy_os_module_patch()

        if OS_IS_WINDOWS:
            pypy_windows_set_console_cp_patch()

    from aiofiles import open as aio_open  # type: ignore
    from aiofiles.os import stat as stat_async  # type: ignore  # noqa: F401

    async def open_async(file, mode="r", **kwargs):
        return aio_open(file, mode, **kwargs)

    CancelledErrors = tuple([asyncio.CancelledError])


__all__ = [
    "CancelledErrors",
    "Header",
    "OS_IS_WINDOWS",
    "PYTHON_314_OR_LATER",
    "PYPY_IMPLEMENTATION",
    "StartMethod",
    "UVLOOP_INSTALLED",
    "UpperStrEnum",
    "clear_function_annotate",
    "ctrlc_workaround_for_windows",
    "enable_windows_color_support",
    "open_async",
    "pypy_os_module_patch",
    "pypy_windows_set_console_cp_patch",
    "stat_async",
    "use_context",
    "use_trio",
]
