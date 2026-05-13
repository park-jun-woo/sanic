# ff:type feature=blueprint type=builder
# ff:what Blueprint class for modular grouping of routes, middleware, and handl
from __future__ import annotations

import asyncio

from collections import defaultdict
from collections.abc import Iterable, Sequence
from copy import deepcopy
from itertools import chain
from types import SimpleNamespace
from typing import (
    TYPE_CHECKING,
    Any,
)

from sanic_routing.exceptions import NotFound
from sanic_routing.route import Route

from sanic.base.root import BaseSanic
from sanic.blueprints.lazy import lazy
from sanic.exceptions import SanicException
from sanic.helpers import Default, _default
from sanic.models.futures import FutureRoute, FutureSignal, FutureStatic
from sanic.models.handler_types import (
    ListenerType,
    MiddlewareType,
    RouteHandler,
)

if TYPE_CHECKING:
    from sanic import Sanic
    from sanic.blueprints.blueprint_group import BlueprintGroup


class Blueprint(BaseSanic):
    """A logical collection of URLs that consist of a similar logical domain.

    A Blueprint object is the main tool for grouping functionality and similar endpoints. It allows the developer to
    organize routes, exception handlers, middleware, and other web functionalities into separate, modular groups.

    See [Blueprints](/en/guide/best-practices/blueprints) for more information.

    Args:
        name (str): The name of the blueprint.
        url_prefix (Optional[str]): The URL prefix for all routes defined on this blueprint.
        host (Optional[Union[List[str], str]]): Host or list of hosts that this blueprint should respond to.
        version (Optional[Union[int, str, float]]): Version number of the API implemented by this blueprint.
        strict_slashes (Optional[bool]): Whether or not the URL should end with a slash.
        version_prefix (str): Prefix for the version. Default is "/v".
    """  # noqa: E501

    __slots__ = (
        "_apps",
        "_future_commands",
        "_future_routes",
        "_future_statics",
        "_future_middleware",
        "_future_listeners",
        "_future_exceptions",
        "_future_signals",
        "_allow_route_overwrite",
        "copied_from",
        "ctx",
        "exceptions",
        "host",
        "listeners",
        "middlewares",
        "routes",
        "statics",
        "strict_slashes",
        "url_prefix",
        "version",
        "version_prefix",
        "websocket_routes",
    )

    def __init__(
        self,
        name: str,
        url_prefix: str | None = None,
        host: list[str] | str | None = None,
        version: int | str | float | None = None,
        strict_slashes: bool | None = None,
        version_prefix: str = "/v",
    ):
        super().__init__(name=name)
        self.reset()
        self._allow_route_overwrite = False
        self.copied_from = ""
        self.ctx = SimpleNamespace()
        self.host = host
        self.strict_slashes = strict_slashes
        self.url_prefix = (
            url_prefix[:-1]
            if url_prefix and url_prefix.endswith("/")
            else url_prefix
        )
        self.version = version
        self.version_prefix = version_prefix

    def __repr__(self) -> str:
        args = ", ".join(
            [
                (
                    f'{attr}="{getattr(self, attr)}"'
                    if isinstance(getattr(self, attr), str)
                    else f"{attr}={getattr(self, attr)}"
                )
                for attr in (
                    "name",
                    "url_prefix",
                    "host",
                    "version",
                    "strict_slashes",
                )
            ]
        )
        return f"Blueprint({args})"

    @property
    def apps(self) -> set[Sanic]:
        """Get the set of apps that this blueprint is registered to.

        Returns:
            Set[Sanic]: Set of apps that this blueprint is registered to.

        Raises:
            SanicException: If the blueprint has not yet been registered to
                an app.
        """
        if not self._apps:
            raise SanicException(
                f"{self} has not yet been registered to an app"
            )
        return self._apps

    @property
    def registered(self) -> bool:
        """Check if the blueprint has been registered to an app.

        Returns:
            bool: `True` if the blueprint has been registered to an app,
                `False` otherwise.
        """
        return bool(self._apps)

    exception = lazy(BaseSanic.exception)
    listener = lazy(BaseSanic.listener)
    middleware = lazy(BaseSanic.middleware)
    route = lazy(BaseSanic.route)
    signal = lazy(BaseSanic.signal)
    static = lazy(BaseSanic.static, as_decorator=False)

    def reset(self) -> None:
        """Reset the blueprint to its initial state."""
        self._apps: set[Sanic] = set()
        self._allow_route_overwrite = False
        self.exceptions: list[RouteHandler] = []
        self.listeners: dict[str, list[ListenerType[Any]]] = {}
        self.middlewares: list[MiddlewareType] = []
        self.routes: list[Route] = []
        self.statics: list[RouteHandler] = []
        self.websocket_routes: list[Route] = []

    def copy(
        self,
        name: str,
        url_prefix: str | Default | None = _default,
        version: int | str | float | Default | None = _default,
        version_prefix: str | Default = _default,
        allow_route_overwrite: bool | Default = _default,
        strict_slashes: bool | Default | None = _default,
        with_registration: bool = True,
        with_ctx: bool = False,
    ):
        """Copy a blueprint instance with some optional parameters to override the values of attributes in the old instance.

        Args:
            name (str): Unique name of the blueprint.
            url_prefix (Optional[Union[str, Default]]): URL to be prefixed before all route URLs.
            version (Optional[Union[int, str, float, Default]]): Blueprint version.
            version_prefix (Union[str, Default]): The prefix of the version number shown in the URL.
            allow_route_overwrite (Union[bool, Default]): Whether to allow route overwrite or not.
            strict_slashes (Optional[Union[bool, Default]]): Enforce the API URLs are requested with a trailing "/*".
            with_registration (bool): Whether to register the new blueprint instance with Sanic apps that were registered with the old instance or not. Default is `True`.
            with_ctx (bool): Whether the ``ctx`` will be copied or not. Default is `False`.

        Returns:
            Blueprint: A new Blueprint instance with the specified attributes.
        """  # noqa: E501

        attrs_backup = {
            "_apps": self._apps,
            "routes": self.routes,
            "websocket_routes": self.websocket_routes,
            "middlewares": self.middlewares,
            "exceptions": self.exceptions,
            "listeners": self.listeners,
            "statics": self.statics,
        }

        self.reset()
        new_bp = deepcopy(self)
        new_bp.name = name
        new_bp.copied_from = self.name

        if not isinstance(url_prefix, Default):
            new_bp.url_prefix = url_prefix
        if not isinstance(version, Default):
            new_bp.version = version
        if not isinstance(strict_slashes, Default):
            new_bp.strict_slashes = strict_slashes
        if not isinstance(version_prefix, Default):
            new_bp.version_prefix = version_prefix
        if not isinstance(allow_route_overwrite, Default):
            new_bp._allow_route_overwrite = allow_route_overwrite

        for key, value in attrs_backup.items():
            setattr(self, key, value)

        if with_registration and self._apps:
            if new_bp._future_statics:
                raise SanicException(
                    "Static routes registered with the old blueprint instance,"
                    " cannot be registered again."
                )
            for app in self._apps:
                app.blueprint(new_bp)

        if not with_ctx:
            new_bp.ctx = SimpleNamespace()

        return new_bp

    @staticmethod
    def group(
        *blueprints: Blueprint | BlueprintGroup,
        url_prefix: str | None = None,
        version: int | str | float | None = None,
        strict_slashes: bool | None = None,
        version_prefix: str = "/v",
        name_prefix: str | None = "",
    ) -> BlueprintGroup:
        """Group multiple blueprints (or other blueprint groups) together.

        Gropuping blueprings is a method for modularizing and organizing
        your application's code. This can be a powerful tool for creating
        reusable components, logically structuring your application code,
        and easily maintaining route definitions in bulk.

        This is the preferred way to group multiple blueprints together.

        Args:
            blueprints (Union[Blueprint, BlueprintGroup]): Blueprints to be
                registered as a group.
            url_prefix (Optional[str]): URL route to be prepended to all
                sub-prefixes. Default is `None`.
            version (Optional[Union[int, str, float]]): API Version to be
                used for Blueprint group. Default is `None`.
            strict_slashes (Optional[bool]): Indicate strict slash
                termination behavior for URL. Default is `None`.
            version_prefix (str): Prefix to be used for the version in the
                URL. Default is "/v".
            name_prefix (Optional[str]): Prefix to be used for the name of
                the blueprints in the group. Default is an empty string.

        Returns:
            BlueprintGroup: A group of blueprints.

        Example:
            The resulting group will have the URL prefixes
            `'/v2/bp1'` and `'/v2/bp2'` for bp1 and bp2, respectively.
            ```python
            bp1 = Blueprint('bp1', url_prefix='/bp1')
            bp2 = Blueprint('bp2', url_prefix='/bp2')
            group = group(bp1, bp2, version=2)
            ```
        """
        from sanic.blueprints.blueprint_group import BlueprintGroup

        def chain_nested(nested) -> Iterable[Blueprint]:
            """Iterate through nested blueprints"""
            for i in nested:
                if isinstance(i, (list, tuple)):
                    yield from chain_nested(i)
                else:
                    yield i

        bps = BlueprintGroup(
            url_prefix=url_prefix,
            version=version,
            strict_slashes=strict_slashes,
            version_prefix=version_prefix,
            name_prefix=name_prefix,
        )
        for bp in chain_nested(blueprints):
            bps.append(bp)
        return bps

    def register(self, app, options):
        """Register the blueprint to the sanic app.

        Args:
            app (Sanic): Sanic app to register the blueprint to.
            options (dict): Options to be passed to the blueprint.
        """

        self._apps.add(app)
        url_prefix = options.get("url_prefix", self.url_prefix)
        opt_version = options.get("version", None)
        opt_strict_slashes = options.get("strict_slashes", None)
        opt_version_prefix = options.get("version_prefix", self.version_prefix)
        opt_name_prefix = options.get("name_prefix", None)
        error_format = options.get(
            "error_format", app.config.FALLBACK_ERROR_FORMAT
        )

        routes = []
        middleware = []
        exception_handlers = []
        listeners = defaultdict(list)
        registered = set()

        # Routes
        route_opts = (
            url_prefix,
            error_format,
            opt_version_prefix,
            opt_version,
            opt_strict_slashes,
            opt_name_prefix,
        )
        for future in self._future_routes:
            result = self._register_future_route(
                future,
                app,
                *route_opts,
                registered,
            )
            if isinstance(result, list):
                routes.extend(result)
            elif result is not None:
                routes.append(result)

        # Static Files
        for future in self._future_statics:
            # Prepend the blueprint URI prefix if available
            uri = self._setup_uri(future.uri, url_prefix)
            apply_route = FutureStatic(uri, *future[1:])

            if (self, apply_route) in app._future_registry:
                continue

            registered.add(apply_route)
            route = app._apply_static(apply_route)
            routes.append(route)

        route_names = [route.name for route in routes if route]

        # Middleware
        for future in self._future_middleware:
            if not route_names or (self, future) in app._future_registry:
                continue
            middleware.append(app._apply_middleware(future, route_names))

        # Exceptions
        for future in self._future_exceptions:
            if not route_names or (self, future) in app._future_registry:
                continue
            exception_handlers.append(
                app._apply_exception_handler(future, route_names)
            )

        # Event listeners
        for future in self._future_listeners:
            if (self, future) in app._future_registry:
                continue
            listeners[future.event].append(app._apply_listener(future))

        # Signals
        for future in self._future_signals:
            self._register_future_signal(future, app)

        self.routes += [route for route in routes if isinstance(route, Route)]
        self.websocket_routes += [
            route for route in self.routes if route.extra.websocket
        ]
        self.middlewares += middleware
        self.exceptions += exception_handlers
        self.listeners.update(dict(listeners))

        if self.registered:
            self._register_all_futures(registered)

        if self._future_commands:
            raise SanicException(
                "Registering commands with blueprints is not supported."
            )

    def _register_all_futures(self, registered):
        self.register_futures(
            self.apps,
            self,
            chain(
                registered,
                self._future_middleware,
                self._future_exceptions,
                self._future_listeners,
                self._future_signals,
            ),
        )

    def _register_future_signal(self, future, app):
        if (self, future) in app._future_registry:
            return
        future.condition.update({"__blueprint__": self.name})
        app._apply_signal(
            FutureSignal(
                future.handler,
                future.event,
                future.condition,
                False,
                future.priority,
            )
        )

    def _register_future_route(
        self,
        future,
        app,
        url_prefix,
        error_format,
        opt_version_prefix,
        opt_version,
        opt_strict_slashes,
        opt_name_prefix,
        registered,
    ):
        uri = self._setup_uri(future.uri, url_prefix)
        route_error_format = (
            future.error_format if future.error_format else error_format
        )

        version_prefix = self.version_prefix
        for prefix in (future.version_prefix, opt_version_prefix):
            if prefix and prefix != "/v":
                version_prefix = prefix
                break

        version = self._extract_value(
            future.version, opt_version, self.version
        )
        strict_slashes = self._extract_value(
            future.strict_slashes, opt_strict_slashes, self.strict_slashes
        )

        name = future.name
        if opt_name_prefix:
            name = f"{opt_name_prefix}_{future.name}"
        name = app.generate_name(name)
        host = future.host or self.host
        if isinstance(host, list):
            host = tuple(host)

        apply_route = FutureRoute(
            future.handler,
            uri,
            future.methods,
            host,
            strict_slashes,
            future.stream,
            version,
            name,
            future.ignore_body,
            future.websocket,
            future.subprotocols,
            future.unquote,
            future.static,
            version_prefix,
            route_error_format,
            future.route_context,
        )

        if (self, apply_route) in app._future_registry:
            return None

        registered.add(apply_route)
        route = app._apply_route(
            apply_route, overwrite=self._allow_route_overwrite
        )

        if self.copied_from:
            for r in route:
                r.name = r.name.replace(self.copied_from, self.name)
                r.extra.ident = r.extra.ident.replace(
                    self.copied_from, self.name
                )

        return route

    async def dispatch(self, *args, **kwargs):
        """Dispatch a signal event

        Args:
            *args: Arguments to be passed to the signal event.
            **kwargs: Keyword arguments to be passed to the signal event.
        """
        condition = kwargs.pop("condition", {})
        condition.update({"__blueprint__": self.name})
        kwargs["condition"] = condition
        return await asyncio.gather(
            *[app.dispatch(*args, **kwargs) for app in self.apps]
        )

    def event(
        self,
        event: str,
        timeout: int | float | None = None,
        *,
        condition: dict[str, Any] | None = None,
    ):
        """Wait for a signal event to be dispatched.

        Args:
            event (str): Name of the signal event.
            timeout (Optional[Union[int, float]]): Timeout for the event to be
                dispatched.
            condition: If provided, method will only return when the signal
                is dispatched with the given condition.

        Returns:
            Awaitable: Awaitable for the event to be dispatched.
        """
        if condition is None:
            condition = {}
        condition.update({"__blueprint__": self.name})

        waiters = []
        for app in self.apps:
            waiter = app.signal_router.get_waiter(
                event, condition, exclusive=False
            )
            if not waiter:
                raise NotFound("Could not find signal %s" % event)
            waiters.append(waiter)

        return self._event(waiters, timeout)

    async def _event(self, waiters, timeout):
        done, pending = await asyncio.wait(
            [asyncio.create_task(waiter.wait()) for waiter in waiters],
            return_when=asyncio.FIRST_COMPLETED,
            timeout=timeout,
        )
        for task in pending:
            task.cancel()
        if not done:
            raise TimeoutError()
        (finished_task,) = done
        return finished_task.result()

    @staticmethod
    def _extract_value(*values):
        value = values[-1]
        for v in values:
            if v is not None:
                value = v
                break
        return value

    @staticmethod
    def _setup_uri(base: str, prefix: str | None):
        uri = base
        if prefix:
            uri = prefix
            if base.startswith("/") and prefix.endswith("/"):
                uri += base[1:]
            else:
                uri += base

        return uri[1:] if uri.startswith("//") else uri

    @staticmethod
    def register_futures(
        apps: set[Sanic], bp: Blueprint, futures: Sequence[tuple[Any, ...]]
    ):
        """Register futures to the apps.

        Args:
            apps (Set[Sanic]): Set of apps to register the futures to.
            bp (Blueprint): Blueprint that the futures belong to.
            futures (Sequence[Tuple[Any, ...]]): Sequence of futures to be
                registered.
        """

        for app in apps:
            app._future_registry.update({(bp, item) for item in futures})
