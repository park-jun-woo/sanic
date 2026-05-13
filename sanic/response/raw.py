# ff:func feature=response type=handler control=sequence
# ff:what Return an HTTP response without encoding the body

from typing import AnyStr

from sanic.constants import DEFAULT_HTTP_CONTENT_TYPE
from sanic.response.http_response import HTTPResponse


def raw(
    body: AnyStr | None,
    status: int = 200,
    headers: dict[str, str] | None = None,
    content_type: str = DEFAULT_HTTP_CONTENT_TYPE,
) -> HTTPResponse:
    """Returns response object without encoding the body.

    Args:
        body (Optional[AnyStr]): Response data.
        status (int, optional): HTTP response code. Defaults to `200`.
        headers (Dict[str, str], optional): Custom HTTP headers. Defaults to `None`.
        content_type (str, optional): The content type (string) of the response. Defaults to `"application/octet-stream"`.

    Returns:
        HTTPResponse: A response object without encoding the body.
    """  # noqa: E501
    return HTTPResponse(
        body=body,
        status=status,
        headers=headers,
        content_type=content_type,
    )
