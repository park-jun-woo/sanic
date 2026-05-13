# ff:type feature=http type=config
# ff:what SSL context that automatically selects certificates based on SNI host
from __future__ import annotations

import ssl

from collections.abc import Iterable

from sanic.log import logger


class CertSelector(ssl.SSLContext):
    """Automatically select SSL certificate based on the hostname that the
    client is trying to access, via SSL SNI. Paths to certificate folders
    with privkey.pem and fullchain.pem in them should be provided, and
    will be matched in the order given whenever there is a new connection.
    """

    def __new__(cls, ctxs):
        return super().__new__(cls)

    def __init__(self, ctxs: Iterable[ssl.SSLContext | None]):
        super().__init__()
        from sanic.http.tls.selector_sni_callback import selector_sni_callback

        self.sni_callback = selector_sni_callback  # type: ignore
        self.sanic_select = []
        self.sanic_fallback = None
        all_names = []
        for i, ctx in enumerate(ctxs):
            if not ctx:
                continue
            names = dict(getattr(ctx, "sanic", {})).get("names", [])
            all_names += names
            self.sanic_select.append(ctx)
            if i == 0:
                self.sanic_fallback = ctx
        if not all_names:
            raise ValueError(
                "No certificates with SubjectAlternativeNames found."
            )
        logger.info(f"Certificate vhosts: {', '.join(all_names)}")
