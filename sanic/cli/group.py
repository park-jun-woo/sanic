# ff:type feature=cli type=model
# ff:what Base argument group class for CLI argument registration and parsing
from __future__ import annotations

from argparse import ArgumentParser, _ArgumentGroup


class Group:
    name: str | None
    container: ArgumentParser | _ArgumentGroup
    _registry: list[type[Group]] = []

    def __init_subclass__(cls) -> None:
        Group._registry.append(cls)

    def __init__(self, parser: ArgumentParser, title: str | None):
        self.parser = parser

        if title:
            self.container = self.parser.add_argument_group(title=f"  {title}")
        else:
            self.container = self.parser

    @classmethod
    def create(cls, parser: ArgumentParser):
        instance = cls(parser, cls.name)
        return instance

    def add_bool_arguments(
        self,
        *args,
        nullable=False,
        help: str,
        negative_help: str | None = None,
        **kwargs,
    ):
        group = self.container.add_mutually_exclusive_group()

        pos_help = help[0].upper() + help[1:]
        neg_help = (
            negative_help if negative_help else f"Disable {help.lower()}"
        )

        group.add_argument(
            *args,
            action="store_true",
            help=pos_help,
            **kwargs,
        )

        group.add_argument(
            "--no-" + args[0][2:],
            *args[1:],
            action="store_false",
            help=neg_help[0].upper() + neg_help[1:],
            **kwargs,
        )

        if nullable:
            group.set_defaults(**{args[0][2:].replace("-", "_"): None})

    def prepare(self, args) -> None: ...

    def attach(self, short: bool = False) -> None: ...
