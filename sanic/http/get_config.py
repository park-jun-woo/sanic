# ff:func feature=http type=config control=sequence
# ff:what Build QUIC configuration from app settings and SSL context for HTTP/3
from __future__ import annotations

from ssl import SSLContext
from typing import TYPE_CHECKING, cast

from sanic.constants import LocalCertCreator
from sanic.exceptions import SanicException
from sanic.http.tls.context import CertSelector, SanicSSLContext

try:
    from aioquic.h0.connection import H0_ALPN
    from aioquic.h3.connection import H3_ALPN
    from aioquic.quic.configuration import QuicConfiguration

    HTTP3_AVAILABLE = True
except ModuleNotFoundError:  # no cov
    HTTP3_AVAILABLE = False

if TYPE_CHECKING:
    from sanic import Sanic


def get_config(app: Sanic, ssl: SanicSSLContext | CertSelector | SSLContext):
    # TODO:
    # - proper selection needed if service with multiple certs insted of
    #   just taking the first
    if isinstance(ssl, CertSelector):
        ssl = cast(SanicSSLContext, ssl.sanic_select[0])
    if app.config.LOCAL_CERT_CREATOR is LocalCertCreator.TRUSTME:
        raise SanicException(
            "Sorry, you cannot currently use trustme as a local certificate "
            "generator for an HTTP/3 server. This is not yet supported. You "
            "should be able to use mkcert instead. For more information, see: "
            "https://github.com/aiortc/aioquic/issues/295."
        )
    if not isinstance(ssl, SanicSSLContext):
        raise SanicException("SSLContext is not SanicSSLContext")

    config = QuicConfiguration(
        alpn_protocols=H3_ALPN + H0_ALPN + ["siduck"],
        is_client=False,
        max_datagram_frame_size=65536,
    )
    password = app.config.TLS_CERT_PASSWORD or None

    config.load_cert_chain(
        ssl.sanic["cert"], ssl.sanic["key"], password=password
    )

    return config
