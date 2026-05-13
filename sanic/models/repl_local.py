# ff:type feature=cli type=model
# ff:what NamedTuple representing a REPL local variable with name and descripti

from typing import Any, NamedTuple


class REPLLocal(NamedTuple):
    var: Any
    name: str
    desc: str
