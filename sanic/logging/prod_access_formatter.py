# ff:type feature=logging type=formatter
# ff:what Production access log formatter with pipe-separated ident and timesta

from sanic.logging.auto_access_formatter import AutoAccessFormatter
from sanic.logging.color import Colors as c


class ProdAccessFormatter(AutoAccessFormatter):
    IDENT_LIMIT = 5
    MESSAGE_START = 42
    PREFIX_FORMAT = (
        f"{c.GREY}%(ident)s{{limit}}|%(asctime)s{c.END} "
        f"%(levelname)s: {{start}}"
    )
    MESSAGE_FORMAT = (
        f"{c.PURPLE}%(host)s {c.BLUE + c.BOLD}"
        f"%(request)s{c.END} "
        f"%(right)s%(status)s %(byte)s {c.GREY}%(duration)s{c.END}"
    )
    LOG_EXTRA = False
