# ff:type feature=touchup type=model
# ff:what Touchup scheme that removes unnecessary signal dispatch calls based o

from ast import NodeTransformer

from .base import BaseScheme
from .remove_dispatch import RemoveDispatch


class OptionalDispatchEvent(BaseScheme):
    ident = "ODE"
    SYNC_SIGNAL_NAMESPACES = "http."

    def __init__(self, app) -> None:
        super().__init__(app)

        self._sync_events()
        self._registered_events = [
            signal.name for signal in app.signal_router.routes
        ]

    def visitors(self) -> list[NodeTransformer]:
        return [RemoveDispatch(self._registered_events)]

    def _sync_events(self):
        all_events = set()
        app_events = {}
        for app in self.app.__class__._app_registry.values():
            if app.state.server_info:
                app_events[app] = {
                    signal.name for signal in app.signal_router.routes
                }
                all_events.update(app_events[app])

        for app, events in app_events.items():
            missing = {
                x
                for x in all_events.difference(events)
                if any(x.startswith(y) for y in self.SYNC_SIGNAL_NAMESPACES)
            }
            if not missing:
                continue
            was_finalized = app.signal_router.finalized
            if was_finalized:  # no cov
                app.signal_router.reset()
            for event in missing:
                app.signal(event)(self.noop)
            if was_finalized:  # no cov
                app.signal_router.finalize()

    @staticmethod
    async def noop(**_):  # no cov
        ...
