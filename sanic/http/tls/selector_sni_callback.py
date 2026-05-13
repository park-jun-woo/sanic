# ff:func feature=http type=handler control=sequence
# ff:what SNI callback that selects the appropriate certificate for a TLS conne
from __future__ import annotations

import ssl

from sanic.http.tls.cert_selector import CertSelector
from sanic.http.tls.find_cert import find_cert
from sanic.http.tls.server_name_callback import server_name_callback
from sanic.log import logger


def selector_sni_callback(
    sslobj: ssl.SSLObject, server_name: str, ctx: CertSelector
) -> int | None:
    """Select a certificate matching the SNI."""
    # Call server_name_callback to store the SNI on sslobj
    server_name_callback(sslobj, server_name, ctx)
    # Find a new context matching the hostname
    try:
        sslobj.context = find_cert(ctx, server_name)
    except ValueError as e:
        logger.warning(f"Rejecting TLS connection: {e}")
        # This would show ERR_SSL_UNRECOGNIZED_NAME_ALERT on client side if
        # asyncio/uvloop did proper SSL shutdown. They don't.
        return ssl.ALERT_DESCRIPTION_UNRECOGNIZED_NAME
    return None  # mypy complains without explicit return
