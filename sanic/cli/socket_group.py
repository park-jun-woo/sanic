# ff:type feature=cli type=model
# ff:what Socket binding CLI argument group for host, port and unix socket opti
from sanic.cli.group import Group
from sanic.compat import OS_IS_WINDOWS


class SocketGroup(Group):
    name = "Socket binding"

    def attach(self, short: bool = False):
        self.container.add_argument(
            "-H",
            "--host",
            dest="host",
            type=str,
            help="Host address [default 127.0.0.1]",
        )
        self.container.add_argument(
            "-p",
            "--port",
            dest="port",
            type=int,
            help="Port to serve on [default 8000]",
        )
        if not OS_IS_WINDOWS and not short:
            self.container.add_argument(
                "-u",
                "--unix",
                dest="unix",
                type=str,
                default="",
                help="location of UNIX socket",
            )
