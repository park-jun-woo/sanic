# ff:func feature=cli type=handler control=sequence
# ff:what Execute an in-process request against the REPL app and return the res
from sanic.response.types import HTTPResponse


async def respond(request) -> HTTPResponse:
    from sanic.cli.console import repl_app, repl_response

    assert repl_app, "No Sanic app has been registered."
    await repl_app.handle_request(request)
    assert repl_response
    return repl_response
