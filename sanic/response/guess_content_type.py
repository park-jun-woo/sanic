# ff:func feature=response type=util control=sequence
# ff:what Guess the content type by file extension with charset for text types

from mimetypes import guess_type
from pathlib import PurePath

from sanic.constants import DEFAULT_HTTP_CONTENT_TYPE


def guess_content_type(
    file_path: str | PurePath,
    fallback: str = DEFAULT_HTTP_CONTENT_TYPE,
) -> str:
    """Guess the content type (rather than MIME only) by the file extension."""
    mediatype = guess_type(file_path)[0]
    if mediatype is None:
        return fallback
    if mediatype.startswith("text/"):
        return f"{mediatype}; charset=utf-8"
    return mediatype
