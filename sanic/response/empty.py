# ff:func feature=response type=handler control=sequence
# ff:what Return an empty HTTP response with configurable status and headers

from sanic.response.http_response import HTTPResponse


def empty(
    status: int = 204, headers: dict[str, str] | None = None
) -> HTTPResponse:
    """Returns an empty response to the client.

    Args:
        status (int, optional): HTTP response code. Defaults to `204`.
        headers ([type], optional): Custom HTTP headers. Defaults to `None`.

    Returns:
        HTTPResponse: An empty response to the client.
    """
    return HTTPResponse(body=b"", status=status, headers=headers)
