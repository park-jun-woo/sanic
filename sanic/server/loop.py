# Re-export loop functions for backward compatibility
import asyncio  # noqa: F401

from os import getenv  # noqa: F401

from sanic.server.try_use_uvloop import try_use_uvloop
from sanic.server.try_windows_loop import try_windows_loop

__all__ = (
    "try_use_uvloop",
    "try_windows_loop",
)
