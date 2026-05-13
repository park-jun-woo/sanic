# ff:func feature=http type=resolver control=iteration dimension=1
# ff:what Find the first certificate matching a given SNI server name
from __future__ import annotations

from sanic.http.tls.cert_selector import CertSelector
from sanic.http.tls.match_hostname import match_hostname


def find_cert(self: CertSelector, server_name: str):
    """Find the first certificate that matches the given SNI.

    :raises ssl.CertificateError: No matching certificate found.
    :return: A matching ssl.SSLContext object if found."""
    if not server_name:
        if self.sanic_fallback:
            return self.sanic_fallback
        raise ValueError(
            "The client provided no SNI to match for certificate."
        )
    for ctx in self.sanic_select:
        if match_hostname(ctx, server_name):
            return ctx
    if self.sanic_fallback:
        return self.sanic_fallback
    raise ValueError(f"No certificate found matching hostname {server_name!r}")
