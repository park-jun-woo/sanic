# F5 exempt: re-export hub
from __future__ import annotations

from sanic import Sanic
from sanic.cli._set_repl_app import _set_repl_app
from sanic.cli._set_repl_response import _set_repl_response
from sanic.cli._variable_description import _variable_description
from sanic.cli.do import do
from sanic.cli.make_request import make_request
from sanic.cli.repl_protocol import REPLProtocol
from sanic.cli.respond import respond
from sanic.cli.result import Result
from sanic.cli.sanic_repl import SanicREPL
from sanic.response.types import HTTPResponse

repl_app: Sanic | None = None
repl_response: HTTPResponse | None = None

__all__ = (
    "REPLProtocol",
    "Result",
    "SanicREPL",
    "_set_repl_app",
    "_set_repl_response",
    "_variable_description",
    "do",
    "make_request",
    "repl_app",
    "repl_response",
    "respond",
)
