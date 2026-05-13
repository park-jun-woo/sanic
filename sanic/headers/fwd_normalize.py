# ff:func feature=http type=parser control=iteration dimension=1
# ff:what Normalizes and converts values extracted from forwarded headers
from __future__ import annotations

from collections.abc import Iterable
from urllib.parse import unquote

from sanic.headers.fwd_normalize_address import fwd_normalize_address

Options = dict[str, int | str]
OptionsIterable = Iterable[tuple[str, str]]


def fwd_normalize(fwd: OptionsIterable) -> Options:
    """Normalize and convert values extracted from forwarded headers.

    Args:
        fwd (OptionsIterable): An iterable of key-value pairs.

    Returns:
        Options: A dict of normalized key-value pairs.
    """

    def _fwd_apply(ret: dict, key: str, val: str) -> None:
        try:
            if key in ("by", "for"):
                ret[key] = fwd_normalize_address(val)
            elif key in ("host", "proto"):
                ret[key] = val.lower()
            elif key == "port":
                ret[key] = int(val)
            elif key == "path":
                ret[key] = unquote(val)
            else:
                ret[key] = val
        except ValueError:
            pass

    ret: dict[str, int | str] = {}
    for key, val in fwd:
        if val is None:
            continue
        _fwd_apply(ret, key, val)
    return ret
