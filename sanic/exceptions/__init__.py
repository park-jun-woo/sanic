from sanic.exceptions.bad_request import BadRequest, BadURL, InvalidUsage
from sanic.exceptions.expectation_failed import (
    ExpectationFailed,
    HeaderExpectationFailed,
)
from sanic.exceptions.file_not_found import FileNotFound
from sanic.exceptions.forbidden import Forbidden
from sanic.exceptions.header_not_found import HeaderNotFound
from sanic.exceptions.http_exception import HTTPException
from sanic.exceptions.invalid_header import InvalidHeader
from sanic.exceptions.invalid_range_type import InvalidRangeType
from sanic.exceptions.invalid_signal import InvalidSignal
from sanic.exceptions.load_file_exception import LoadFileException
from sanic.exceptions.method_not_allowed import (
    MethodNotAllowed,
    MethodNotSupported,
)
from sanic.exceptions.not_found import NotFound
from sanic.exceptions.payload_too_large import PayloadTooLarge
from sanic.exceptions.py_file_error import PyFileError
from sanic.exceptions.range_not_satisfiable import (
    ContentRangeError,
    RangeNotSatisfiable,
)
from sanic.exceptions.request_cancelled import RequestCancelled
from sanic.exceptions.request_timeout import RequestTimeout
from sanic.exceptions.sanic_exception import SanicException
from sanic.exceptions.server_error import InternalServerError, ServerError
from sanic.exceptions.server_killed import ServerKilled
from sanic.exceptions.service_unavailable import ServiceUnavailable
from sanic.exceptions.unauthorized import Unauthorized
from sanic.exceptions.url_build_error import URLBuildError
from sanic.exceptions.websocket_closed import WebsocketClosed

__all__ = [
    "BadRequest",
    "BadURL",
    "ContentRangeError",
    "ExpectationFailed",
    "FileNotFound",
    "Forbidden",
    "HTTPException",
    "HeaderExpectationFailed",
    "HeaderNotFound",
    "InternalServerError",
    "InvalidHeader",
    "InvalidRangeType",
    "InvalidSignal",
    "InvalidUsage",
    "LoadFileException",
    "MethodNotAllowed",
    "MethodNotSupported",
    "NotFound",
    "PayloadTooLarge",
    "PyFileError",
    "RangeNotSatisfiable",
    "RequestCancelled",
    "RequestTimeout",
    "SanicException",
    "ServerError",
    "ServerKilled",
    "ServiceUnavailable",
    "Unauthorized",
    "URLBuildError",
    "WebsocketClosed",
]

# Preserve the original module path in repr for all exception classes
# so that str(cls) shows "sanic.exceptions.Foo" instead of
# "sanic.exceptions.sub_module.Foo" after the file-split refactoring.
for _cls in list(locals().values()):
    if isinstance(_cls, type) and issubclass(_cls, BaseException):
        _cls.__module__ = __name__
