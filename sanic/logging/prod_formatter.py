# ff:type feature=logging type=formatter
# ff:what Production log formatter for non-debug environments

from sanic.logging.auto_formatter import AutoFormatter


class ProdFormatter(AutoFormatter):
    """
    The ProdFormatter is used for production environments.

    It can be used directly, or it will be automatically selected if the
    environment is set up for production and is using the AutoFormatter.
    """
