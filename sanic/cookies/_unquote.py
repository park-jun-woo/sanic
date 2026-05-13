# ff:func feature=request type=util control=iteration dimension=1
# ff:what Unquote a cookie value by processing octal escapes and backslash-quot

import re

OCTAL_PATTERN = re.compile(r"\\[0-3][0-7][0-7]")
QUOTE_PATTERN = re.compile(r"[\\].")


def _unquote(str):  # no cov
    if str is None or len(str) < 2:
        return str
    if str[0] != '"' or str[-1] != '"':
        return str

    str = str[1:-1]

    i = 0
    n = len(str)
    res = []
    while 0 <= i < n:
        o_match = OCTAL_PATTERN.search(str, i)
        q_match = QUOTE_PATTERN.search(str, i)
        if not o_match and not q_match:
            res.append(str[i:])
            break
        # else:
        j = k = -1
        if o_match:
            j = o_match.start(0)
        if q_match:
            k = q_match.start(0)
        if q_match and (not o_match or k < j):
            res.append(str[i:k])
            res.append(str[k + 1])
            i = k + 2
        else:
            res.append(str[i:j])
            res.append(chr(int(str[j + 1 : j + 4], 8)))  # noqa: E203
            i = j + 4
    return "".join(res)
