# ff:func feature=http type=util control=iteration dimension=1
# ff:what Match SSL certificate names against a received hostname for SNI selec
from __future__ import annotations

import ssl

from sanic.http.tls.cert_selector import CertSelector


def match_hostname(ctx: ssl.SSLContext | CertSelector, hostname: str) -> bool:
    """Match names from CertSelector against a received hostname."""
    # Local certs are considered trusted, so this can be less pedantic
    # and thus faster than the deprecated ssl.match_hostname function is.
    names = dict(getattr(ctx, "sanic", {})).get("names", [])
    hostname = hostname.lower()
    for name in names:
        if name.startswith("*.") and hostname.split(".", 1)[-1] == name[2:]:
            return True
        elif name == hostname:
            return True
    return False
