# ff:func feature=http type=resolver control=sequence
# ff:what Process app.run ssl argument from easy formats to full SSLContext
from __future__ import annotations

import ssl

from sanic.http.tls.cert_selector import CertSelector
from sanic.http.tls.shorthand_to_ctx import shorthand_to_ctx


def process_to_context(
    ssldef: None | ssl.SSLContext | dict | str | list | tuple,
) -> ssl.SSLContext | None:
    """Process app.run ssl argument from easy formats to full SSLContext."""
    return (
        CertSelector(map(shorthand_to_ctx, ssldef))
        if isinstance(ssldef, (list, tuple))
        else shorthand_to_ctx(ssldef)
    )
