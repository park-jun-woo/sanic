# F5 exempt: re-export hub
from sanic.http_method import HTTPMethod
from sanic.local_cert_creator import LocalCertCreator

HTTP_METHODS = tuple(HTTPMethod.__members__.values())
SAFE_HTTP_METHODS = (HTTPMethod.GET, HTTPMethod.HEAD, HTTPMethod.OPTIONS)
IDEMPOTENT_HTTP_METHODS = (
    HTTPMethod.GET,
    HTTPMethod.HEAD,
    HTTPMethod.PUT,
    HTTPMethod.DELETE,
    HTTPMethod.OPTIONS,
)
CACHEABLE_HTTP_METHODS = (HTTPMethod.GET, HTTPMethod.HEAD)
DEFAULT_HTTP_CONTENT_TYPE = "application/octet-stream"
DEFAULT_LOCAL_TLS_KEY = "key.pem"
DEFAULT_LOCAL_TLS_CERT = "cert.pem"

__all__ = (
    "CACHEABLE_HTTP_METHODS",
    "DEFAULT_HTTP_CONTENT_TYPE",
    "DEFAULT_LOCAL_TLS_CERT",
    "DEFAULT_LOCAL_TLS_KEY",
    "HTTPMethod",
    "HTTP_METHODS",
    "IDEMPOTENT_HTTP_METHODS",
    "LocalCertCreator",
    "SAFE_HTTP_METHODS",
)
