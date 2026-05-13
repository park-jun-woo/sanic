# ff:func feature=http type=util control=sequence
# ff:what Checks if a given header name is an HTTP entity header
_ENTITY_HEADERS = frozenset(
    [
        "allow",
        "content-encoding",
        "content-language",
        "content-length",
        "content-location",
        "content-md5",
        "content-range",
        "content-type",
        "expires",
        "last-modified",
        "extension-header",
    ]
)


def is_entity_header(header):
    """Checks if the given header is an Entity Header"""
    return header.lower() in _ENTITY_HEADERS
