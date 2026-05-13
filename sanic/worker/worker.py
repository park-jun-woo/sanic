# ff:type feature=worker type=manager
# ff:what Worker container that creates and manages a set of WorkerProcess inst
from __future__ import annotations

from collections.abc import MutableMapping
from multiprocessing.context import BaseContext
from typing import Any

from sanic.worker.worker_process import WorkerProcess


class Worker:
    WORKER_PREFIX = "Sanic"

    def __init__(
        self,
        ident: str,
        name: str,
        serve,
        server_settings,
        context: BaseContext,
        worker_state: MutableMapping[str, Any],
        num: int = 1,
        restartable: bool = False,
        tracked: bool = True,
        auto_start: bool = True,
    ):
        self.ident = ident
        self.name = name
        self.num = num
        self.context = context
        self.serve = serve
        self.server_settings = server_settings
        self.worker_state = worker_state
        self.processes: set[WorkerProcess] = set()
        self.restartable = restartable
        self.tracked = tracked
        self.auto_start = auto_start
        for _ in range(num):
            self.create_process()

    def create_process(self) -> WorkerProcess:
        process = WorkerProcess(
            # Need to ignore this typing error - The problem is the
            # BaseContext itself has no Process. But, all of its
            # implementations do. We can safely ignore as it is a typing
            # issue in the standard lib.
            factory=self.context.Process,  # type: ignore
            name="-".join(
                [self.WORKER_PREFIX, self.name, str(len(self.processes))]
            ),
            ident=self.ident,
            target=self.serve,
            kwargs={**self.server_settings},
            worker_state=self.worker_state,
            restartable=self.restartable,
        )
        self.processes.add(process)
        return process

    def has_alive_processes(self) -> bool:
        return any(process.is_alive() for process in self.processes)
