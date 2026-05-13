# ff:type feature=model type=model
# ff:what NamedTuple representing a future static file/directory registration

from pathlib import Path
from typing import NamedTuple

from sanic.handlers.directory_handler import DirectoryHandler


class FutureStatic(NamedTuple):
    uri: str
    file_or_directory: Path
    pattern: str
    use_modified_since: bool
    use_content_range: bool
    stream_large_files: bool | int
    name: str
    host: str | None
    strict_slashes: bool | None
    content_type: str | None
    resource_type: str | None
    directory_handler: DirectoryHandler
    follow_external_symlink_files: bool
    follow_external_symlink_dirs: bool
