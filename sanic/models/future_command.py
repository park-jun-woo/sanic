# ff:type feature=model type=model
# ff:what NamedTuple representing a future command registration with name and c

from typing import Callable, NamedTuple


class FutureCommand(NamedTuple):
    name: str
    func: Callable
