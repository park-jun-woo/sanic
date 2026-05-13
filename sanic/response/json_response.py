# ff:type feature=response type=model
# ff:what JSON response with raw body access, mutation methods (append, extend,

from __future__ import annotations

from typing import Any, AnyStr, Callable

from sanic.compat import Header
from sanic.exceptions import SanicException
from sanic.helpers import Default, _default
from sanic.response.base_http_response import BaseHTTPResponse
from sanic.response.http_response import HTTPResponse


class JSONResponse(HTTPResponse):
    """Convenience class for JSON responses

    HTTP response to be sent back to the client, when the response
    is of json type. Offers several utilities to manipulate common
    json data types.

    Args:
        body (Optional[Any], optional): The body content to be returned. Defaults to `None`.
        status (int, optional): HTTP response number. Defaults to `200`.
        headers (Optional[Union[Header, Dict[str, str]]], optional): Headers to be returned. Defaults to `None`.
        content_type (str, optional): Content type to be returned (as a header). Defaults to `"application/json"`.
        dumps (Optional[Callable[..., AnyStr]], optional): The function to use for json encoding. Defaults to `None`.
        **kwargs (Any, optional): The kwargs to pass to the json encoding function. Defaults to `{}`.
    """  # noqa: E501

    __slots__ = (
        "_body",
        "_body_manually_set",
        "_initialized",
        "_raw_body",
        "_use_dumps",
        "_use_dumps_kwargs",
    )

    def __init__(
        self,
        body: Any = None,
        status: int = 200,
        headers: Header | dict[str, str] | None = None,
        content_type: str = "application/json",
        dumps: Callable[..., AnyStr] | None = None,
        **kwargs: Any,
    ):
        self._initialized = False
        self._body_manually_set = False

        self._use_dumps: Callable[..., str | bytes] = (
            dumps or BaseHTTPResponse._dumps
        )
        self._use_dumps_kwargs = kwargs

        self._raw_body = body

        super().__init__(
            self._encode_body(self._use_dumps(body, **self._use_dumps_kwargs)),
            headers=headers,
            status=status,
            content_type=content_type,
        )

        self._initialized = True

    def _check_body_not_manually_set(self):
        if self._body_manually_set:
            raise SanicException(
                "Cannot use raw_body after body has been manually set."
            )

    @property
    def raw_body(self) -> Any:
        """Returns the raw body, as long as body has not been manually set previously.

        NOTE: This object should not be mutated, as it will not be
        reflected in the response body. If you need to mutate the
        response body, consider using one of the provided methods in
        this class or alternatively call set_body() with the mutated
        object afterwards or set the raw_body property to it.

        Returns:
            Optional[Any]: The raw body
        """  # noqa: E501
        self._check_body_not_manually_set()
        return self._raw_body

    @raw_body.setter
    def raw_body(self, value: Any):
        self._body_manually_set = False
        self._body = self._encode_body(
            self._use_dumps(value, **self._use_dumps_kwargs)
        )
        self._raw_body = value

    @property  # type: ignore
    def body(self) -> bytes | None:  # type: ignore
        """Returns the response body.

        Returns:
            Optional[bytes]: The response body
        """
        return self._body

    @body.setter
    def body(self, value: bytes | None):
        self._body = value
        if not self._initialized:
            return
        self._body_manually_set = True

    def set_body(
        self,
        body: Any,
        dumps: Callable[..., AnyStr] | None = None,
        **dumps_kwargs: Any,
    ) -> None:
        """Set the response body to the given value, using the given dumps function

        Sets a new response body using the given dumps function
        and kwargs, or falling back to the defaults given when
        creating the object if none are specified.

        Args:
            body (Any): The body to set
            dumps (Optional[Callable[..., AnyStr]], optional): The function to use for json encoding. Defaults to `None`.
            **dumps_kwargs (Any, optional): The kwargs to pass to the json encoding function. Defaults to `{}`.

        Examples:
            ```python
            response = JSONResponse({"foo": "bar"})
            response.set_body({"bar": "baz"})
            assert response.body == b'{"bar": "baz"}'
            ```
        """  # noqa: E501
        self._body_manually_set = False
        self._raw_body = body

        use_dumps = dumps or self._use_dumps
        use_dumps_kwargs = dumps_kwargs if dumps else self._use_dumps_kwargs

        self._body = self._encode_body(use_dumps(body, **use_dumps_kwargs))

    def append(self, value: Any) -> None:
        """Appends a value to the response raw_body, ensuring that body is kept up to date.

        This can only be used if raw_body is a list.

        Args:
            value (Any): The value to append

        Raises:
            SanicException: If the body is not a list
        """  # noqa: E501

        self._check_body_not_manually_set()

        if not isinstance(self._raw_body, list):
            raise SanicException("Cannot append to a non-list object.")

        self._raw_body.append(value)
        self.raw_body = self._raw_body

    def extend(self, value: Any) -> None:
        """Extends the response's raw_body with the given values, ensuring that body is kept up to date.

        This can only be used if raw_body is a list.

        Args:
            value (Any): The values to extend with

        Raises:
            SanicException: If the body is not a list
        """  # noqa: E501

        self._check_body_not_manually_set()

        if not isinstance(self._raw_body, list):
            raise SanicException("Cannot extend a non-list object.")

        self._raw_body.extend(value)
        self.raw_body = self._raw_body

    def update(self, *args, **kwargs) -> None:
        """Updates the response's raw_body with the given values, ensuring that body is kept up to date.

        This can only be used if raw_body is a dict.

        Args:
            *args: The args to update with
            **kwargs: The kwargs to update with

        Raises:
            SanicException: If the body is not a dict
        """  # noqa: E501

        self._check_body_not_manually_set()

        if not isinstance(self._raw_body, dict):
            raise SanicException("Cannot update a non-dict object.")

        self._raw_body.update(*args, **kwargs)
        self.raw_body = self._raw_body

    def pop(self, key: Any, default: Any = _default) -> Any:
        """Pops a key from the response's raw_body, ensuring that body is kept up to date.

        This can only be used if raw_body is a dict or a list.

        Args:
            key (Any): The key to pop
            default (Any, optional): The default value to return if the key is not found. Defaults to `_default`.

        Raises:
            SanicException: If the body is not a dict or a list
            TypeError: If the body is a list and a default value is provided

        Returns:
            Any: The value that was popped
        """  # noqa: E501

        self._check_body_not_manually_set()

        if not isinstance(self._raw_body, (list, dict)):
            raise SanicException(
                "Cannot pop from a non-list and non-dict object."
            )

        if isinstance(default, Default):
            value = self._raw_body.pop(key)
        elif isinstance(self._raw_body, list):
            raise TypeError("pop doesn't accept a default argument for lists")
        else:
            value = self._raw_body.pop(key, default)

        self.raw_body = self._raw_body

        return value
