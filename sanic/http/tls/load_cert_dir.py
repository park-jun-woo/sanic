# ff:func feature=http type=resolver control=sequence
# ff:what Load SSL certificate and key from a directory containing PEM files
from __future__ import annotations

import os
import ssl

from sanic.http.tls.cert_simple import CertSimple


def load_cert_dir(p: str) -> ssl.SSLContext:
    if os.path.isfile(p):
        raise ValueError(f"Certificate folder expected but {p} is a file.")
    keyfile = os.path.join(p, "privkey.pem")
    certfile = os.path.join(p, "fullchain.pem")
    if not os.access(keyfile, os.R_OK):
        raise ValueError(
            f"Certificate not found or permission denied {keyfile}"
        )
    if not os.access(certfile, os.R_OK):
        raise ValueError(
            f"Certificate not found or permission denied {certfile}"
        )
    return CertSimple(certfile, keyfile)
