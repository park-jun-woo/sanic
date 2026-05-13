# ff:func feature=response type=handler control=sequence
# ff:what Return a streaming response object with chunked file data and optiona

from __future__ import annotations

from mimetypes import guess_type
from os import path
from pathlib import PurePath

from sanic.compat import open_async
from sanic.models.range import Range
from sanic.response.response_stream import ResponseStream


async def file_stream(
    location: str | PurePath,
    status: int = 200,
    chunk_size: int = 4096,
    mime_type: str | None = None,
    headers: dict[str, str] | None = None,
    filename: str | None = None,
    _range: Range | None = None,
) -> ResponseStream:
    """Return a streaming response object with file data.

    Args:
        location (Union[str, PurePath]): Location of file on system.
        status (int, optional): HTTP response code. Won't enforce the passed in status if only a part of the content will be sent (206) or file is being validated (304). Defaults to `200`.
        chunk_size (int, optional): The size of each chunk in the stream (in bytes). Defaults to `4096`.
        mime_type (Optional[str], optional): Specific mime_type.
        headers (Optional[Dict[str, str]], optional): Custom HTTP headers.
        filename (Optional[str], optional): Override filename.
        _range (Optional[Range], optional): The range of bytes to send.
    """  # noqa: E501
    headers = headers or {}
    if filename:
        headers.setdefault(
            "Content-Disposition", f'attachment; filename="{filename}"'
        )
    filename = filename or path.split(location)[-1]
    mime_type = mime_type or guess_type(filename)[0] or "text/plain"
    if _range:
        start = _range.start
        end = _range.end
        total = _range.total

        headers["Content-Range"] = f"bytes {start}-{end}/{total}"
        status = 206

    async def _stream_range(f, response, _range, chunk_size):
        await f.seek(_range.start)
        to_send = _range.size
        while to_send > 0:
            content = await f.read(min((_range.size, chunk_size)))
            if len(content) < 1:
                break
            to_send -= len(content)
            await response.write(content)

    async def _stream_full(f, response, chunk_size):
        while True:
            content = await f.read(chunk_size)
            if len(content) < 1:
                break
            await response.write(content)

    async def _streaming_fn(response):
        async with await open_async(location, mode="rb") as f:
            if _range:
                await _stream_range(f, response, _range, chunk_size)
            else:
                await _stream_full(f, response, chunk_size)

    return ResponseStream(
        streaming_fn=_streaming_fn,
        status=status,
        headers=headers,
        content_type=mime_type,
    )
