# ff:type feature=cli type=model
# ff:what Output CLI argument group for coffee, motd, verbosity, and noisy-exce
from sanic.cli.group import Group


class OutputGroup(Group):
    name = "Output"

    def attach(self, short: bool = False):
        if short:
            return

        self.add_bool_arguments(
            "--coffee",
            dest="coffee",
            default=False,
            help="Uhm, coffee?",
            negative_help="No coffee? Is that a typo?",
        )
        self.add_bool_arguments(
            "--motd",
            dest="motd",
            default=True,
            help="Show the startup display",
            negative_help="Disable the startup display",
        )
        self.container.add_argument(
            "-v",
            "--verbosity",
            action="count",
            help="Control logging noise, eg. -vv or --verbosity=2 [default 0]",
        )
        self.add_bool_arguments(
            "--noisy-exceptions",
            dest="noisy_exceptions",
            help="Output stack traces for all exceptions",
            default=None,
        )
