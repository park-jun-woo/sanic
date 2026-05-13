# ff:func feature=error type=handler control=sequence
# ff:what Renders an HTTP response for the default exception handler
from __future__ import annotations

import typing as t

from sanic.errorpages._get_renderers import _get_renderers
from sanic.errorpages.base_renderer import BaseRenderer
from sanic.errorpages.guess_mime import guess_mime

if t.TYPE_CHECKING:
    from sanic import HTTPResponse, Request


def exception_response(
    request: Request,
    exception: Exception,
    debug: bool,
    fallback: str,
    base: t.Type[BaseRenderer],
    renderer: t.Optional[t.Type[BaseRenderer]] = None,
) -> HTTPResponse:
    """Render a response for the default FALLBACK exception handler."""
    if not renderer:
        mt = guess_mime(request, fallback)
        renderers = _get_renderers()
        renderer = renderers.get(mt, base)

    renderer = t.cast(t.Type[BaseRenderer], renderer)
    return renderer(request, exception, debug).render()
