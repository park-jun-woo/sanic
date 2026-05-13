# ff:type feature=http type=config
# ff:what SSL context subclass that carries Sanic-specific certificate metadata
from __future__ import annotations

import os
import ssl


class SanicSSLContext(ssl.SSLContext):
    sanic: dict[str, os.PathLike]

    @classmethod
    def create_from_ssl_context(cls, context: ssl.SSLContext):
        context.__class__ = cls
        return context
