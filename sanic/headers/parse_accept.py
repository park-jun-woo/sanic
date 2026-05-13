# ff:func feature=http type=parser control=sequence
# ff:what Parses Accept header value into an ordered AcceptList per RFC 7231
from __future__ import annotations

from sanic.exceptions import InvalidHeader
from sanic.headers.accept_list import AcceptList
from sanic.headers.media_type import MediaType


def parse_accept(accept: str | None) -> AcceptList:
    """Parse an Accept header and order the acceptable media types according to RFC 7231, s. 5.3.2

    https://datatracker.ietf.org/doc/html/rfc7231#section-5.3.2

    Args:
        accept (str): The Accept header value to parse.

    Returns:
        AcceptList: A list of MediaType objects, ordered by preference.

    Raises:
        InvalidHeader: If the header value is invalid.
    """  # noqa: E501
    if not accept:
        if accept == "":
            return AcceptList()  # Empty header, accept nothing
        accept = "*/*"  # No header means that all types are accepted
    try:
        a = [
            mt
            for mt in [MediaType._parse(mtype) for mtype in accept.split(",")]
            if mt
        ]
        if not a:
            raise ValueError
        return AcceptList(sorted(a, key=lambda x: x.key))
    except ValueError:
        raise InvalidHeader(f"Invalid header value in Accept: {accept}")
