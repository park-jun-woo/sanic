# ff:func feature=cli type=builder control=sequence
# ff:what Build the kill command parser with target arguments
from argparse import ArgumentParser

from sanic.cli._add_target_args import _add_target_args


def make_kill_parser(parser: ArgumentParser) -> None:
    """Kill command always sends SIGKILL."""
    _add_target_args(parser)
