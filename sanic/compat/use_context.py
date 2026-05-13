# ff:func feature=compat type=util control=sequence
# ff:what Context manager to temporarily override Sanic start method
from contextlib import contextmanager
from typing import Literal

from sanic.helpers import Default

StartMethod = (
    Default | Literal["fork"] | Literal["forkserver"] | Literal["spawn"]
)


@contextmanager
def use_context(method: StartMethod):
    from sanic import Sanic

    orig = Sanic.start_method
    Sanic.start_method = method
    yield
    Sanic.start_method = orig
