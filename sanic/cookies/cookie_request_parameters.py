# ff:type feature=request type=model
# ff:what Container for accessing single and multiple cookie values with prefix

from __future__ import annotations

from typing import Any

from sanic.cookies.cookie import Cookie
from sanic.request.parameters import RequestParameters


class CookieRequestParameters(RequestParameters):
    """A container for accessing single and multiple cookie values.

    Because the HTTP standard allows for multiple cookies with the same name,
    a standard dictionary cannot be used to access cookie values. This class
    provides a way to access cookie values in a way that is similar to a
    dictionary, but also allows for accessing multiple values for a single
    cookie name when necessary.

    Args:
        cookies (Dict[str, List[str]]): A dictionary containing the cookie
            names as keys and a list of values for each cookie.

    Example:
        ```python
        raw = 'name1=value1; name2="value2"; name3=value3'
        cookies = parse_cookie(raw)
        # cookies will be {'name1': ['value1'], 'name2': ['value2'], 'name3': ['value3']}

        request_cookies = CookieRequestParameters(cookies)
        request_cookies['name1']  # 'value1'
        request_cookies.get('name1')  # 'value1'
        request_cookies.getlist('name1')  # ['value1']
        ```
    """  # noqa: E501

    def __getitem__(self, key: str) -> str | None:
        try:
            value = self._get_prefixed_cookie(key)
        except KeyError:
            value = super().__getitem__(key)
        return value

    def __getattr__(self, key: str) -> str:
        if key.startswith("_"):
            return self.__getattribute__(key)
        key = key.rstrip("_").replace("_", "-")
        return str(self.get(key, ""))

    def get(self, name: str, default: Any | None = None) -> Any | None:
        try:
            return self._get_prefixed_cookie(name)[0]
        except KeyError:
            return super().get(name, default)

    def getlist(
        self, name: str, default: list[Any] | None = None
    ) -> list[Any]:
        try:
            return self._get_prefixed_cookie(name)
        except KeyError:
            return super().getlist(name, default)

    def _get_prefixed_cookie(self, name: str) -> Any:
        getitem = super().__getitem__
        try:
            return getitem(f"{Cookie.HOST_PREFIX}{name}")
        except KeyError:
            return getitem(f"{Cookie.SECURE_PREFIX}{name}")
