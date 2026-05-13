# ff:type feature=worker type=handler
# ff:what File-watching reloader that triggers worker restarts on source change
from __future__ import annotations

import os
import sys

from asyncio import new_event_loop
from itertools import chain
from multiprocessing.connection import Connection
from pathlib import Path
from signal import SIGINT, SIGTERM
from signal import signal as signal_func
from time import sleep

from sanic.server.events import trigger_events
from sanic.worker.loader import AppLoader


class Reloader:
    INTERVAL = 1.0  # seconds

    def __init__(
        self,
        publisher: Connection,
        interval: float,
        reload_dirs: set[Path],
        app_loader: AppLoader,
    ):
        self._publisher = publisher
        self.interval = interval or self.INTERVAL
        self.reload_dirs = reload_dirs
        self.run = True
        self.app_loader = app_loader

    def __call__(self) -> None:
        app = self.app_loader.load()
        signal_func(SIGINT, self.stop)
        signal_func(SIGTERM, self.stop)
        mtimes: dict[str, float] = {}

        reloader_start = app.listeners.get("reload_process_start")
        reloader_stop = app.listeners.get("reload_process_stop")
        before_trigger = app.listeners.get("before_reload_trigger")
        after_trigger = app.listeners.get("after_reload_trigger")
        loop = new_event_loop()
        if reloader_start:
            trigger_events(reloader_start, loop, app)

        while self.run:
            changed = self._detect_changes(mtimes)
            if changed and before_trigger:
                trigger_events(before_trigger, loop, app)
            if changed:
                self.reload(",".join(changed) if changed else "unknown")
            if changed and after_trigger:
                trigger_events(after_trigger, loop, app, changed=changed)
            sleep(self.interval)
        else:
            if reloader_stop:
                trigger_events(reloader_stop, loop, app)

    def _detect_changes(self, mtimes):
        changed = set()
        for filename in self.files():
            try:
                if self.check_file(filename, mtimes):
                    path = (
                        filename
                        if isinstance(filename, str)
                        else filename.resolve()
                    )
                    changed.add(str(path))
            except OSError:
                continue
        return changed

    def stop(self, *_):
        self.run = False

    def reload(self, reloaded_files):
        message = f"__ALL_PROCESSES__:{reloaded_files}"
        self._publisher.send(message)

    def files(self):
        return chain(
            self.python_files(),
            *(d.glob("**/*") for d in self.reload_dirs),
        )

    @staticmethod
    def _resolve_module_file(filename):
        """Resolve a module filename to an actual file path."""
        old = None
        while not os.path.isfile(filename):
            old = filename
            filename = os.path.dirname(filename)
            if filename == old:
                return None
        if filename[-4:] in (".pyc", ".pyo"):
            filename = filename[:-1]
        return filename

    def python_files(self):  # no cov
        """This iterates over all relevant Python files.

        It goes through all
        loaded files from modules, all files in folders of already loaded
        modules as well as all files reachable through a package.
        """
        # The list call is necessary on Python 3 in case the module
        # dictionary modifies during iteration.
        for module in list(sys.modules.values()):
            if module is None:
                continue
            filename = getattr(module, "__file__", None)
            if not filename:
                continue
            resolved = self._resolve_module_file(filename)
            if resolved is not None:
                yield resolved

    @staticmethod
    def check_file(filename, mtimes) -> bool:
        need_reload = False

        mtime = os.stat(filename).st_mtime
        old_time = mtimes.get(filename)
        if old_time is None:
            mtimes[filename] = mtime
        elif mtime > old_time:
            mtimes[filename] = mtime
            need_reload = True

        return need_reload
