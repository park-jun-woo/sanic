# ff:type feature=http type=parser
# ff:what Matching result of a MIME string against an Accept header entry
from __future__ import annotations

from typing import Any

from sanic.headers.media_type import MediaType


class Matched:
    """A matching result of a MIME string against a header.

    This class is a representation of a matching result of a MIME string
    against a header. It encapsulates the MIME string, the header, and
    provides methods for matching against other MIME strings.

    Args:
        mime (str): The MIME string to match.
        header (MediaType): The header to match against, if any.
    """

    def __init__(self, mime: str, header: MediaType | None):
        self.mime = mime
        self.header = header

    def __repr__(self):
        return f"<{self} matched {self.header}>" if self else "<no match>"

    def __str__(self):
        return self.mime

    def __bool__(self):
        return self.header is not None

    def __eq__(self, other: Any) -> bool:
        try:
            comp, other_accept = self._compare(other)
        except TypeError:
            return False

        return bool(
            comp
            and (
                (self.header and other_accept.header)
                or (not self.header and not other_accept.header)
            )
        )

    def _compare(self, other) -> tuple[bool, Matched]:
        if isinstance(other, str):
            parsed = Matched.parse(other)
            if self.mime == other:
                return True, parsed
            other = parsed

        if isinstance(other, Matched):
            return self.header == other.header, other

        raise TypeError(
            "Comparison not supported between unequal "
            f"mime types of '{self.mime}' and '{other}'"
        )

    def match(self, other: str | Matched) -> Matched | None:
        """Match this MIME string against another MIME string.

        Check if this MIME string matches the given MIME string. Wildcards are supported both ways on both type and subtype.

        Args:
            other (str): A MIME string to match.

        Returns:
            Matched: Returns `self` if the MIME strings are compatible.
            None: Returns `None` if the MIME strings are not compatible.
        """  # noqa: E501
        accept = Matched.parse(other) if isinstance(other, str) else other
        if not self.header or not accept.header:
            return None
        if self.header.match(accept.header):
            return accept
        return None

    @classmethod
    def parse(cls, raw: str) -> Matched:
        media_type = MediaType._parse(raw)
        return cls(raw, media_type)
