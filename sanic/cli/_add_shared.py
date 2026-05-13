# ff:func feature=cli type=builder control=sequence
# ff:what Add shared inspector arguments (host, port, secure, api-key, raw) to
from argparse import ArgumentParser


def _add_shared(parser: ArgumentParser) -> None:
    parser.add_argument(
        "--host",
        "-H",
        default="localhost",
        help="Inspector host address [default 127.0.0.1]",
    )
    parser.add_argument(
        "--port",
        "-p",
        default=6457,
        type=int,
        help="Inspector port [default 6457]",
    )
    parser.add_argument(
        "--secure",
        "-s",
        action="store_true",
        help="Whether to access the Inspector via TLS encryption",
    )
    parser.add_argument("--api-key", "-k", help="Inspector authentication key")
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Whether to output the raw response information",
    )
