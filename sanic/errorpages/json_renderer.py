# ff:type feature=error type=formatter
# ff:what Renders exception responses as JSON
from __future__ import annotations

import sys

from traceback import extract_tb
from typing import TYPE_CHECKING

from sanic.errorpages.base_renderer import BaseRenderer
from sanic.helpers import STATUS_CODES
from sanic.response import json

if TYPE_CHECKING:
    from sanic import HTTPResponse


class JSONRenderer(BaseRenderer):
    """Render an exception as JSON."""

    def full(self) -> HTTPResponse:
        output = self._generate_output(full=True)
        return json(output, dumps=self.dumps)

    def minimal(self) -> HTTPResponse:
        output = self._generate_output(full=False)
        return json(output, dumps=self.dumps)

    def _generate_output(self, *, full):
        output = {
            "description": self.title,
            "status": self.status,
            "message": self.text,
        }

        for attr, display in (("context", True), ("extra", bool(full))):
            info = getattr(self.exception, attr, None)
            if info and display:
                output[attr] = info

        if full:
            _, exc_value, __ = sys.exc_info()
            exceptions = []

            while exc_value:
                exceptions.append(
                    {
                        "type": exc_value.__class__.__name__,
                        "exception": str(exc_value),
                        "frames": [
                            {
                                "file": frame.filename,
                                "line": frame.lineno,
                                "name": frame.name,
                                "src": frame.line,
                            }
                            for frame in extract_tb(exc_value.__traceback__)
                        ],
                    }
                )
                exc_value = exc_value.__cause__

            output["path"] = self.request.path
            output["args"] = self.request.args
            output["exceptions"] = exceptions[::-1]

        return output

    @property
    def title(self):
        return STATUS_CODES.get(self.status, b"Error Occurred").decode()
