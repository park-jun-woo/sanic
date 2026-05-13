# ff:func feature=response type=handler control=sequence
# ff:what Return a plain text HTTP response with type validation

from sanic.response.http_response import HTTPResponse


def text(
    body: str,
    status: int = 200,
    headers: dict[str, str] | None = None,
    content_type: str = "text/plain; charset=utf-8",
) -> HTTPResponse:
    """Returns response object with body in text format.

    Args:
        body (str): Response data.
        status (int, optional): HTTP response code. Defaults to `200`.
        headers (Dict[str, str], optional): Custom HTTP headers. Defaults to `None`.
        content_type (str, optional): The content type (string) of the response. Defaults to `"text/plain; charset=utf-8"`.

    Returns:
        HTTPResponse: A response object with body in text format.

    Raises:
        TypeError: If the body is not a string.
    """  # noqa: E501
    if not isinstance(body, str):
        raise TypeError(
            f"Bad body type. Expected str, got {type(body).__name__})"
        )

    return HTTPResponse(
        body, status=status, headers=headers, content_type=content_type
    )
