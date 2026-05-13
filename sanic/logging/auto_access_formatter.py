# ff:type feature=logging type=formatter
# ff:what Access log formatter with host, request, status, byte, and duration f

from __future__ import annotations

import logging

from sanic.logging.auto_formatter import CONTROL_LIMIT_END, AutoFormatter
from sanic.logging.color import Colors as c


class AutoAccessFormatter(AutoFormatter):
    MESSAGE_FORMAT = (
        f"{c.PURPLE}%(host)s "
        f"{c.BLUE + c.BOLD}%(request)s{c.END} "
        f"%(right)s%(status)s %(byte)s {c.GREY}%(duration)s{c.END}"
    )

    def format(self, record: logging.LogRecord) -> str:
        status = len(str(getattr(record, "status", "")))
        byte = len(str(getattr(record, "byte", "")))
        duration = len(str(getattr(record, "duration", "")))
        record.right = (
            CONTROL_LIMIT_END.format(right=status + byte + duration + 1)
            if self.ATTY
            else ""
        )
        return super().format(record)

    def _set_levelname(self, record: logging.LogRecord) -> None:
        if self.ATTY and record.levelno == logging.INFO:
            record.levelname = f"{c.SANIC}ACCESS{c.END}"
