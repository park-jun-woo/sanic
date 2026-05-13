# Re-export daemon functions for backward compatibility
from sanic.cli._add_target_args import _add_target_args
from sanic.cli._terminate_process import _terminate_process
from sanic.cli.kill_daemon import kill_daemon
from sanic.cli.make_kill_parser import make_kill_parser
from sanic.cli.make_restart_parser import make_restart_parser
from sanic.cli.make_status_parser import make_status_parser
from sanic.cli.resolve_target import resolve_target
from sanic.cli.restart_daemon import restart_daemon
from sanic.cli.status_daemon import status_daemon
from sanic.cli.stop_daemon import stop_daemon

__all__ = (
    "_add_target_args",
    "_terminate_process",
    "kill_daemon",
    "make_kill_parser",
    "make_restart_parser",
    "make_status_parser",
    "resolve_target",
    "restart_daemon",
    "status_daemon",
    "stop_daemon",
)
