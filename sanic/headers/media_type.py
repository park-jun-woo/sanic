# ff:type feature=http type=parser
# ff:what Representation of a media type as used in the Accept header
from __future__ import annotations


class MediaType:
    """A media type, as used in the Accept header.

    This class is a representation of a media type, as used in the Accept
    header. It encapsulates the type, subtype and any parameters, and
    provides methods for matching against other media types.

    Two separate methods are provided for searching the list:
    - 'match' for finding the most preferred match (wildcards supported)
    -  operator 'in' for checking explicit matches (wildcards as literals)

    Args:
        type_ (str): The type of the media type.
        subtype (str): The subtype of the media type.
        **params (str): Any parameters for the media type.
    """

    def __init__(
        self,
        type_: str,
        subtype: str,
        **params: str,
    ):
        self.type = type_
        self.subtype = subtype
        self.q = float(params.get("q", "1.0"))
        self.params = params
        self.mime = f"{type_}/{subtype}"
        self.key = (
            -1 * self.q,
            -1 * len(self.params),
            self.subtype == "*",
            self.type == "*",
        )

    def __repr__(self):
        return self.mime + "".join(f";{k}={v}" for k, v in self.params.items())

    def __eq__(self, other):
        """Check for mime (str or MediaType) identical type/subtype.
        Parameters such as q are not considered."""
        if isinstance(other, str):
            # Give a friendly reminder if str contains parameters
            if ";" in other:
                raise ValueError("Use match() to compare with parameters")
            return self.mime == other
        if isinstance(other, MediaType):
            # Ignore parameters silently with MediaType objects
            return self.mime == other.mime
        return NotImplemented

    def match(
        self,
        mime_with_params: str | MediaType,
    ) -> MediaType | None:
        """Match this media type against another media type.

        Check if this media type matches the given mime type/subtype.
        Wildcards are supported both ways on both type and subtype.
        If mime contains a semicolon, optionally followed by parameters,
        the parameters of the two media types must match exactly.

        .. note::
            Use the `==` operator instead to check for literal matches
            without expanding wildcards.


        Args:
            media_type (str): A type/subtype string to match.

        Returns:
            MediaType: Returns `self` if the media types are compatible.
            None: Returns `None` if the media types are not compatible.
        """
        mt = (
            MediaType._parse(mime_with_params)
            if isinstance(mime_with_params, str)
            else mime_with_params
        )
        return (
            self
            if (
                mt
                # All parameters given in the other media type must match
                and all(self.params.get(k) == v for k, v in mt.params.items())
                # Subtype match
                and (
                    self.subtype == mt.subtype
                    or self.subtype == "*"
                    or mt.subtype == "*"
                )
                # Type match
                and (
                    self.type == mt.type or self.type == "*" or mt.type == "*"
                )
            )
            else None
        )

    @property
    def has_wildcard(self) -> bool:
        """Return True if this media type has a wildcard in it.

        Returns:
            bool: True if this media type has a wildcard in it.
        """
        return any(part == "*" for part in (self.subtype, self.type))

    @classmethod
    def _parse(cls, mime_with_params: str) -> MediaType | None:
        mtype = mime_with_params.strip()
        if "/" not in mime_with_params:
            return None

        mime, *raw_params = mtype.split(";")
        type_, subtype = mime.split("/", 1)
        if not type_ or not subtype:
            raise ValueError(f"Invalid media type: {mtype}")

        params = {
            key.strip(): value.strip()
            for key, value in (param.split("=", 1) for param in raw_params)
        }

        return cls(type_.lstrip(), subtype.rstrip(), **params)
