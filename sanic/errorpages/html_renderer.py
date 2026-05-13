# ff:type feature=error type=formatter
# ff:what Renders exception responses as HTML pages
from __future__ import annotations

from typing import TYPE_CHECKING

from sanic.errorpages.base_renderer import BaseRenderer
from sanic.pages.error import ErrorPage
from sanic.response import html

if TYPE_CHECKING:
    from sanic import HTTPResponse


class HTMLRenderer(BaseRenderer):
    """Render an exception as HTML.

    The default fallback type.
    """

    def full(self) -> HTTPResponse:
        page = ErrorPage(
            debug=self.debug,
            title=super().title,
            text=super().text,
            request=self.request,
            exc=self.exception,
        )
        return html(page.render())

    def minimal(self) -> HTTPResponse:
        return self.full()
