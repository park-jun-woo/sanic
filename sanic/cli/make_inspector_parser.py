# ff:func feature=cli type=builder control=sequence
# ff:what Build the inspector argument parser with shared args and sub-commands
from argparse import ArgumentParser

from sanic.cli._add_shared import _add_shared
from sanic.cli.inspector_sub_parser import InspectorSubParser
from sanic.cli.sanic_help_formatter import SanicHelpFormatter
from sanic.cli.sanic_sub_parsers_action import SanicSubParsersAction


def make_inspector_parser(parser: ArgumentParser) -> None:
    _add_shared(parser)
    subparsers = parser.add_subparsers(
        action=SanicSubParsersAction,
        dest="action",
        description=(
            "Run one or none of the below subcommands. Using inspect without "
            "a subcommand will fetch general information about the state "
            "of the application instance.\n\n"
            "Or, you can optionally follow inspect with a subcommand. "
            "If you have created a custom "
            "Inspector instance, then you can run custom commands. See "
            "https://sanic.dev/en/guide/deployment/inspector.html "
            "for more details."
        ),
        title="  Subcommands",
        parser_class=InspectorSubParser,
    )
    reloader = subparsers.add_parser(
        "reload",
        help="Trigger a reload of the server workers",
        formatter_class=SanicHelpFormatter,
    )
    reloader.add_argument(
        "--zero-downtime",
        action="store_true",
        help=(
            "Whether to wait for the new process to be online before "
            "terminating the old"
        ),
    )
    subparsers.add_parser(
        "shutdown",
        help="Shutdown the application and all processes",
        formatter_class=SanicHelpFormatter,
    )
    scale = subparsers.add_parser(
        "scale",
        help="Scale the number of workers",
        formatter_class=SanicHelpFormatter,
    )
    scale.add_argument(
        "replicas",
        type=int,
        help="Number of workers requested",
    )

    custom = subparsers.add_parser(
        "<custom>",
        help="Run a custom command",
        description=(
            "keyword arguments:\n  When running a custom command, you can "
            "add keyword arguments by appending them to your command\n\n"
            "\tsanic inspect foo --one=1 --two=2"
        ),
        formatter_class=SanicHelpFormatter,
    )
    custom.add_argument(
        "positional",
        nargs="*",
        help="Add one or more non-keyword args to your custom command",
    )
