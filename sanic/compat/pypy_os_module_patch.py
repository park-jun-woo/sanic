# ff:func feature=compat type=util control=sequence
# ff:what Patches PyPy os module to add missing readlink function
import os
import sys

from sanic.log import error_logger


def pypy_os_module_patch() -> None:
    """
    The PyPy os module is missing the 'readlink' function, which causes issues
    withaiofiles. This workaround replaces the missing 'readlink' function
    with 'os.path.realpath', which serves the same purpose.
    """
    if hasattr(os, "readlink"):
        error_logger.debug(
            "PyPy: Skipping patching of the os module as it appears the "
            "'readlink' function has been added."
        )
        return

    module = sys.modules["os"]
    module.readlink = os.path.realpath  # type: ignore
