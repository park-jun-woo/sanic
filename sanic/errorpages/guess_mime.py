# ff:func feature=error type=resolver control=sequence
# ff:what Guesses the MIME type for error responses based on the request
from __future__ import annotations

from typing import TYPE_CHECKING

from sanic.exceptions import BadRequest
from sanic.log import deprecation, logger

if TYPE_CHECKING:
    from sanic import Request

JSON = "application/json"

MIME_BY_CONFIG = {
    "text": "text/plain",
    "json": "application/json",
    "html": "text/html",
}
CONFIG_BY_MIME = {v: k for k, v in MIME_BY_CONFIG.items()}


def guess_mime(req: Request, fallback: str) -> str:
    """Guess the MIME type for the response based upon the request."""

    def _detect_json_format(req, formats, name):
        if JSON in req.accept:
            formats["json"] = "request.accept"
        elif JSON in req.headers.getone("content-type", ""):
            formats["json"] = "content-type"
        else:
            c = None
            try:
                c = req.json
            except BadRequest:
                pass
            if c:
                formats["json"] = "request.json"
                deprecation(
                    "Response type was determined by the JSON content "
                    "of the request. This behavior is deprecated and "
                    "will be removed in v24.3. Please specify the "
                    "format either by\n"
                    f'  error_format="json" on route {name}, by\n'
                    '  FALLBACK_ERROR_FORMAT = "json", or by adding '
                    "header\n"
                    "  accept: application/json to your requests.",
                    24.3,
                )

    # Attempt to find a suitable MIME format for the response.
    # Insertion-ordered map of formats["html"] = "source of that suggestion"
    formats = {}
    name = ""
    # Route error_format (by magic from handler code if auto, the default)
    if req.route:
        name = req.route.name
        f = req.route.extra.error_format
        if f in MIME_BY_CONFIG:
            formats[f] = name

    if not formats and fallback in MIME_BY_CONFIG:
        formats[fallback] = "FALLBACK_ERROR_FORMAT"

    # If still not known, check for the request for clues of JSON
    if not formats and fallback == "auto" and req.accept.match(JSON):
        _detect_json_format(req, formats, name)

    # Any other supported formats
    if fallback == "auto":
        for k in MIME_BY_CONFIG:
            formats.setdefault(k, "any")

    mimes = [MIME_BY_CONFIG[k] for k in formats]
    m = req.accept.match(*mimes)
    if m:
        format = CONFIG_BY_MIME[m.mime]
        source = formats[format]
        logger.debug(
            "Error Page: The client accepts %s, using '%s' from %s",
            m.header,
            format,
            source,
        )
    else:
        logger.debug(
            "Error Page: No format found, the client accepts %s",
            repr(req.accept),
        )
    return m.mime
