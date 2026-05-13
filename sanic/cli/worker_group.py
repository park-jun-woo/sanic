# ff:type feature=cli type=model
# ff:what Worker CLI argument group for worker count, fast mode, and access log
from sanic.cli.group import Group


class WorkerGroup(Group):
    name = "Worker"

    def attach(self, short: bool = False):
        if short:
            return

        group = self.container.add_mutually_exclusive_group()
        group.add_argument(
            "-w",
            "--workers",
            dest="workers",
            type=int,
            default=1,
            help="Number of worker processes [default 1]",
        )
        group.add_argument(
            "--fast",
            dest="fast",
            action="store_true",
            help="Set the number of workers to max allowed",
        )
        group.add_argument(
            "--single-process",
            dest="single",
            action="store_true",
            help="Do not use multiprocessing, run server in a single process",
        )
        self.add_bool_arguments(
            "--access-logs",
            dest="access_log",
            help="display access logs",
            default=None,
        )
