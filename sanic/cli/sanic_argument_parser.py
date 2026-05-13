# ff:type feature=cli type=parser
# ff:what Custom argument parser that handles sub-parser value checking
from argparse import Action, ArgumentParser
from typing import Any

from sanic.cli.sanic_sub_parsers_action import SanicSubParsersAction


class SanicArgumentParser(ArgumentParser):
    def _check_value(self, action: Action, value: Any) -> None:
        if isinstance(action, SanicSubParsersAction):
            return
        super()._check_value(action, value)
