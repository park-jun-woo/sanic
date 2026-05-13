# ff:func feature=http type=parser control=sequence
# ff:what Normalizes address fields of proxy headers
from __future__ import annotations

import re

_ipv6 = "(?:[0-9A-Fa-f]{0,4}:){2,7}[0-9A-Fa-f]{0,4}"
_ipv6_re = re.compile(_ipv6)


def fwd_normalize_address(addr: str) -> str:
    """Normalize address fields of proxy headers.

    Args:
        addr (str): An address string.

    Returns:
        str: A normalized address string.
    """
    if addr == "unknown":
        raise ValueError()  # omit unknown value identifiers
    if addr.startswith("_"):
        return addr  # do not lower-case obfuscated strings
    if _ipv6_re.fullmatch(addr):
        addr = f"[{addr}]"  # bracket IPv6
    return addr.lower()
