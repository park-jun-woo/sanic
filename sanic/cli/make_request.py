# ff:func feature=cli type=handler control=sequence
# ff:what Create a mock Request object for REPL inline HTTP testing
from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from sanic import Request
from sanic.cli.repl_protocol import REPLProtocol
from sanic.compat import Header


def make_request(
    url: str = "/",
    headers: dict[str, Any] | Sequence[tuple[str, str]] | None = None,
    method: str = "GET",
    body: str | None = None,
):
    from sanic.cli.console import repl_app

    assert repl_app, "No Sanic app has been registered."
    headers = headers or {}
    protocol = REPLProtocol()
    request = Request(  # type: ignore
        url.encode(),
        Header(headers),
        "1.1",
        method,
        protocol,
        repl_app,
    )
    if body is not None:
        request.body = body.encode()
    request.stream = protocol  # type: ignore
    request.conn_info = None
    return request
