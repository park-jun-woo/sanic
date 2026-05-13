# ff:type feature=response type=model
# ff:what Container to manipulate response cookies by dynamically writing Set-C

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sanic.cookies.cookie import Cookie, SameSite
from sanic.exceptions import ServerError

if TYPE_CHECKING:
    from sanic.compat import Header


class CookieJar:
    """A container to manipulate cookies.

    CookieJar dynamically writes headers as cookies are added and removed
    It gets around the limitation of one header per name by using the
    MultiHeader class to provide a unique key that encodes to Set-Cookie.

    Args:
        headers (Header): The headers object to write cookies to.
    """

    HEADER_KEY = "Set-Cookie"

    def __init__(self, headers: Header):
        self.headers = headers

    def __len__(self):  # no cov
        return len(self.cookies)

    @property
    def cookies(self) -> list[Cookie]:
        """A list of cookies in the CookieJar.

        Returns:
            List[Cookie]: A list of cookies in the CookieJar.
        """
        return self.headers.getall(self.HEADER_KEY, [])

    def get_cookie(
        self,
        key: str,
        path: str = "/",
        domain: str | None = None,
        host_prefix: bool = False,
        secure_prefix: bool = False,
    ) -> Cookie | None:
        """Fetch a cookie from the CookieJar.

        Args:
            key (str): The key of the cookie to fetch.
            path (str, optional): The path of the cookie. Defaults to `"/"`.
            domain (Optional[str], optional): The domain of the cookie.
                Defaults to `None`.
            host_prefix (bool, optional): Whether to add __Host- as a prefix to the key.
                This requires that path="/", domain=None, and secure=True.
                Defaults to `False`.
            secure_prefix (bool, optional): Whether to add __Secure- as a prefix to the key.
                This requires that secure=True. Defaults to `False`.

        Returns:
            Optional[Cookie]: The cookie if it exists, otherwise `None`.
        """  # noqa: E501
        for cookie in self.cookies:
            if (
                cookie.key == Cookie.make_key(key, host_prefix, secure_prefix)
                and cookie.path == path
                and cookie.domain == domain
            ):
                return cookie
        return None

    def has_cookie(
        self,
        key: str,
        path: str = "/",
        domain: str | None = None,
        host_prefix: bool = False,
        secure_prefix: bool = False,
    ) -> bool:
        """Check if a cookie exists in the CookieJar.

        Args:
            key (str): The key of the cookie to check.
            path (str, optional): The path of the cookie. Defaults to `"/"`.
            domain (Optional[str], optional): The domain of the cookie.
                Defaults to `None`.
            host_prefix (bool, optional): Whether to add __Host- as a prefix to the key.
                This requires that path="/", domain=None, and secure=True.
                Defaults to `False`.
            secure_prefix (bool, optional): Whether to add __Secure- as a prefix to the key.
                This requires that secure=True. Defaults to `False`.

        Returns:
            bool: Whether the cookie exists.
        """  # noqa: E501
        for cookie in self.cookies:
            if (
                cookie.key == Cookie.make_key(key, host_prefix, secure_prefix)
                and cookie.path == path
                and cookie.domain == domain
            ):
                return True
        return False

    def add_cookie(
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
    ) -> Cookie:
        """Add a cookie to the CookieJar.

        Args:
            key (str): Key of the cookie.
            value (str): Value of the cookie.
            path (str, optional): Path of the cookie. Defaults to "/".
            domain (Optional[str], optional): Domain of the cookie. Defaults to None.
            secure (bool, optional): Whether to set it as a secure cookie. Defaults to True.
            max_age (Optional[int], optional): Max age of the cookie in seconds; if set to 0 a
                browser should delete it. Defaults to None.
            expires (Optional[datetime], optional): When the cookie expires; if set to None browsers
                should set it as a session cookie. Defaults to None.
            httponly (bool, optional): Whether to set it as HTTP only. Defaults to False.
            samesite (Optional[SameSite], optional): How to set the samesite property, should be
                strict, lax, or none (case insensitive). Defaults to "Lax".
            partitioned (bool, optional): Whether to set it as partitioned. Defaults to False.
            comment (Optional[str], optional): A cookie comment. Defaults to None.
            host_prefix (bool, optional): Whether to add __Host- as a prefix to the key.
                This requires that path="/", domain=None, and secure=True. Defaults to False.
            secure_prefix (bool, optional): Whether to add __Secure- as a prefix to the key.
                This requires that secure=True. Defaults to False.

        Returns:
            Cookie: The instance of the created cookie.

        Raises:
            ServerError: If host_prefix is set without secure=True.
            ServerError: If host_prefix is set without path="/" and domain=None.
            ServerError: If host_prefix is set with domain.
            ServerError: If secure_prefix is set without secure=True.
            ServerError: If partitioned is set without host_prefix=True.

        Examples:
            Basic usage
            ```python
            cookie = add_cookie('name', 'value')
            ```

            Adding a cookie with a custom path and domain
            ```python
            cookie = add_cookie('name', 'value', path='/custom', domain='example.com')
            ```

            Adding a secure, HTTP-only cookie with a comment
            ```python
            cookie = add_cookie('name', 'value', secure=True, httponly=True, comment='My Cookie')
            ```

            Adding a cookie with a max age of 60 seconds
            ```python
            cookie = add_cookie('name', 'value', max_age=60)
            ```
        """  # noqa: E501
        cookie = Cookie(
            key,
            value,
            path=path,
            expires=expires,
            comment=comment,
            domain=domain,
            max_age=max_age,
            secure=secure,
            httponly=httponly,
            samesite=samesite,
            partitioned=partitioned,
            host_prefix=host_prefix,
            secure_prefix=secure_prefix,
        )
        self.headers.add(self.HEADER_KEY, cookie)

        return cookie

    def delete_cookie(
        self,
        key: str,
        *,
        path: str = "/",
        domain: str | None = None,
        secure: bool = True,
        host_prefix: bool = False,
        secure_prefix: bool = False,
    ) -> None:
        """
        Delete a cookie

        This will effectively set it as Max-Age: 0, which a browser should
        interpret it to mean: "delete the cookie".

        Since it is a browser/client implementation, your results may vary
        depending upon which client is being used.

        :param key: The key to be deleted
        :type key: str
        :param path: Path of the cookie, defaults to None
        :type path: Optional[str], optional
        :param domain: Domain of the cookie, defaults to None
        :type domain: Optional[str], optional
        :param secure: Whether to delete a secure cookie. Defaults to True.
        :param secure: bool
        :param host_prefix: Whether to add __Host- as a prefix to the key.
            This requires that path="/", domain=None, and secure=True,
            defaults to False
        :type host_prefix: bool
        :param secure_prefix: Whether to add __Secure- as a prefix to the key.
            This requires that secure=True, defaults to False
        :type secure_prefix: bool
        """
        if host_prefix and not (secure and path == "/" and domain is None):
            raise ServerError(
                "Cannot set host_prefix on a cookie without "
                "path='/', domain=None, and secure=True"
            )
        if secure_prefix and not secure:
            raise ServerError(
                "Cannot set secure_prefix on a cookie without secure=True"
            )

        cookies: list[Cookie] = self.headers.popall(self.HEADER_KEY, [])
        existing_cookie = None
        for cookie in cookies:
            if (
                cookie.key != Cookie.make_key(key, host_prefix, secure_prefix)
                or cookie.path != path
                or cookie.domain != domain
            ):
                self.headers.add(self.HEADER_KEY, cookie)
            elif existing_cookie is None:
                existing_cookie = cookie

        self._add_deletion_cookie(
            key,
            path,
            domain,
            secure,
            host_prefix,
            secure_prefix,
            existing_cookie,
        )

    def _add_deletion_cookie(
        self,
        key: str,
        path: str,
        domain: str | None,
        secure: bool,
        host_prefix: bool,
        secure_prefix: bool,
        existing_cookie: Cookie | None,
    ) -> None:
        if existing_cookie is not None:
            self._delete_existing_cookie(
                key,
                existing_cookie,
                host_prefix,
                secure_prefix,
            )
        else:
            self.add_cookie(
                key=key,
                value="",
                path=path,
                domain=domain,
                secure=secure,
                max_age=0,
                samesite=None,
                host_prefix=host_prefix,
                secure_prefix=secure_prefix,
            )

    def _delete_existing_cookie(
        self,
        key,
        existing_cookie,
        host_prefix,
        secure_prefix,
    ):
        self.add_cookie(
            key=key,
            value="",
            path=existing_cookie.path,
            domain=existing_cookie.domain,
            secure=existing_cookie.secure,
            max_age=0,
            httponly=existing_cookie.httponly,
            partitioned=existing_cookie.partitioned,
            samesite=existing_cookie.samesite,
            host_prefix=host_prefix,
            secure_prefix=secure_prefix,
        )
