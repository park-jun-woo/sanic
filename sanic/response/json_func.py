# ff:func feature=response type=handler control=sequence
# ff:what Return a JSON-encoded HTTP response with custom serializer support

from typing import Any, AnyStr, Callable

from sanic.response.json_response import JSONResponse


def json(
    body: Any,
    status: int = 200,
    headers: dict[str, str] | None = None,
    content_type: str = "application/json",
    dumps: Callable[..., AnyStr] | None = None,
    **kwargs: Any,
) -> JSONResponse:
    """Returns response object with body in json format.

    Args:
        body (Any): Response data to be serialized.
        status (int, optional): HTTP response code. Defaults to `200`.
        headers (Dict[str, str], optional): Custom HTTP headers. Defaults to `None`.
        content_type (str, optional): The content type (string) of the response. Defaults to `"application/json"`.
        dumps (Callable[..., AnyStr], optional): A custom json dumps function. Defaults to `None`.
        **kwargs (Any): Remaining arguments that are passed to the json encoder.

    Returns:
        JSONResponse: A response object with body in json format.
    """  # noqa: E501
    return JSONResponse(
        body,
        status=status,
        headers=headers,
        content_type=content_type,
        dumps=dumps,
        **kwargs,
    )
