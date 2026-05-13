# ff:type feature=logging type=formatter
# ff:what Debug access log formatter with compact timestamps and no extra field

from sanic.logging.auto_access_formatter import AutoAccessFormatter


class DebugAccessFormatter(AutoAccessFormatter):
    IDENT_LIMIT = 5
    MESSAGE_START = 23
    DATE_FORMAT = "%H:%M:%S"
    LOG_EXTRA = False
