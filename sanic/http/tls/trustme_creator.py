# ff:type feature=http type=builder
# ff:what TLS certificate creator using trustme for local development
import ssl
import sys

from types import ModuleType

from sanic.exceptions import SanicException
from sanic.http.tls.cert_creator import CertCreator
from sanic.http.tls.sanic_ssl_context import SanicSSLContext

try:
    import trustme

    TRUSTME_INSTALLED = True
except (ImportError, ModuleNotFoundError):
    trustme = ModuleType("trustme")
    TRUSTME_INSTALLED = False


_TRUSTME_NOT_INSTALLED_MSG = (
    "Sanic is attempting to use trustme to generate local TLS "
    "certificates since you did not supply a certificate, but "
    "one is required. Sanic cannot proceed since trustme does not "
    "appear to be installed. Alternatively, you can use mkcert. "
    "Please install mkcert, trustme, or supply TLS certificates "
    "to proceed. Installation instructions can be found here: "
    "https://github.com/python-trio/trustme.\n"
    "Find out more information about your options here: "
    "https://sanic.dev/en/guide/deployment/development.html#"
    "automatic-tls-certificate"
)


class TrustmeCreator(CertCreator):
    def check_supported(self) -> None:
        _mod = (
            sys.modules.get("sanic.http.tls.creators") or sys.modules[__name__]
        )
        if not getattr(_mod, "TRUSTME_INSTALLED", TRUSTME_INSTALLED):
            raise SanicException(_TRUSTME_NOT_INSTALLED_MSG)

    def generate_cert(self, localhost: str) -> ssl.SSLContext:
        _mod = (
            sys.modules.get("sanic.http.tls.creators") or sys.modules[__name__]
        )
        _trustme = getattr(_mod, "trustme", trustme)

        context = SanicSSLContext.create_from_ssl_context(
            ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        )
        context.sanic = {
            "cert": self.cert_path.absolute(),
            "key": self.key_path.absolute(),
        }
        ca = _trustme.CA()
        server_cert = ca.issue_cert(localhost)
        server_cert.configure_cert(context)
        ca.configure_trust(context)

        ca.cert_pem.write_to_path(str(self.cert_path.absolute()))
        server_cert.private_key_and_cert_chain_pem.write_to_path(
            str(self.key_path.absolute())
        )
        context.sanic["creator"] = "trustme"
        context.sanic["localhost"] = localhost

        return context
