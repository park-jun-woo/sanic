# ff:type feature=cli type=model
# ff:what Daemon CLI argument group for background process, pidfile, logfile, a
from sanic.cli.group import Group
from sanic.compat import OS_IS_WINDOWS


class DaemonGroup(Group):
    name = "Daemon"

    def attach(self, short: bool = False):
        if OS_IS_WINDOWS:
            return

        self.container.add_argument(
            "-D",
            "--daemon",
            dest="daemon",
            action="store_true",
            help="Run server in background (auto-generated PID file)",
        )

        if short:
            return

        self.container.add_argument(
            "--pidfile",
            dest="pidfile",
            type=str,
            default=None,
            help="Override auto-generated PID file path (requires --daemon)",
        )
        self.container.add_argument(
            "--logfile",
            dest="logfile",
            type=str,
            default=None,
            help="Path to log file for daemon output (requires --daemon)",
        )
        self.container.add_argument(
            "--user",
            dest="daemon_user",
            type=str,
            default=None,
            help="User to run daemon as (requires root)",
        )
        self.container.add_argument(
            "--group",
            dest="daemon_group",
            type=str,
            default=None,
            help="Group to run daemon as (requires root)",
        )

    def prepare(self, args):
        if OS_IS_WINDOWS:
            return

        has_daemon_opts = getattr(args, "pidfile", None) or getattr(
            args, "logfile", None
        )
        if has_daemon_opts and not getattr(args, "daemon", False):
            raise SystemExit("Error: --pidfile and --logfile require --daemon")
