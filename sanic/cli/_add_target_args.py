# ff:func feature=cli type=builder control=sequence
# ff:what Add mutually exclusive --pid and --pidfile target arguments to parser
from argparse import ArgumentParser


def _add_target_args(parser: ArgumentParser) -> None:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--pid",
        type=int,
        metavar="PID",
        help="Process ID of the daemon",
    )
    group.add_argument(
        "--pidfile",
        type=str,
        metavar="PATH",
        help="Path to PID file of the daemon",
    )
