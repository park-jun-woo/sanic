# ff:type feature=cli type=protocol
# ff:what Minimal transport protocol for REPL request/response handling
from sanic.http.constants import Stage
from sanic.models.protocol_types import TransportProtocol


class REPLProtocol(TransportProtocol):
    def __init__(self):
        self.stage = Stage.IDLE
        self.request_body = True

    def respond(self, response):
        from sanic.cli.console import _set_repl_response

        _set_repl_response(response)
        response.stream = self
        return response

    async def send(self, data, end_stream): ...
