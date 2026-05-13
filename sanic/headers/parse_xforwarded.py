# ff:func feature=http type=parser control=sequence
# ff:what Parses traditional X-Forwarded proxy headers
from __future__ import annotations

from sanic.headers._resolve_addr import _resolve_addr
from sanic.headers.fwd_normalize import fwd_normalize

Options = dict[str, int | str]


def parse_xforwarded(headers, config) -> Options | None:
    """Parse traditional proxy headers."""
    addr = _resolve_addr(headers, config)
    # No processing of other headers if no address is found
    if not addr:
        return None

    def options():
        yield "for", addr
        for key, header in (
            ("proto", "x-scheme"),
            ("proto", "x-forwarded-proto"),  # Overrides X-Scheme if present
            ("host", "x-forwarded-host"),
            ("port", "x-forwarded-port"),
            ("path", "x-forwarded-path"),
        ):
            yield key, headers.getone(header, None)

    return fwd_normalize(options())
