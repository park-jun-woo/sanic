# ff:type feature=logging type=formatter
# ff:what Auto-switching log formatter that selects Debug or Production format

from __future__ import annotations

import logging
import os
import re

from sanic.helpers import is_atty
from sanic.logging.color import LEVEL_COLORS
from sanic.logging.color import Colors as c

CONTROL_RE = re.compile(r"\033\[[0-9;]*\w")
CONTROL_LIMIT_IDENT = "\033[1000D\033[{limit}C"
CONTROL_LIMIT_START = "\033[1000D\033[{start}C\033[K"
CONTROL_LIMIT_END = "\033[1000C\033[{right}D\033[K"
EXCEPTION_LINE_RE = re.compile(r"^(?P<exc>.*?): (?P<message>.*)$")
FILE_LINE_RE = re.compile(
    r"File \"(?P<path>.*?)\", line (?P<line_num>\d+), in (?P<location>.*)"
)
DEFAULT_FIELDS = set(
    logging.LogRecord("", 0, "", 0, "", (), None).__dict__.keys()
) | {
    "ident",
    "message",
    "asctime",
    "right",
}


class AutoFormatter(logging.Formatter):
    """
    Automatically sets up the formatter based on the environment.

    It will switch between the Debug and Production formatters based upon
    how the environment is set up. Additionally, it will automatically
    detect if the output is a TTY and colorize the output accordingly.
    """

    SETUP = False
    ATTY = is_atty()
    NO_COLOR = os.environ.get("SANIC_NO_COLOR", "false").lower() == "true"
    LOG_EXTRA = os.environ.get("SANIC_LOG_EXTRA", "true").lower() == "true"
    IDENT = os.environ.get("SANIC_WORKER_IDENTIFIER", "Main ") or "Main "
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S %z"
    IDENT_LIMIT = 5
    MESSAGE_START = 42
    PREFIX_FORMAT = (
        f"{c.GREY}%(ident)s{{limit}} %(asctime)s {c.END}"
        "%(levelname)s: {start}"
    )
    MESSAGE_FORMAT = "%(message)s"

    def __init__(self, *args) -> None:
        args_list = list(args)
        if not args:
            args_list.append(self._make_format())
        elif args and not args[0]:
            args_list[0] = self._make_format()
        if len(args_list) < 2:
            args_list.append(self.DATE_FORMAT)
        elif not args[1]:
            args_list[1] = self.DATE_FORMAT

        super().__init__(*args_list)

    def format(self, record: logging.LogRecord) -> str:
        record.ident = self.IDENT
        self._set_levelname(record)
        output = super().format(record)
        if self.LOG_EXTRA:
            output += self._log_extra(record)
        return output

    def _set_levelname(self, record: logging.LogRecord) -> None:
        if (
            self.ATTY
            and not self.NO_COLOR
            and (color := LEVEL_COLORS.get(record.levelno))
        ):
            record.levelname = f"{color}{record.levelname}{c.END}"

    def _make_format(self) -> str:
        limit = CONTROL_LIMIT_IDENT.format(limit=self.IDENT_LIMIT)
        start = CONTROL_LIMIT_START.format(start=self.MESSAGE_START)
        base_format = self.PREFIX_FORMAT + self.MESSAGE_FORMAT
        fmt = base_format.format(limit=limit, start=start)
        if not self.ATTY or self.NO_COLOR:
            return CONTROL_RE.sub("", fmt)
        return fmt

    def _log_extra(self, record: logging.LogRecord, indent: int = 0) -> str:
        extra_lines = [""]

        for key, value in record.__dict__.items():
            if key not in DEFAULT_FIELDS:
                extra_lines.append(self._format_key_value(key, value, indent))

        return "\n".join(extra_lines)

    def _format_key_value(self, key, value, indent):
        indentation = " " * indent
        template = (
            f"{indentation}  {{c.YELLOW}}{{key}}{{c.END}}={{value}}"
            if self.ATTY and not self.NO_COLOR
            else f"{indentation}{{key}}={{value}}"
        )
        if isinstance(value, dict):
            nested_lines = [template.format(c=c, key=key, value="")]
            for nested_key, nested_value in value.items():
                nested_lines.append(
                    self._format_key_value(
                        nested_key, nested_value, indent + 2
                    )
                )
            return "\n".join(nested_lines)
        else:
            return template.format(c=c, key=key, value=value)
