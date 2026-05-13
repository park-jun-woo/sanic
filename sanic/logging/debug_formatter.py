# ff:type feature=logging type=formatter
# ff:what Debug log formatter with truncated level names and colorized tracebac

from __future__ import annotations

import logging

from sanic.logging.auto_formatter import (
    EXCEPTION_LINE_RE,
    FILE_LINE_RE,
    AutoFormatter,
)
from sanic.logging.color import Colors as c


class DebugFormatter(AutoFormatter):
    """
    The DebugFormatter is used for development and debugging purposes.

    It can be used directly, or it will be automatically selected if the
    environment is set up for development and is using the AutoFormatter.
    """

    IDENT_LIMIT = 5
    MESSAGE_START = 23
    DATE_FORMAT = "%H:%M:%S"

    def _set_levelname(self, record: logging.LogRecord) -> None:
        if len(record.levelname) > 5:
            record.levelname = record.levelname[:4]
        super()._set_levelname(record)

    def formatException(self, ei):  # no cov
        orig = super().formatException(ei)
        if not self.ATTY or self.NO_COLOR:
            return orig
        colored_traceback = []
        lines = orig.splitlines()
        for idx, line in enumerate(lines):
            if line.startswith("  File"):
                line = self._color_file_line(line)
            elif line.startswith("    "):
                line = self._color_code_line(line)
            elif (
                "Error" in line or "Exception" in line or len(lines) - 1 == idx
            ):
                line = self._color_exception_line(line)
            colored_traceback.append(line)
        return "\n".join(colored_traceback)

    def _color_exception_line(self, line: str) -> str:  # no cov
        match = EXCEPTION_LINE_RE.match(line)
        if not match:
            return line
        exc = match.group("exc")
        message = match.group("message")
        return f"{c.SANIC}{c.BOLD}{exc}{c.END}: {c.BOLD}{message}{c.END}"

    def _color_file_line(self, line: str) -> str:  # no cov
        match = FILE_LINE_RE.search(line)
        if not match:
            return line
        path = match.group("path")
        line_num = match.group("line_num")
        location = match.group("location")
        return (
            f'  File "{path}", line {c.CYAN}{c.BOLD}{line_num}{c.END}, '
            f"in {c.BLUE}{c.BOLD}{location}{c.END}"
        )

    def _color_code_line(self, line: str) -> str:  # no cov
        return f"{c.YELLOW}{line}{c.END}"
