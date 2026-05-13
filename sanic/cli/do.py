# ff:func feature=cli type=handler control=sequence
# ff:what Execute a full REPL HTTP request cycle and return the Result tuple
from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from sanic.cli.make_request import make_request
from sanic.cli.respond import respond
from sanic.cli.result import Result


async def do(
    url: str = "/",
    headers: dict[str, Any] | Sequence[tuple[str, str]] | None = None,
    method: str = "GET",
    body: str | None = None,
) -> Result:
    request = make_request(url, headers, method, body)
    response = await respond(request)
    return Result(request, response)
