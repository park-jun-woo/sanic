# ff:type feature=logging type=formatter
# ff:what JSON access log formatter that outputs access logs as JSON objects

from __future__ import annotations

import logging

from sanic.logging.json_formatter import JSONFormatter


class JSONAccessFormatter(JSONFormatter):
    """
    The JSONAccessFormatter is used to output access logs in JSON format.

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
                "class": "sanic.logging.formatter.JSONAccessFormatter"
            },
        }
    """

    FIELDS = [
        "host",
        "request",
        "status",
        "byte",
        "duration",
    ]

    def to_dict(self, record: logging.LogRecord) -> dict:
        base = {field: getattr(record, field, None) for field in self.FIELDS}
        return {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            **base,
        }
