# ff:func feature=response type=handler control=sequence
# ff:what Return an HTTP response with file data, supporting range requests, ca

from __future__ import annotations

from datetime import datetime
from email.utils import formatdate
from os import path
from pathlib import PurePath
from time import time

from sanic.compat import Header, open_async, stat_async
from sanic.helpers import Default, _default
from sanic.models.range import Range
from sanic.response.guess_content_type import guess_content_type
from sanic.response.http_response import HTTPResponse
from sanic.response.validate_file import validate_file


async def file(
    location: str | PurePath,
    status: int = 200,
    request_headers: Header | None = None,
    validate_when_requested: bool = True,
    mime_type: str | None = None,
    headers: dict[str, str] | None = None,
    filename: str | None = None,
    last_modified: datetime | float | int | Default | None = _default,
    max_age: float | int | None = None,
    no_store: bool | None = None,
    _range: Range | None = None,
) -> HTTPResponse:
    """Return a response object with file data.

    Args:
        location (Union[str, PurePath]): Location of file on system.
        status (int, optional): HTTP response code. Won't enforce the passed in status if only a part of the content will be sent (206) or file is being validated (304). Defaults to 200.
        request_headers (Optional[Header], optional): The request headers.
        validate_when_requested (bool, optional): If `True`, will validate the file when requested. Defaults to True.
        mime_type (Optional[str], optional): Specific mime_type.
        headers (Optional[Dict[str, str]], optional): Custom Headers.
        filename (Optional[str], optional): Override filename.
        last_modified (Optional[Union[datetime, float, int, Default]], optional): The last modified date and time of the file.
        max_age (Optional[Union[float, int]], optional): Max age for cache control.
        no_store (Optional[bool], optional): Any cache should not store this response. Defaults to None.
        _range (Optional[Range], optional):

    Returns:
        HTTPResponse: The response object with the file data.
    """  # noqa: E501

    if isinstance(last_modified, datetime):
        last_modified = last_modified.replace(microsecond=0).timestamp()
    elif isinstance(last_modified, Default):
        stat = await stat_async(location)
        last_modified = stat.st_mtime

    if (
        validate_when_requested
        and request_headers is not None
        and last_modified
    ):
        response = await validate_file(request_headers, last_modified)
        if response:
            return response

    headers = headers or {}
    if last_modified:
        headers.setdefault(
            "Last-Modified", formatdate(last_modified, usegmt=True)
        )

    if filename:
        headers.setdefault(
            "Content-Disposition", f'attachment; filename="{filename}"'
        )

    if no_store:
        cache_control = "no-store"
    elif max_age:
        cache_control = f"public, max-age={max_age}"
        headers.setdefault(
            "expires",
            formatdate(
                time() + max_age,
                usegmt=True,
            ),
        )
    else:
        cache_control = "no-cache"

    headers.setdefault("cache-control", cache_control)

    filename = filename or path.split(location)[-1]

    async with await open_async(location, mode="rb") as f:
        if _range:
            await f.seek(_range.start)
            out_stream = await f.read(_range.size)
            headers["Content-Range"] = (
                f"bytes {_range.start}-{_range.end}/{_range.total}"
            )
            status = 206
        else:
            out_stream = await f.read()

    content_type = mime_type or guess_content_type(
        filename, fallback="text/plain; charset=utf-8"
    )
    return HTTPResponse(
        body=out_stream,
        status=status,
        headers=headers,
        content_type=content_type,
    )
