# ff:func feature=http type=parser control=sequence
# ff:what Splits host:port string into hostname and port components
from __future__ import annotations

import re

_ipv6 = "(?:[0-9A-Fa-f]{0,4}:){2,7}[0-9A-Fa-f]{0,4}"
_host_re = re.compile(
    r"((?:\[" + _ipv6 + r"\])|[a-zA-Z0-9.\-]{1,253})(?::(\d{1,5}))?"
)


def parse_host(host: str) -> tuple[str | None, int | None]:
    """Split host:port into hostname and port.

    Args:
        host (str): A host string.

    Returns:
        Tuple[Optional[str], Optional[int]]: A tuple of hostname and port.
    """
    m = _host_re.fullmatch(host)
    if not m:
        return None, None
    host, port = m.groups()
    return host.lower(), int(port) if port is not None else None
