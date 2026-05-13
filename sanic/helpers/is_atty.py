# ff:func feature=util type=util control=sequence
# ff:what Checks if stdout is connected to a terminal
import sys


def is_atty() -> bool:
    return bool(sys.stdout and sys.stdout.isatty())
