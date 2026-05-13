# ff:type feature=cli type=model
# ff:what Basic MOTD display for terminals without ANSI escape code support

from sanic import __version__
from sanic.application.motd_base import MOTD
from sanic.log import logger


class MOTDBasic(MOTD):
    """A basic MOTD display.

    This is used when the terminal does not support ANSI escape codes.
    """

    def display(self):
        if self.logo:
            logger.debug(self.logo)
        lines = [f"Sanic v{__version__}"]
        if self.serve_location:
            lines.append(f"Goin' Fast @ {self.serve_location}")
        lines += [
            *(f"{key}: {value}" for key, value in self.data.items()),
            *(f"{key}: {value}" for key, value in self.extra.items()),
        ]
        for line in lines:
            logger.info(line)
