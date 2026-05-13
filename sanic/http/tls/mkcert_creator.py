# ff:type feature=http type=builder
# ff:what TLS certificate creator using mkcert for local development
import ssl
import subprocess
import sys

from contextlib import suppress

from sanic.application.loading import loading
from sanic.exceptions import SanicException
from sanic.http.tls.cert_creator import CertCreator
from sanic.http.tls.cert_simple import CertSimple
from sanic.http.tls.sanic_ssl_context import SanicSSLContext


class MkcertCreator(CertCreator):
    def check_supported(self) -> None:
        try:
            subprocess.run(  # nosec B603 B607
                ["mkcert", "-help"],
                check=True,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
            )
        except Exception as e:
            raise SanicException(
                "Sanic is attempting to use mkcert to generate local TLS "
                "certificates since you did not supply a certificate, but "
                "one is required. Sanic cannot proceed since mkcert does not "
                "appear to be installed. Alternatively, you can use trustme. "
                "Please install mkcert, trustme, or supply TLS certificates "
                "to proceed. Installation instructions can be found here: "
                "https://github.com/FiloSottile/mkcert.\n"
                "Find out more information about your options here: "
                "https://sanic.dev/en/guide/deployment/development.html#"
                "automatic-tls-certificate"
            ) from e

    def generate_cert(self, localhost: str) -> ssl.SSLContext:
        try:
            if not self.cert_path.exists():
                message = "Generating TLS certificate"
                # TODO: Validate input for security
                with loading(message):
                    cmd = [
                        "mkcert",
                        "-key-file",
                        str(self.key_path),
                        "-cert-file",
                        str(self.cert_path),
                        localhost,
                    ]
                    resp = subprocess.run(  # nosec B603
                        cmd,
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                    )
                sys.stdout.write("\r" + " " * (len(message) + 4))
                sys.stdout.flush()
                sys.stdout.write(resp.stdout)
        finally:

            @self.app.main_process_stop
            async def cleanup(*_):  # no cov
                if self.tmpdir:
                    with suppress(FileNotFoundError):
                        self.key_path.unlink()
                        self.cert_path.unlink()
                    self.tmpdir.rmdir()

        _mod = (
            sys.modules.get("sanic.http.tls.creators") or sys.modules[__name__]
        )
        _CertSimple = getattr(_mod, "CertSimple", CertSimple)
        context = _CertSimple(self.cert_path, self.key_path)
        context.sanic["creator"] = "mkcert"
        context.sanic["localhost"] = localhost
        SanicSSLContext.create_from_ssl_context(context)

        return context
