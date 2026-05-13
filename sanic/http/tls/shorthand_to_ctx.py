# ff:func feature=http type=resolver control=sequence
# ff:what Convert an ssl argument shorthand (str, dict, SSLContext) to an SSLCo
from __future__ import annotations

import ssl

from sanic.http.tls.cert_simple import CertSimple
from sanic.http.tls.load_cert_dir import load_cert_dir


def shorthand_to_ctx(
    ctxdef: None | ssl.SSLContext | dict | str,
) -> ssl.SSLContext | None:
    """Convert an ssl argument shorthand to an SSLContext object."""
    if ctxdef is None or isinstance(ctxdef, ssl.SSLContext):
        return ctxdef
    if isinstance(ctxdef, str):
        return load_cert_dir(ctxdef)
    if isinstance(ctxdef, dict):
        return CertSimple(**ctxdef)
    raise ValueError(
        f"Invalid ssl argument {type(ctxdef)}."
        " Expecting a list of certdirs, a dict or an SSLContext."
    )
