# ff:type feature=error type=exception
# ff:what HTTP 401 Unauthorized exception with WWW-Authenticate header support
from typing import Any

from sanic.exceptions.http_exception import HTTPException


class Unauthorized(HTTPException):
    """
    **Status**: 401 Unauthorized

    When present, additional keyword arguments may be used to complete
    the WWW-Authentication header.

    Args:
        message (Optional[Union[str, bytes]], optional): The message to be sent to the client. If `None`
            then the HTTP status 'Bad Request' will be sent. Defaults to `None`.
        scheme (Optional[str], optional): Name of the authentication scheme to be used. Defaults to `None`.
        quiet (Optional[bool], optional): When `True`, the error traceback will be suppressed
            from the logs. Defaults to `None`.
        context (Optional[Dict[str, Any]], optional): Additional mapping of key/value data that will be
            sent to the client upon exception. Defaults to `None`.
        extra (Optional[Dict[str, Any]], optional): Additional mapping of key/value data that will NOT be
            sent to the client when in PRODUCTION mode. Defaults to `None`.
        headers (Optional[Dict[str, Any]], optional): Additional headers that should be sent with the HTTP
            response. Defaults to `None`.
        **challenges (Dict[str, Any]): Additional keyword arguments that will be used to complete the
            WWW-Authentication header. Defaults to `None`.

    Examples:
        With a Basic auth-scheme, realm MUST be present:
        ```python
        raise Unauthorized(
            "Auth required.",
            scheme="Basic",
            realm="Restricted Area"
        )
        ```

        With a Digest auth-scheme, things are a bit more complicated:
        ```python
        raise Unauthorized(
            "Auth required.",
            scheme="Digest",
            realm="Restricted Area",
            qop="auth, auth-int",
            algorithm="MD5",
            nonce="abcdef",
            opaque="zyxwvu"
        )
        ```

        With a Bearer auth-scheme, realm is optional so you can write:
        ```python
        raise Unauthorized("Auth required.", scheme="Bearer")
        ```

        or, if you want to specify the realm:
        ```python
        raise Unauthorized(
            "Auth required.",
            scheme="Bearer",
            realm="Restricted Area"
        )
        ```
    """  # noqa: E501

    status_code = 401
    quiet = True

    def __init__(
        self,
        message: str | bytes | None = None,
        scheme: str | None = None,
        *,
        quiet: bool | None = None,
        context: dict[str, Any] | None = None,
        extra: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        **challenges,
    ):
        super().__init__(
            message,
            quiet=quiet,
            context=context,
            extra=extra,
            headers=headers,
        )

        # if auth-scheme is specified, set "WWW-Authenticate" header
        if scheme is not None:
            values = [f'{k!s}="{v!s}"' for k, v in challenges.items()]
            challenge = ", ".join(values)

            self.headers = {
                **self.headers,
                "WWW-Authenticate": f"{scheme} {challenge}".rstrip(),
            }
