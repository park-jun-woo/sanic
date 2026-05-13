# ff:func feature=logging type=util control=iteration dimension=1
# ff:what Configure logging formatters for all loggers based on debug mode and

import os

from sanic.helpers import Default, _default
from sanic.log import (
    access_logger,
    error_logger,
    logger,
    server_logger,
    websockets_logger,
)
from sanic.logging._auto_format import _auto_format
from sanic.logging.auto_access_formatter import AutoAccessFormatter
from sanic.logging.auto_formatter import AutoFormatter
from sanic.logging.debug_access_formatter import DebugAccessFormatter
from sanic.logging.debug_formatter import DebugFormatter
from sanic.logging.prod_access_formatter import ProdAccessFormatter
from sanic.logging.prod_formatter import ProdFormatter


def setup_logging(
    debug: bool,
    no_color: bool = False,
    log_extra: bool | Default = _default,
) -> None:
    if AutoFormatter.SETUP:
        return

    if isinstance(log_extra, Default):
        log_extra = debug
        os.environ["SANIC_LOG_EXTRA"] = str(log_extra)
    AutoFormatter.LOG_EXTRA = log_extra

    if no_color:
        os.environ["SANIC_NO_COLOR"] = str(no_color)
        AutoFormatter.NO_COLOR = no_color

    AutoFormatter.SETUP = True

    for lggr in (logger, server_logger, error_logger, websockets_logger):
        _auto_format(
            lggr,
            AutoFormatter,
            DebugFormatter if debug else ProdFormatter,
        )
    _auto_format(
        access_logger,
        AutoAccessFormatter,
        DebugAccessFormatter if debug else ProdAccessFormatter,
    )
