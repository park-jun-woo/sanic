# ff:func feature=http type=util control=sequence
# ff:what Checks if a given header name is an HTTP hop-by-hop header
_HOP_BY_HOP_HEADERS = frozenset(
    [
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailers",
        "transfer-encoding",
        "upgrade",
    ]
)


def is_hop_by_hop_header(header):
    """Checks if the given header is a Hop By Hop header"""
    return header.lower() in _HOP_BY_HOP_HEADERS
