# ff:func feature=http type=resolver control=sequence
# ff:what Get or auto-create an SSL context, falling back to local cert generat
from __future__ import annotations

import ssl

from typing import TYPE_CHECKING, cast

from sanic.application.constants import Mode
from sanic.constants import LocalCertCreator
from sanic.exceptions import SanicException
from sanic.http.tls.cert_creator import CertCreator

if TYPE_CHECKING:
    from sanic import Sanic


def get_ssl_context(app: Sanic, ssl: ssl.SSLContext | None) -> ssl.SSLContext:
    if ssl:
        return ssl

    if app.state.mode is Mode.PRODUCTION:
        raise SanicException(
            "Cannot run Sanic as an HTTPS server in PRODUCTION mode "
            "without passing a TLS certificate. If you are developing "
            "locally, please enable DEVELOPMENT mode and Sanic will "
            "generate a localhost TLS certificate. For more information "
            "please see: https://sanic.dev/en/guide/deployment/development."
            "html#automatic-tls-certificate."
        )

    creator = CertCreator.select(
        app,
        cast(LocalCertCreator, app.config.LOCAL_CERT_CREATOR),
        app.config.LOCAL_TLS_KEY,
        app.config.LOCAL_TLS_CERT,
    )
    context = creator.generate_cert(app.config.LOCALHOST)
    return context
