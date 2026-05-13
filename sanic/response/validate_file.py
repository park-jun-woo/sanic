# ff:func feature=response type=handler control=sequence
# ff:what Validate file modification time against request If-Modified-Since hea

from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

from sanic.compat import Header
from sanic.log import logger
from sanic.response.http_response import HTTPResponse


async def validate_file(
    request_headers: Header, last_modified: datetime | float | int
) -> HTTPResponse | None:
    """Validate file based on request headers.

    Args:
        request_headers (Header): The request headers.
        last_modified (Union[datetime, float, int]): The last modified date and time of the file.

    Returns:
        Optional[HTTPResponse]: A response object with status 304 if the file is not modified.
    """  # noqa: E501
    try:
        if_modified_since = request_headers.getone("If-Modified-Since")
    except KeyError:
        return None
    try:
        if_modified_since = parsedate_to_datetime(if_modified_since)
    except (TypeError, ValueError):
        logger.warning(
            "Ignorning invalid If-Modified-Since header received: '%s'",
            if_modified_since,
        )
        return None
    if not isinstance(last_modified, datetime):
        last_modified = datetime.fromtimestamp(
            float(last_modified), tz=timezone.utc
        ).replace(microsecond=0)

    if (
        last_modified.utcoffset() is None
        and if_modified_since.utcoffset() is not None
    ):
        logger.warning(
            "Cannot compare tz-aware and tz-naive datetimes. To avoid "
            "this conflict Sanic is converting last_modified to UTC."
        )
        last_modified.replace(tzinfo=timezone.utc)
    elif (
        last_modified.utcoffset() is not None
        and if_modified_since.utcoffset() is None
    ):
        logger.warning(
            "Cannot compare tz-aware and tz-naive datetimes. To avoid "
            "this conflict Sanic is converting if_modified_since to UTC."
        )
        if_modified_since.replace(tzinfo=timezone.utc)
    if last_modified.timestamp() <= if_modified_since.timestamp():
        return HTTPResponse(status=304)

    return None
