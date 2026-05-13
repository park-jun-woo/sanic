# ff:type feature=http type=parser
# ff:what Ordered list of media types from the Accept header with preference ma
from __future__ import annotations

from sanic.headers.matched import Matched


class AcceptList(list):
    """A list of media types, as used in the Accept header.

    The Accept header entries are listed in order of preference, starting
    with the most preferred. This class is a list of `MediaType` objects,
    that encapsulate also the q value or any other parameters.

    Two separate methods are provided for searching the list:
    - 'match' for finding the most preferred match (wildcards supported)
    -  operator 'in' for checking explicit matches (wildcards as literals)

    Args:
        *args (MediaType): Any number of MediaType objects.
    """

    def match(self, *mimes: str, accept_wildcards=True) -> Matched:
        """Find a media type accepted by the client.

        This method can be used to find which of the media types requested by
        the client is most preferred against the ones given as arguments.

        The ordering of preference is set by:
        1. The order set by RFC 7231, s. 5.3.2, giving a higher priority
            to q values and more specific type definitions,
        2. The order of the arguments (first is most preferred), and
        3. The first matching entry on the Accept header.

        Wildcards are matched both ways. A match is usually found, as the
        Accept headers typically include `*/*`, in particular if the header
        is missing, is not manually set, or if the client is a browser.

        Note: the returned object behaves as a string of the mime argument
        that matched, and is empty/falsy if no match was found. The matched
        header entry `MediaType` or `None` is available as the `m` attribute.

        Args:
            mimes (List[str]): Any MIME types to search for in order of preference.
            accept_wildcards (bool): Match Accept entries with wildcards in them.

        Returns:
            Match: A match object with the mime string and the MediaType object.
        """  # noqa: E501
        a = sorted(
            (-acc.q, i, j, mime, acc)
            for j, acc in enumerate(self)
            if accept_wildcards or not acc.has_wildcard
            for i, mime in enumerate(mimes)
            if acc.match(mime)
        )
        return Matched(*(a[0][-2:] if a else ("", None)))

    def __str__(self):
        """Format as Accept header value (parsed, not original)."""
        return ", ".join(str(m) for m in self)
