# ff:type feature=asgi type=handler
# ff:what ASGI lifespan handler for server startup and shutdown events
from __future__ import annotations

import warnings

from sanic.helpers import Default
from sanic.log import error_logger, logger
from sanic.models.asgi import ASGIReceive, ASGIScope, ASGISend


class Lifespan:
    def __init__(
        self, sanic_app, scope: ASGIScope, receive: ASGIReceive, send: ASGISend
    ) -> None:
        self.sanic_app = sanic_app
        self.scope = scope
        self.receive = receive
        self.send = send

        if "server.init.before" in self.sanic_app.signal_router.name_index:
            logger.debug(
                'You have set a listener for "before_server_start" '
                "in ASGI mode. "
                "It will be executed as early as possible, but not before "
                "the ASGI server is started.",
                extra={"verbosity": 1},
            )
        if "server.shutdown.after" in self.sanic_app.signal_router.name_index:
            logger.debug(
                'You have set a listener for "after_server_stop" '
                "in ASGI mode. "
                "It will be executed as late as possible, but not after "
                "the ASGI server is stopped.",
                extra={"verbosity": 1},
            )

    async def startup(self) -> None:
        """
        Gather the listeners to fire on server start.
        Because we are using a third-party server and not Sanic server, we do
        not have access to fire anything BEFORE the server starts.
        Therefore, we fire before_server_start and after_server_start
        in sequence since the ASGI lifespan protocol only supports a single
        startup event.
        """
        await self.sanic_app._startup()
        await self.sanic_app._server_event("init", "before")
        await self.sanic_app._server_event("init", "after")

        if not isinstance(self.sanic_app.config.USE_UVLOOP, Default):
            warnings.warn(
                "You have set the USE_UVLOOP configuration option, but Sanic "
                "cannot control the event loop when running in ASGI mode."
                "This option will be ignored."
            )

    async def shutdown(self) -> None:
        """
        Gather the listeners to fire on server stop.
        Because we are using a third-party server and not Sanic server, we do
        not have access to fire anything AFTER the server stops.
        Therefore, we fire before_server_stop and after_server_stop
        in sequence since the ASGI lifespan protocol only supports a single
        shutdown event.
        """
        await self.sanic_app._server_event("shutdown", "before")
        await self.sanic_app._server_event("shutdown", "after")

    async def __call__(self) -> None:
        while True:
            message = await self.receive()
            if message["type"] == "lifespan.startup":
                try:
                    await self.startup()
                except Exception as e:
                    error_logger.exception(e)
                    await self.send(
                        {"type": "lifespan.startup.failed", "message": str(e)}
                    )
                else:
                    await self.send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                try:
                    await self.shutdown()
                except Exception as e:
                    error_logger.exception(e)
                    await self.send(
                        {"type": "lifespan.shutdown.failed", "message": str(e)}
                    )
                else:
                    await self.send({"type": "lifespan.shutdown.complete"})
                return
