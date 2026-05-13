# ff:func feature=server type=config control=sequence
# ff:what Configure SIGINT and SIGTERM handlers for worker process signal manag
from __future__ import annotations

import asyncio
import os

from functools import partial
from signal import SIG_IGN, SIGINT, SIGTERM
from signal import signal as signal_func
from typing import TYPE_CHECKING

from sanic.compat import OS_IS_WINDOWS, ctrlc_workaround_for_windows

if TYPE_CHECKING:
    from sanic.app import Sanic


def _setup_system_signals(
    app: Sanic,
    run_multiple: bool,
    register_sys_signals: bool,
    loop: asyncio.AbstractEventLoop,
) -> None:  # no cov
    signal_func(SIGINT, SIG_IGN)
    signal_func(SIGTERM, SIG_IGN)
    os.environ["SANIC_WORKER_PROCESS"] = "true"
    # Register signals for graceful termination
    if not register_sys_signals:
        return
    if OS_IS_WINDOWS:
        ctrlc_workaround_for_windows(app)
    else:
        for _signal in [SIGINT, SIGTERM]:
            loop.add_signal_handler(
                _signal, partial(app.stop, terminate=False)
            )
