from sanic.errorpages._get_renderers import RENDERERS_BY_CONTENT_TYPE
from sanic.errorpages.base_renderer import (
    FALLBACK_STATUS,
    FALLBACK_TEXT,
    BaseRenderer,
)
from sanic.errorpages.check_error_format import (
    MIME_BY_CONFIG,
    check_error_format,
)
from sanic.errorpages.escape import escape
from sanic.errorpages.exception_response import exception_response
from sanic.errorpages.guess_mime import CONFIG_BY_MIME, guess_mime
from sanic.errorpages.html_renderer import HTMLRenderer
from sanic.errorpages.json_renderer import JSONRenderer
from sanic.errorpages.text_renderer import TextRenderer

DEFAULT_FORMAT = "auto"

RESPONSE_MAPPING = {
    "json": "json",
    "text": "text",
    "html": "html",
    "JSONResponse": "json",
    "text/plain": "text",
    "text/html": "html",
    "application/json": "json",
}

__all__ = [
    "BaseRenderer",
    "CONFIG_BY_MIME",
    "DEFAULT_FORMAT",
    "FALLBACK_STATUS",
    "FALLBACK_TEXT",
    "HTMLRenderer",
    "JSONRenderer",
    "MIME_BY_CONFIG",
    "RENDERERS_BY_CONTENT_TYPE",
    "RESPONSE_MAPPING",
    "TextRenderer",
    "check_error_format",
    "escape",
    "exception_response",
    "guess_mime",
]
