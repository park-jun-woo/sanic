# ff:type feature=cli type=model
# ff:what Named tuple for REPL request/response result pair
from typing import NamedTuple

from sanic import Request
from sanic.response.types import HTTPResponse


class Result(NamedTuple):
    request: Request
    response: HTTPResponse
