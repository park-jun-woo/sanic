# ff:type feature=cli type=model
# ff:what HTTP version CLI argument group for selecting HTTP/1.1 or HTTP/3
from sanic.cli.group import Group
from sanic.http.constants import HTTP


class HTTPVersionGroup(Group):
    name = "HTTP version"

    def attach(self, short: bool = False):
        if short:
            return

        http_values = [http.value for http in HTTP.__members__.values()]

        self.container.add_argument(
            "--http",
            dest="http",
            action="append",
            choices=http_values,
            type=int,
            help=(
                "Which HTTP version to use: HTTP/1.1 or HTTP/3. Value should\n"
                "be either 1, or 3. [default 1]"
            ),
        )
        self.container.add_argument(
            "-1",
            dest="http",
            action="append_const",
            const=1,
            help=("Run Sanic server using HTTP/1.1"),
        )
        self.container.add_argument(
            "-3",
            dest="http",
            action="append_const",
            const=3,
            help=("Run Sanic server using HTTP/3"),
        )

    def prepare(self, args):
        if not args.http:
            args.http = [1]
        args.http = tuple(sorted(set(map(HTTP, args.http)), reverse=True))
