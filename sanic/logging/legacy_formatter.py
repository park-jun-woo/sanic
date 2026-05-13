# ff:type feature=logging type=formatter
# ff:what Legacy-style log formatter matching the old Sanic logging format

from sanic.logging.auto_formatter import AutoFormatter


class LegacyFormatter(AutoFormatter):
    """
    The LegacyFormatter is used if you want to use the old style of logging.

    You can use it as follows, typically in conjunction with the
    LegacyAccessFormatter:

    .. code-block:: python

        from sanic.log import LOGGING_CONFIG_DEFAULTS

        LOGGING_CONFIG_DEFAULTS["formatters"] = {
            "generic": {
                "class": "sanic.logging.formatter.LegacyFormatter"
            },
            "access": {
                "class": "sanic.logging.formatter.LegacyAccessFormatter"
            },
        }
    """

    PREFIX_FORMAT = "%(asctime)s [%(process)s] [%(levelname)s] "
    DATE_FORMAT = "[%Y-%m-%d %H:%M:%S %z]"
