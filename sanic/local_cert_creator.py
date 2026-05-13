# ff:type feature=core type=constant
# ff:what Local TLS certificate creator enum (AUTO, TRUSTME, MKCERT)

from enum import auto

from sanic.compat import UpperStrEnum


class LocalCertCreator(UpperStrEnum):
    """Local certificate creator."""

    AUTO = auto()
    TRUSTME = auto()
    MKCERT = auto()
