# ff:type feature=cli type=parser
# ff:what ArgumentParser subclass that prepends the Sanic logo to the descripti
from argparse import ArgumentParser

from sanic.application.logo import get_logo


class ExecutorSubParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.description:
            self.description = ""
        self.description = get_logo(True) + self.description
