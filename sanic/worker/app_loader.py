# ff:type feature=worker type=handler
# ff:what Application loader that resolves and imports Sanic app instances from
from __future__ import annotations

import os
import sys

from contextlib import suppress
from importlib import import_module
from inspect import isfunction
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from sanic import Sanic as SanicApp

DEFAULT_APP_NAME = "app"


class AppLoader:
    """A helper to load application instances.

    Generally used by the worker to load the application instance.

    See [Dynamic Applications](/en/guide/deployment/app-loader) for information on when you may need to use this.

    Args:
        module_input (str): The module to load the application from.
        as_factory (bool): Whether the application is a factory.
        as_simple (bool): Whether the application is a simple server.
        args (Any): Arguments to pass to the application factory.
        factory (Callable[[], SanicApp]): A callable that returns a Sanic application instance.
    """  # noqa: E501

    def __init__(
        self,
        module_input: str = "",
        as_factory: bool = False,
        as_simple: bool = False,
        args: Any = None,
        factory: Callable[[], SanicApp] | None = None,
    ) -> None:
        self.module_input = module_input
        self.module_name = ""
        self.app_name = ""
        self.as_factory = as_factory
        self.as_simple = as_simple
        self.args = args
        self.factory = factory
        self.cwd = os.getcwd()

        if module_input:
            self._parse_module_input(module_input)

    def _parse_module_input(self, module_input: str) -> None:
        delimiter = ":" if ":" in module_input else "."
        if (
            delimiter not in module_input
            or "\\" in module_input
            or "/" in module_input
        ):
            return
        module_name, app_name = module_input.rsplit(delimiter, 1)
        self.module_name = module_name
        self.app_name = app_name
        if self.app_name.endswith("()"):
            self.as_factory = True
            self.app_name = self.app_name[:-2]

    def _load_from_module(self, Sanic):
        implied_app_name = False
        if not self.module_name and not self.app_name:
            self.module_name = self.module_input
            self.app_name = DEFAULT_APP_NAME
            implied_app_name = True
        module = import_module(self.module_name)
        app = getattr(module, self.app_name, None)
        if not app and implied_app_name:
            raise ValueError(
                "Looks like you only supplied a module name. Sanic "
                "tried to locate an application instance named "
                f"{self.module_name}:app, but was unable to locate "
                "an application instance. Please provide a path "
                "to a global instance of Sanic(), or a callable that "
                "will return a Sanic() application instance."
            )
        if (self.as_factory or isfunction(app)) and not callable(app):
            raise ValueError(
                f"Expected a callable, but got {type(app).__name__}."
            )
        if self.as_factory or isfunction(app):
            try:
                app = app(self.args)
            except TypeError:
                app = app()
        if (
            not isinstance(app, Sanic)
            and self.args
            and hasattr(self.args, "target")
        ):
            app = self._try_fallback_import(app)
        return app

    def _try_fallback_import(self, app):
        app_type_name = type(app).__name__
        with suppress(ModuleNotFoundError):
            maybe_module = import_module(self.module_input)
            app = getattr(maybe_module, "app", None)
        if not app:
            raise ValueError(
                f"Module is not a Sanic app, it is a {app_type_name}\n"
                f"  Perhaps you meant {self.args.target}:app?"
            )
        return app

    def load(self) -> SanicApp:
        module_path = os.path.abspath(self.cwd)
        if module_path not in sys.path:
            sys.path.append(module_path)

        if self.factory:
            return self.factory()
        else:
            from sanic.app import Sanic
            from sanic.simple import create_simple_server

            maybe_path = Path(self.module_input)
            if self.as_simple or (
                maybe_path.is_dir()
                and ("\\" in self.module_input or "/" in self.module_input)
            ):
                app = create_simple_server(maybe_path)
            else:
                app = self._load_from_module(Sanic)
        return app
