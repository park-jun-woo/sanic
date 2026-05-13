# ff:type feature=http type=config
# ff:what SSLContext wrapper that creates context from cert/key file paths with
from __future__ import annotations

import ssl

from typing import Any

from sanic.http.tls.create_context import create_context
from sanic.http.tls.sanic_ssl_context import SanicSSLContext


class CertSimple(SanicSSLContext):
    """A wrapper for creating SSLContext with a sanic attribute."""

    sanic: dict[str, Any]

    def __new__(cls, cert, key, **kw):
        # try common aliases, rename to cert/key
        certfile = kw["cert"] = kw.pop("certificate", None) or cert
        keyfile = kw["key"] = kw.pop("keyfile", None) or key
        password = kw.get("password", None)
        if not certfile or not keyfile:
            raise ValueError("SSL dict needs filenames for cert and key.")
        subject = {}
        if "names" not in kw:
            cert = ssl._ssl._test_decode_cert(certfile)  # type: ignore
            kw["names"] = [
                name
                for t, name in cert["subjectAltName"]
                if t in ["DNS", "IP Address"]
            ]
            subject = {k: v for item in cert["subject"] for k, v in item}
        self = create_context(certfile, keyfile, password)
        self.__class__ = cls
        self.sanic = {**subject, **kw}
        return self

    def __init__(self, cert, key, **kw):
        pass  # Do not call super().__init__ because it is already initialized
