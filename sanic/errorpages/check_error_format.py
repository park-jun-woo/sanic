# ff:func feature=error type=util control=sequence
# ff:what Validates that the error format is a known format type
from sanic.exceptions import SanicException

MIME_BY_CONFIG = {
    "text": "text/plain",
    "json": "application/json",
    "html": "text/html",
}


def check_error_format(format):
    """Check that the format is known."""
    if format not in MIME_BY_CONFIG and format != "auto":
        raise SanicException(f"Unknown format: {format}")
