# ff:type feature=response type=model
# ff:what HTTP cookie representation with manipulation interface for path, doma

from __future__ import annotations

from datetime import datetime
from typing import Literal, cast

from sanic.cookies._quote import _is_legal_key, _quote
from sanic.exceptions import ServerError

SameSite = (
    Literal["Strict"]
    | Literal["Lax"]
    | Literal["None"]
    | Literal["strict"]
    | Literal["lax"]
    | Literal["none"]
)

DEFAULT_MAX_AGE = 0
SAMESITE_VALUES = ("strict", "lax", "none")


class Cookie:
    """A representation of a HTTP cookie, providing an interface to manipulate cookie attributes intended for a response.

    This class is a simplified representation of a cookie, similar to the Morsel SimpleCookie in Python's standard library.
    It allows the manipulation of various cookie attributes including path, domain, security settings, and others.

    Several "smart defaults" are provided to make it easier to create cookies that are secure by default. These include:

    - Setting the `secure` flag to `True` by default
    - Setting the `samesite` flag to `Lax` by default

    Args:
        key (str): The key (name) of the cookie.
        value (str): The value of the cookie.
        path (str, optional): The path for the cookie. Defaults to "/".
        domain (Optional[str], optional): The domain for the cookie.
            Defaults to `None`.
        secure (bool, optional): Whether the cookie is secure.
            Defaults to `True`.
        max_age (Optional[int], optional): The maximum age of the cookie
            in seconds. Defaults to `None`.
        expires (Optional[datetime], optional): The expiration date of the
            cookie. Defaults to `None`.
        httponly (bool, optional): HttpOnly flag for the cookie.
            Defaults to `False`.
        samesite (Optional[SameSite], optional): The SameSite attribute for
            the cookie. Defaults to `"Lax"`.
        partitioned (bool, optional): Whether the cookie is partitioned.
            Defaults to `False`.
        comment (Optional[str], optional): A comment for the cookie.
            Defaults to `None`.
        host_prefix (bool, optional): Whether to use the host prefix.
            Defaults to `False`.
        secure_prefix (bool, optional): Whether to use the secure prefix.
            Defaults to `False`.
    """  # noqa: E501

    HOST_PREFIX = "__Host-"
    SECURE_PREFIX = "__Secure-"

    __slots__ = (
        "key",
        "value",
        "_path",
        "_comment",
        "_domain",
        "_secure",
        "_httponly",
        "_partitioned",
        "_expires",
        "_max_age",
        "_samesite",
    )

    _keys = {
        "path": "Path",
        "comment": "Comment",
        "domain": "Domain",
        "max-age": "Max-Age",
        "expires": "expires",
        "samesite": "SameSite",
        # "version": "Version",
        "secure": "Secure",
        "httponly": "HttpOnly",
        "partitioned": "Partitioned",
    }
    _flags = {"secure", "httponly", "partitioned"}

    def __init__(
        self,
        key: str,
        value: str,
        *,
        path: str = "/",
        domain: str | None = None,
        secure: bool = True,
        max_age: int | None = None,
        expires: datetime | None = None,
        httponly: bool = False,
        samesite: SameSite | None = "Lax",
        partitioned: bool = False,
        comment: str | None = None,
        host_prefix: bool = False,
        secure_prefix: bool = False,
    ):
        if key in self._keys:
            raise KeyError("Cookie name is a reserved word")
        if not _is_legal_key(key):
            raise KeyError("Cookie key contains illegal characters")
        if host_prefix and not secure:
            raise ServerError(
                "Cannot set host_prefix on a cookie without secure=True"
            )
        if host_prefix and path != "/":
            raise ServerError(
                "Cannot set host_prefix on a cookie unless path='/'"
            )
        if host_prefix and domain:
            raise ServerError(
                "Cannot set host_prefix on a cookie with a defined domain"
            )
        if not host_prefix and secure_prefix and not secure:
            raise ServerError(
                "Cannot set secure_prefix on a cookie without secure=True"
            )
        if partitioned and not host_prefix:
            # This is technically possible, but it is not advisable so we will
            # take a stand and say "don't shoot yourself in the foot"
            raise ServerError(
                "Cannot create a partitioned cookie without "
                "also setting host_prefix=True"
            )

        self.key = self.make_key(key, host_prefix, secure_prefix)
        self.value = value

        self._path = path
        self._comment = comment
        self._domain = domain
        self._secure = secure
        self._httponly = httponly
        self._partitioned = partitioned
        self._expires: datetime | None = None
        self._max_age: int | None = None
        self._samesite: SameSite | None = None

        if expires is not None:
            self.expires = expires
        if max_age is not None:
            self.max_age = max_age
        if samesite is not None:
            self.samesite = samesite

    def __str__(self):
        """Format as a Set-Cookie header value."""
        output = ["{}={}".format(self.key, _quote(self.value))]
        ordered_keys = list(self._keys.keys())
        for key in sorted(
            self._keys.keys(), key=lambda k: ordered_keys.index(k)
        ):
            value = getattr(self, key.replace("-", "_"))
            if value is None or value is False:
                continue
            if key == "max-age":
                try:
                    output.append("%s=%d" % (self._keys[key], value))
                except TypeError:
                    output.append("{}={}".format(self._keys[key], value))
            elif key == "expires":
                output.append(
                    "%s=%s"
                    % (
                        self._keys[key],
                        value.strftime("%a, %d-%b-%Y %T GMT"),
                    )
                )
            elif key in self._flags:
                output.append(self._keys[key])
            else:
                output.append("{}={}".format(self._keys[key], value))

        return "; ".join(output)

    @property
    def path(self) -> str:  # no cov
        """The path of the cookie. Defaults to `"/"`."""
        return self._path

    @path.setter
    def path(self, value: str) -> None:  # no cov
        self._path = value

    @property
    def expires(self) -> datetime | None:  # no cov
        """The expiration date of the cookie. Defaults to `None`."""
        return self._expires

    @expires.setter
    def expires(self, value: datetime) -> None:  # no cov
        if not isinstance(value, datetime):
            raise TypeError("Cookie 'expires' property must be a datetime")
        self._expires = value

    @property
    def comment(self) -> str | None:  # no cov
        """A comment for the cookie. Defaults to `None`."""
        return self._comment

    @comment.setter
    def comment(self, value: str) -> None:  # no cov
        self._comment = value

    @property
    def domain(self) -> str | None:  # no cov
        """The domain of the cookie. Defaults to `None`."""
        return self._domain

    @domain.setter
    def domain(self, value: str) -> None:  # no cov
        self._domain = value

    @property
    def max_age(self) -> int | None:  # no cov
        """The maximum age of the cookie in seconds. Defaults to `None`."""
        return self._max_age

    @max_age.setter
    def max_age(self, value: int) -> None:  # no cov
        if not str(value).isdigit():
            raise ValueError("Cookie max-age must be an integer")
        self._max_age = value

    @property
    def secure(self) -> bool:  # no cov
        """Whether the cookie is secure. Defaults to `True`."""
        return self._secure

    @secure.setter
    def secure(self, value: bool) -> None:  # no cov
        self._secure = value

    @property
    def httponly(self) -> bool:  # no cov
        """Whether the cookie is HTTP only. Defaults to `False`."""
        return self._httponly

    @httponly.setter
    def httponly(self, value: bool) -> None:  # no cov
        self._httponly = value

    @property
    def samesite(self) -> SameSite | None:  # no cov
        """The SameSite attribute for the cookie. Defaults to `"Lax"`."""
        return self._samesite

    @samesite.setter
    def samesite(self, value: SameSite) -> None:  # no cov
        if value.lower() not in SAMESITE_VALUES:
            raise TypeError(
                "Cookie 'samesite' property must "
                f"be one of: {','.join(SAMESITE_VALUES)}"
            )
        self._samesite = cast(SameSite, value.title())

    @property
    def partitioned(self) -> bool:  # no cov
        """Whether the cookie is partitioned. Defaults to `False`."""
        return self._partitioned

    @partitioned.setter
    def partitioned(self, value: bool) -> None:  # no cov
        self._partitioned = value

    @classmethod
    def make_key(
        cls, key: str, host_prefix: bool = False, secure_prefix: bool = False
    ) -> str:
        """Create a cookie key with the appropriate prefix.

        Cookies can have one ow two prefixes. The first is `__Host-` which
        requires that the cookie be set with `path="/", domain=None, and
        secure=True`. The second is `__Secure-` which requires that
        `secure=True`.

        They cannot be combined.

        Args:
            key (str): The key (name) of the cookie.
            host_prefix (bool, optional): Whether to add __Host- as a prefix to the key.
                This requires that path="/", domain=None, and secure=True.
                Defaults to `False`.
            secure_prefix (bool, optional): Whether to add __Secure- as a prefix to the key.
                This requires that secure=True. Defaults to `False`.

        Raises:
            ServerError: If both host_prefix and secure_prefix are set.

        Returns:
            str: The key with the appropriate prefix.
        """  # noqa: E501
        if host_prefix and secure_prefix:
            raise ServerError(
                "Both host_prefix and secure_prefix were requested. "
                "A cookie should have only one prefix."
            )
        elif host_prefix:
            key = cls.HOST_PREFIX + key
        elif secure_prefix:
            key = cls.SECURE_PREFIX + key
        return key
