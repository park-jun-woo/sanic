from sanic.headers.accept_list import AcceptList
from sanic.headers.format_http1_response import (
    HeaderBytesIterable,
    format_http1_response,
)
from sanic.headers.fwd_normalize import fwd_normalize
from sanic.headers.fwd_normalize_address import fwd_normalize_address
from sanic.headers.matched import Matched
from sanic.headers.media_type import MediaType
from sanic.headers.parse_accept import parse_accept
from sanic.headers.parse_content_header import (
    HeaderIterable,
    Options,
    parse_content_header,
)
from sanic.headers.parse_credentials import parse_credentials
from sanic.headers.parse_forwarded import parse_forwarded
from sanic.headers.parse_host import parse_host
from sanic.headers.parse_xforwarded import parse_xforwarded

OptionsIterable = list[tuple[str, str]]

__all__ = [
    "AcceptList",
    "HeaderBytesIterable",
    "HeaderIterable",
    "Matched",
    "MediaType",
    "Options",
    "OptionsIterable",
    "format_http1_response",
    "fwd_normalize",
    "fwd_normalize_address",
    "parse_accept",
    "parse_content_header",
    "parse_credentials",
    "parse_forwarded",
    "parse_host",
    "parse_xforwarded",
]
