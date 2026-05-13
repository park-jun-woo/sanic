# ff:func feature=http type=builder control=sequence
# ff:what Create an SSL context with secure TLS 1.2+ ciphers and HTTP/1.1 ALPN
from __future__ import annotations

import ssl

from sanic.http.tls.server_name_callback import server_name_callback

# Only allow secure ciphers, notably leaving out AES-CBC mode
# OpenSSL chooses ECDSA or RSA depending on the cert in use
CIPHERS_TLS12 = [
    "ECDHE-ECDSA-CHACHA20-POLY1305",
    "ECDHE-ECDSA-AES256-GCM-SHA384",
    "ECDHE-ECDSA-AES128-GCM-SHA256",
    "ECDHE-RSA-CHACHA20-POLY1305",
    "ECDHE-RSA-AES256-GCM-SHA384",
    "ECDHE-RSA-AES128-GCM-SHA256",
]


def create_context(
    certfile: str | None = None,
    keyfile: str | None = None,
    password: str | None = None,
    purpose: ssl.Purpose = ssl.Purpose.CLIENT_AUTH,
) -> ssl.SSLContext:
    """Create a context with secure crypto and HTTP/1.1 in protocols."""
    context = ssl.create_default_context(purpose=purpose)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.set_ciphers(":".join(CIPHERS_TLS12))
    context.set_alpn_protocols(["http/1.1"])
    if purpose is ssl.Purpose.CLIENT_AUTH:
        context.sni_callback = server_name_callback
    if certfile and keyfile:
        context.load_cert_chain(certfile, keyfile, password)
    return context
