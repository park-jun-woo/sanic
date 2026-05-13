# ff:type feature=error type=formatter
# ff:what Renders exception responses as plain text
from __future__ import annotations

import sys

from traceback import extract_tb
from typing import TYPE_CHECKING

from sanic.errorpages.base_renderer import BaseRenderer
from sanic.response import text

if TYPE_CHECKING:
    from sanic import HTTPResponse


class TextRenderer(BaseRenderer):
    """Render an exception as plain text."""

    OUTPUT_TEXT = "{title}\n{bar}\n{text}\n\n{body}"
    SPACER = "  "

    def full(self) -> HTTPResponse:
        return text(
            self.OUTPUT_TEXT.format(
                title=self.title,
                text=self.text,
                bar=("=" * len(self.title)),
                body=self._generate_body(full=True),
            )
        )

    def minimal(self) -> HTTPResponse:
        return text(
            self.OUTPUT_TEXT.format(
                title=self.title,
                text=self.text,
                bar=("=" * len(self.title)),
                body=self._generate_body(full=False),
            )
        )

    @property
    def title(self):
        return f"⚠️ {super().title}"

    def _build_full_traceback(self):
        _, exc_value, __ = sys.exc_info()
        exceptions = []

        lines = [
            f"{self.exception.__class__.__name__}: {self.exception} while "
            f"handling path {self.request.path}",
            f"Traceback of {self.request.app.name} "
            "(most recent call last):\n",
        ]

        while exc_value:
            exceptions.append(self._format_exc(exc_value))
            exc_value = exc_value.__cause__

        lines += exceptions[::-1]
        return lines

    def _generate_body(self, *, full):
        lines = []
        if full:
            lines += self._build_full_traceback()

        for attr, display in (("context", True), ("extra", bool(full))):
            info = getattr(self.exception, attr, None)
            if info and display:
                lines += self._generate_object_display_list(info, attr)

        return "\n".join(lines)

    def _format_exc(self, exc):
        frames = "\n\n".join(
            [
                f"{self.SPACER * 2}File {frame.filename}, "
                f"line {frame.lineno}, in "
                f"{frame.name}\n{self.SPACER * 2}{frame.line}"
                for frame in extract_tb(exc.__traceback__)
            ]
        )
        return f"{self.SPACER}{exc.__class__.__name__}: {exc}\n{frames}"

    def _generate_object_display_list(self, obj, descriptor):
        lines = [f"\n{descriptor.title()}"]
        for key, value in obj.items():
            display = self.dumps(value)
            lines.append(f"{self.SPACER * 2}{key}: {display}")
        return lines
