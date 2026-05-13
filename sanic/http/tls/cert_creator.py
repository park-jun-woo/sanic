# ff:type feature=http type=builder
# ff:what Abstract base class for TLS certificate creators with auto-selection
from __future__ import annotations

import ssl

from abc import ABC, abstractmethod
from pathlib import Path
from tempfile import mkdtemp
from typing import TYPE_CHECKING

from sanic.constants import (
    DEFAULT_LOCAL_TLS_CERT,
    DEFAULT_LOCAL_TLS_KEY,
    LocalCertCreator,
)
from sanic.exceptions import SanicException
from sanic.helpers import Default
from sanic.http.tls._make_path import _make_path

if TYPE_CHECKING:
    from sanic import Sanic


class CertCreator(ABC):
    def __init__(self, app, key, cert) -> None:
        self.app = app
        self.key = key
        self.cert = cert
        self.tmpdir = None

        if isinstance(self.key, Default) or isinstance(self.cert, Default):
            self.tmpdir = Path(mkdtemp())

        key = (
            DEFAULT_LOCAL_TLS_KEY
            if isinstance(self.key, Default)
            else self.key
        )
        cert = (
            DEFAULT_LOCAL_TLS_CERT
            if isinstance(self.cert, Default)
            else self.cert
        )

        self.key_path = _make_path(key, self.tmpdir)
        self.cert_path = _make_path(cert, self.tmpdir)

    @abstractmethod
    def check_supported(self) -> None:  # no cov
        ...

    @abstractmethod
    def generate_cert(self, localhost: str) -> ssl.SSLContext:  # no cov
        ...

    @classmethod
    def select(
        cls,
        app: Sanic,
        cert_creator: LocalCertCreator,
        local_tls_key,
        local_tls_cert,
    ) -> CertCreator:
        import sys

        from sanic.http.tls.mkcert_creator import MkcertCreator
        from sanic.http.tls.trustme_creator import TrustmeCreator

        _creators = sys.modules.get("sanic.http.tls.creators")
        _MkcertCreator = (
            getattr(_creators, "MkcertCreator", MkcertCreator)
            if _creators
            else MkcertCreator
        )
        _TrustmeCreator = (
            getattr(_creators, "TrustmeCreator", TrustmeCreator)
            if _creators
            else TrustmeCreator
        )

        creator: CertCreator | None = None

        cert_creator_options: tuple[
            tuple[type[CertCreator], LocalCertCreator], ...
        ] = (
            (_MkcertCreator, LocalCertCreator.MKCERT),
            (_TrustmeCreator, LocalCertCreator.TRUSTME),
        )
        for creator_class, local_creator in cert_creator_options:
            creator = cls._try_select(
                app,
                creator,
                creator_class,
                local_creator,
                cert_creator,
                local_tls_key,
                local_tls_cert,
            )
            if creator:
                break

        if not creator:
            raise SanicException(
                "Sanic could not find package to create a TLS certificate. "
                "You must have either mkcert or trustme installed. See "
                "https://sanic.dev/en/guide/deployment/development.html"
                "#automatic-tls-certificate for more details."
            )

        return creator

    @staticmethod
    def _try_select(
        app: Sanic,
        creator: CertCreator | None,
        creator_class: type[CertCreator],
        creator_requirement: LocalCertCreator,
        creator_requested: LocalCertCreator,
        local_tls_key,
        local_tls_cert,
    ):
        if creator or (
            creator_requested is not LocalCertCreator.AUTO
            and creator_requested is not creator_requirement
        ):
            return creator

        instance = creator_class(app, local_tls_key, local_tls_cert)
        try:
            instance.check_supported()
        except SanicException:
            if creator_requested is creator_requirement:
                raise
            else:
                return None

        return instance
