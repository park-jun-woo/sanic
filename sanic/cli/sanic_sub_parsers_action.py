# ff:type feature=cli type=handler
# ff:what Custom sub-parsers action that auto-registers unknown parser names as
from argparse import _SubParsersAction


class SanicSubParsersAction(_SubParsersAction):
    def __call__(self, parser, namespace, values, option_string=None):
        self._name_parser_map
        parser_name = values[0]
        if parser_name not in self._name_parser_map:
            self._name_parser_map[parser_name] = parser
            values = ["<custom>", *values]

        super().__call__(parser, namespace, values, option_string)
