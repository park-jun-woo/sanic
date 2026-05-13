# ff:func feature=cli type=builder control=sequence
# ff:what Add the command argument to the executor sub-parser
from argparse import ArgumentParser


def make_executor_parser(parser: ArgumentParser) -> None:
    parser.add_argument(
        "command",
        help="Command to execute",
    )
