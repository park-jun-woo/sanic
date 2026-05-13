# ff:func feature=logging type=util control=iteration dimension=1
# ff:what Replace AutoFormatter instances on logger handlers with the specified

import logging

from sanic.logging.auto_formatter import AutoFormatter


def _auto_format(
    logger: logging.Logger,
    auto_class: type[AutoFormatter],
    formatter_class: type[AutoFormatter],
) -> None:
    for handler in logger.handlers:
        if type(handler.formatter) is auto_class:
            handler.setFormatter(formatter_class())
