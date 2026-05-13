# ff:type feature=worker type=handler
# ff:what Certificate loader that resolves SSL context from various input forma
from __future__ import annotations

import os

from ssl import SSLContext
from typing import TYPE_CHECKING, cast

from sanic.http.tls.context import process_to_context
from sanic.http.tls.creators import MkcertCreator, TrustmeCreator

if TYPE_CHECKING:
    from sanic import Sanic as SanicApp


class CertLoader:
    _creators = {
        "mkcert": MkcertCreator,
        "trustme": TrustmeCreator,
    }

    def __init__(
        self,
        ssl_data: SSLContext | dict[str, str | os.PathLike] | None,
    ):
        self._ssl_data = ssl_data
        self._creator_class = None
        if not ssl_data or not isinstance(ssl_data, dict):
            return

        creator_name = cast(str, ssl_data.get("creator"))

        self._creator_class = self._creators.get(creator_name)
        if not creator_name:
            return

        if not self._creator_class:
            raise RuntimeError(f"Unknown certificate creator: {creator_name}")

        self._key = ssl_data["key"]
        self._cert = ssl_data["cert"]
        self._localhost = cast(str, ssl_data["localhost"])

    def load(self, app: SanicApp):
        if not self._creator_class:
            return process_to_context(self._ssl_data)

        creator = self._creator_class(app, self._key, self._cert)
        return creator.generate_cert(self._localhost)
