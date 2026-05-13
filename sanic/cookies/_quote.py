# ff:func feature=response type=util control=sequence
# ff:what Quote a string for use in a cookie header, escaping special character

import re
import string

LEGAL_CHARS = string.ascii_letters + string.digits + "!#$%&'*+-.^_`|~:"
UNESCAPED_CHARS = LEGAL_CHARS + " ()/<=>?@[]{}"
TRANSLATOR = {ch: f"\\{ch:03o}" for ch in bytes(range(32)) + b'";\\\x7f'}

_is_legal_key = re.compile("[%s]+" % re.escape(LEGAL_CHARS)).fullmatch


def _quote(str):  # no cov
    r"""Quote a string for use in a cookie header.
    If the string does not need to be double-quoted, then just return the
    string.  Otherwise, surround the string in doublequotes and quote
    (with a \) special characters.
    """
    if str is None or _is_legal_key(str):
        return str
    else:
        return f'"{str.translate(TRANSLATOR)}"'
