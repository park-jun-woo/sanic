# ff:type feature=logging type=formatter
# ff:what JSON log formatter that outputs log records as JSON objects

from __future__ import annotations

import logging

from sanic.helpers import json_dumps
from sanic.logging.auto_formatter import DEFAULT_FIELDS, AutoFormatter


class JSONFormatter(AutoFormatter):
    """
    The JSONFormatter is used to output logs in JSON format.

    This is useful for logging to a file or to a log aggregator that
    understands JSON. It will output all the fields from the LogRecord
    as well as the extra fields that are passed in.

    You can use it as follows:

    .. code-block:: python

        from sanic.log import LOGGING_CONFIG_DEFAULTS

        LOGGING_CONFIG_DEFAULTS["formatters"] = {
            "generic": {
                "class": "sanic.logging.formatter.JSONFormatter"
            },
            "access": {
                "class": "sanic.logging.formatter.JSONFormatter"
            },
        }
    """

    ATTY = False
    NO_COLOR = True
    FIELDS = [
        "name",
        "levelno",
        "pathname",
        "module",
        "filename",
        "lineno",
    ]

    dumps = json_dumps

    def format(self, record: logging.LogRecord) -> str:
        return self.format_dict(self.to_dict(record))

    def to_dict(self, record: logging.LogRecord) -> dict:
        base = {field: getattr(record, field, None) for field in self.FIELDS}
        extra = {
            key: value
            for key, value in record.__dict__.items()
            if key not in DEFAULT_FIELDS
        }
        info = {}
        if record.exc_info:
            info["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info:
            info["stack_info"] = self.formatStack(record.stack_info)
        return {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            **base,
            **info,
            **extra,
        }

    def format_dict(self, record: dict) -> str:
        return self.dumps(record)
