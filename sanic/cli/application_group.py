# ff:type feature=cli type=model
# ff:what Application CLI argument group for factory and simple server options
from sanic.cli.group import Group


class ApplicationGroup(Group):
    name = "Application"

    def attach(self, short: bool = False):
        if short:
            return

        group = self.container.add_mutually_exclusive_group()
        group.add_argument(
            "--factory",
            action="store_true",
            help=(
                "Treat app as an application factory, "
                "i.e. a () -> <Sanic app> callable"
            ),
        )
        group.add_argument(
            "-s",
            "--simple",
            dest="simple",
            action="store_true",
            help=(
                "Run Sanic as a Simple Server, and serve the contents of "
                "a directory\n(module arg should be a path)"
            ),
        )
        self.add_bool_arguments(
            "--repl",
            help="Run with an interactive shell session",
            negative_help="Disable interactive shell session",
        )
