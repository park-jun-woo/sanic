# ff:func feature=response type=handler control=sequence
# ff:what Return a redirect HTTP response by setting the Location header

from urllib.parse import quote_plus

from sanic.response.http_response import HTTPResponse


def redirect(
    to: str,
    headers: dict[str, str] | None = None,
    status: int = 302,
    content_type: str = "text/html; charset=utf-8",
) -> HTTPResponse:
    """Cause a HTTP redirect (302 by default) by setting a Location header.

    Args:
        to (str): path or fully qualified URL to redirect to
        headers (Optional[Dict[str, str]], optional): optional dict of headers to include in the new request. Defaults to None.
        status (int, optional): status code (int) of the new request, defaults to 302. Defaults to 302.
        content_type (str, optional): the content type (string) of the response. Defaults to "text/html; charset=utf-8".

    Returns:
        HTTPResponse: A response object with the redirect.
    """  # noqa: E501
    headers = headers or {}

    # URL Quote the URL before redirecting
    safe_to = quote_plus(to, safe=":/%#?&=@[]!$&'()*+,;")

    # According to RFC 7231, a relative URI is now permitted.
    headers["Location"] = safe_to

    return HTTPResponse(
        status=status, headers=headers, content_type=content_type
    )
