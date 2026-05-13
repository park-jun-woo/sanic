# ff:func feature=http type=parser control=iteration dimension=1
# ff:what Parses RFC 7239 Forwarded headers to extract proxy information
from __future__ import annotations

import re

from sanic.headers.fwd_normalize import fwd_normalize

_token, _quoted = r"([\w!#$%&'*+\-.^_`|~]+)", r'"([^"]*)"'
Options = dict[str, int | str]
OptionsIterable = list[tuple[str, str]]

_rparam = re.compile(f"(?:{_token}|{_quoted})={_token}\\s*($|[;,])", re.ASCII)


def parse_forwarded(headers, config) -> Options | None:
    """Parse RFC 7239 Forwarded headers.
    The value of `by` or `secret` must match `config.FORWARDED_SECRET`
    :return: dict with keys and values, or None if nothing matched
    """
    header = headers.getall("forwarded", None)
    secret = config.FORWARDED_SECRET
    if header is None or not secret:
        return None
    header = ",".join(header)  # Join multiple header lines
    if secret not in header:
        return None
    # Loop over <separator><key>=<value> elements from right to left
    sep = pos = None
    options_list: OptionsIterable = []
    found = False
    for m in _rparam.finditer(header[::-1]):
        # Start of new element? (on parser skips and non-semicolon right sep)
        if (m.start() != pos or sep != ";") and found:
            break
        if m.start() != pos or sep != ";":
            del options_list[:]
        pos = m.end()
        val_token, val_quoted, key, sep = m.groups()
        key = key.lower()[::-1]
        val = (val_token or val_quoted.replace('"\\', '"'))[::-1]
        options_list.append((key, val))
        if key in ("secret", "by") and val == secret:
            found = True
        # Check if we would return on next round, to avoid useless parse
        if found and sep != ";":
            break
    # If secret was found, return the matching options in left-to-right order
    return fwd_normalize(reversed(options_list)) if found else None
