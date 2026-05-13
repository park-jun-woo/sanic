# ff:func feature=request type=parser control=iteration dimension=1
# ff:what Parse a raw cookie string from HTTP headers into a dictionary of name

import re

from sanic.cookies._unquote import _unquote

COOKIE_NAME_RESERVED_CHARS = re.compile(
    '[\x00-\x1f\x7f-\xff()<>@,;:\\\\"/[\\]?={} \x09]'
)


def parse_cookie(raw: str) -> dict[str, list[str]]:
    """Parses a raw cookie string into a dictionary.

    The function takes a raw cookie string (usually from HTTP headers) and
    returns a dictionary where each key is a cookie name and the value is a
    list of values for that cookie. The function handles quoted values and
    skips invalid cookie names.

    Args:
        raw (str): The raw cookie string to be parsed.

    Returns:
        Dict[str, List[str]]: A dictionary containing the cookie names as keys
        and a list of values for each cookie.

    Example:
        ```python
        raw = 'name1=value1; name2="value2"; name3=value3'
        cookies = parse_cookie(raw)
        # cookies will be {'name1': ['value1'], 'name2': ['value2'], 'name3': ['value3']}
        ```
    """  # noqa: E501
    cookies: dict[str, list[str]] = {}

    for token in raw.split(";"):
        name, sep, value = token.partition("=")
        name = name.strip()
        value = value.strip()

        # Support cookies =value or plain value with no name
        # https://github.com/httpwg/http-extensions/issues/159
        if not sep and not name:
            continue
        if not sep:
            name, value = "", name

        if COOKIE_NAME_RESERVED_CHARS.search(name):  # no cov
            continue

        if len(value) > 2 and value[0] == '"' and value[-1] == '"':  # no cov
            value = _unquote(value)

        if name in cookies:
            cookies[name].append(value)
        else:
            cookies[name] = [value]

    return cookies
