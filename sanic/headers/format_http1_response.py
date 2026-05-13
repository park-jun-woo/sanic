# ff:func feature=http type=formatter control=iteration dimension=1
# ff:what Formats HTTP/1.1 response status line and headers into bytes
from __future__ import annotations

from collections.abc import Iterable

from sanic.helpers import STATUS_CODES

HeaderBytesIterable = Iterable[tuple[bytes, bytes]]

_HTTP1_STATUSLINES = [
    b"HTTP/1.1 %d %b\r\n" % (status, STATUS_CODES.get(status, b"UNKNOWN"))
    for status in range(1000)
]


def format_http1_response(status: int, headers: HeaderBytesIterable) -> bytes:
    """Format a HTTP/1.1 response header.

    Args:
        status (int): The HTTP status code.
        headers (HeaderBytesIterable): An iterable of header tuples.

    Returns:
        bytes: The formatted response header.
    """
    # Note: benchmarks show that here bytes concat is faster than bytearray,
    # b"".join() or %-formatting. %timeit any changes you make.
    ret = _HTTP1_STATUSLINES[status]
    for h in headers:
        ret += b"%b: %b\r\n" % h
    ret += b"\r\n"
    return ret
