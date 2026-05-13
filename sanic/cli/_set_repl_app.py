# ff:func feature=cli type=handler control=sequence
# ff:what Set the global REPL app reference

from __future__ import annotations

from sanic import Sanic


def _set_repl_app(app: Sanic) -> None:
    import sanic.cli.console as _console

    _console.repl_app = app
