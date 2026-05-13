# ff:type feature=cli type=model
# ff:what Development CLI argument group for debug, auto-reload, and dev mode o
from sanic.cli.group import Group


class DevelopmentGroup(Group):
    name = "Development"

    def _attach_full(self):
        self.container.add_argument(
            "--debug",
            dest="debug",
            action="store_true",
            help="Run the server in debug mode",
        )
        self.container.add_argument(
            "-r",
            "--reload",
            "--auto-reload",
            dest="auto_reload",
            action="store_true",
            help="Auto-reload on source changes",
        )
        self.container.add_argument(
            "-R",
            "--reload-dir",
            dest="path",
            action="append",
            help="Additional directories to watch for changes",
        )

    def attach(self, short: bool = False):
        if not short:
            self._attach_full()
        self.container.add_argument(
            "-d",
            "--dev",
            dest="dev",
            action="store_true",
            help="Run in development mode (debug + auto-reload)",
        )
        if not short:
            self.container.add_argument(
                "--auto-tls",
                dest="auto_tls",
                action="store_true",
                help=(
                    "Create a temporary TLS certificate for local development "
                    "(requires mkcert or trustme)"
                ),
            )
