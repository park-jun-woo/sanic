# ff:func feature=response type=handler control=sequence
# ff:what Return an HTML HTTP response, supporting str, bytes, and HTMLProtocol

from sanic.models.html_protocol import HTMLProtocol
from sanic.response.http_response import HTTPResponse


def html(
    body: str | bytes | HTMLProtocol,
    status: int = 200,
    headers: dict[str, str] | None = None,
) -> HTTPResponse:
    """Returns response object with body in html format.

    Body should be a `str` or `bytes` like object, or an object with `__html__` or `_repr_html_`.

    Args:
        body (Union[str, bytes, HTMLProtocol]): Response data.
        status (int, optional): HTTP response code. Defaults to `200`.
        headers (Dict[str, str], optional): Custom HTTP headers. Defaults to `None`.

    Returns:
        HTTPResponse: A response object with body in html format.
    """  # noqa: E501
    if not isinstance(body, (str, bytes)):
        if hasattr(body, "__html__"):
            body = body.__html__()
        elif hasattr(body, "_repr_html_"):
            body = body._repr_html_()

    return HTTPResponse(
        body,
        status=status,
        headers=headers,
        content_type="text/html; charset=utf-8",
    )
