# ff:type feature=compat type=model
# ff:what Case-insensitive multi-value HTTP header container
from multidict import CIMultiDict  # type: ignore


class Header(CIMultiDict):
    """Container used for both request and response headers.
    It is a subclass of  [CIMultiDict](https://multidict.readthedocs.io/en/stable/multidict.html#cimultidictproxy)

    It allows for multiple values for a single key in keeping with the HTTP
    spec. Also, all keys are *case in-sensitive*.

    Please checkout [the MultiDict documentation](https://multidict.readthedocs.io/en/stable/multidict.html#multidict)
    for more details about how to use the object. In general, it should work
    very similar to a regular dictionary.
    """  # noqa: E501

    def __getattr__(self, key: str) -> str:
        if key.startswith("_"):
            return self.__getattribute__(key)
        key = key.rstrip("_").replace("_", "-")
        return ",".join(self.getall(key, []))

    def get_all(self, key: str):
        """Convenience method mapped to ``getall()``."""
        return self.getall(key, [])
