# ff:type feature=cli type=model
# ff:what Abstract base class for Message of the Day display with logo, data, a

from abc import ABC, abstractmethod

from sanic.helpers import is_atty


class MOTD(ABC):
    """Base class for the Message of the Day (MOTD) display."""

    def __init__(
        self,
        logo: str | None,
        serve_location: str,
        data: dict[str, str],
        extra: dict[str, str],
    ) -> None:
        self.logo = logo
        self.serve_location = serve_location
        self.data = data
        self.extra = extra
        self.key_width = 0
        self.value_width = 0

    @abstractmethod
    def display(self):
        """Display the MOTD."""

    @classmethod
    def output(
        cls,
        logo: str | None,
        serve_location: str,
        data: dict[str, str],
        extra: dict[str, str],
    ) -> None:
        """Output the MOTD.

        Args:
            logo (Optional[str]): Logo to display.
            serve_location (str): Location to serve.
            data (Dict[str, str]): Data to display.
            extra (Dict[str, str]): Extra data to display.
        """
        from sanic.application.motd_basic import MOTDBasic
        from sanic.application.motd_tty import MOTDTTY

        motd_class = MOTDTTY if is_atty() else MOTDBasic
        motd_class(logo, serve_location, data, extra).display()
