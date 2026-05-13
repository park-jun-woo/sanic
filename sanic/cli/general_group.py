# ff:type feature=cli type=model
# ff:what General CLI argument group providing version and target positional ar
from sanic_routing import __version__ as __routing_version__

from sanic import __version__
from sanic.cli.group import Group
from sanic.compat import OS_IS_WINDOWS


class GeneralGroup(Group):
    name = None

    def attach(self, short: bool = False):
        if short:
            return

        self.container.add_argument(
            "--version",
            action="version",
            version=f"Sanic {__version__}; Routing {__routing_version__}",
        )

        self.container.add_argument(
            "target",
            help=(
                "Path to your Sanic app instance.\n"
                "\tExample: path.to.server:app\n"
                "If running a Simple Server, path to directory to serve.\n"
                "\tExample: ./\n"
                "Additionally, this can be a path to a factory function\n"
                "that returns a Sanic app instance.\n"
                "\tExample: path.to.server:create_app\n"
            ),
        )

        choices = ["serve", "exec"]
        help_text = (
            "Action to perform.\n"
            "\tserve: Run the Sanic app [default]\n"
            "\texec: Execute a command in the Sanic app context\n"
        )
        if not OS_IS_WINDOWS:
            choices.extend(["status", "restart", "stop"])
            help_text += (
                "\tstatus: Check if daemon is running\n"
                "\trestart: Restart daemon (future use)\n"
                "\tstop: Stop daemon gracefully\n"
            )
        self.container.add_argument(
            "action",
            nargs="?",
            default="serve",
            choices=choices,
            help=help_text,
        )
