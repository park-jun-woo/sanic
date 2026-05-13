# ff:type feature=cli type=parser
# ff:what Inspector sub-parser that auto-adds shared arguments and prepends log
from argparse import ArgumentParser

from sanic.application.logo import get_logo
from sanic.cli._add_shared import _add_shared


class InspectorSubParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _add_shared(self)
        if not self.description:
            self.description = ""
        self.description = get_logo(True) + self.description
