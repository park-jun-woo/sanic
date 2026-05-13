# ff:func feature=cli type=builder control=sequence
# ff:what Build the restart command parser with target arguments
from argparse import ArgumentParser

from sanic.cli._add_target_args import _add_target_args


def make_restart_parser(parser: ArgumentParser) -> None:
    _add_target_args(parser)
