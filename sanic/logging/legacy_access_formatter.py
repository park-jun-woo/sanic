# ff:type feature=logging type=formatter
# ff:what Legacy-style access log formatter matching the old Sanic access log f

from sanic.logging.auto_access_formatter import AutoAccessFormatter


class LegacyAccessFormatter(AutoAccessFormatter):
    """
    The LegacyFormatter is used if you want to use the old style of logging.

    You can use it as follows, typically in conjunction with the
    LegacyFormatter:

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

    PREFIX_FORMAT = "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
    MESSAGE_FORMAT = "%(request)s %(message)s %(status)s %(byte)s"
