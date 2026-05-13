# ff:func feature=http type=parser control=sequence
# ff:what Parses content-type and content-disposition header values into type a
from __future__ import annotations

import re

from collections.abc import Iterable
from typing import Any

HeaderIterable = Iterable[tuple[str, Any]]  # Values convertible to str
Options = dict[str, int | str]  # key=value fields in various headers

_token, _quoted = r"([\w!#$%&'*+\-.^_`|~]+)", r'"([^"]*)"'
_param = re.compile(rf";\s*{_token}=(?:{_token}|{_quoted})", re.ASCII)


def parse_content_header(value: str) -> tuple[str, Options]:
    """Parse content-type and content-disposition header values.

    E.g. `form-data; name=upload; filename="file.txt"` to
    ('form-data', {'name': 'upload', 'filename': 'file.txt'})

    Mostly identical to cgi.parse_header and werkzeug.parse_options_header
    but runs faster and handles special characters better.

    Unescapes %22 to `"` and %0D%0A to `\n` in field values.

    Args:
        value (str): The header value to parse.

    Returns:
        Tuple[str, Options]: The header value and a dict of options.
    """
    pos = value.find(";")
    if pos == -1:
        options: dict[str, int | str] = {}
    else:
        options = {
            m.group(1)
            .lower(): (m.group(2) or m.group(3))
            .replace("%22", '"')
            .replace("%0D%0A", "\n")
            for m in _param.finditer(value[pos:])
        }
        value = value[:pos]
    return value.strip().lower(), options
