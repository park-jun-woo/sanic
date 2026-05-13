# ff:func feature=cli type=handler control=sequence
# ff:what Set the global REPL response reference

from __future__ import annotations

from sanic.response.types import HTTPResponse


def _set_repl_response(response: HTTPResponse) -> None:
    import sanic.cli.console as _console

    _console.repl_response = response
