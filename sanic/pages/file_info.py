# ff:type feature=page type=model
# ff:what TypedDict defining file info fields for directory listing display

from typing import TypedDict


class FileInfo(TypedDict):
    """Type for file info."""

    icon: str
    file_name: str
    file_access: str
    file_size: str
