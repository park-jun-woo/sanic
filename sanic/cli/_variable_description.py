# ff:func feature=cli type=formatter control=sequence
# ff:what Format a REPL variable description with color coding for display
from sanic.log import Colors


def _variable_description(name: str, desc: str, type_desc: str) -> str:
    return (
        f"  - {Colors.BOLD + Colors.SANIC}{name}{Colors.END}: {desc} - "
        f"{Colors.BOLD + Colors.BLUE}{type_desc}{Colors.END}"
    )
