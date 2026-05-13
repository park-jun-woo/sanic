# ff:type feature=mixin type=mixin
# ff:what Mixin providing the static file/directory route registration method

from __future__ import annotations

from collections.abc import Sequence
from os import PathLike
from pathlib import Path, PurePath

from sanic.base.meta import SanicMeta
from sanic.handlers.directory_handler import DirectoryHandler
from sanic.mixins.base_mixin import BaseMixin
from sanic.models.futures import FutureStatic


class StaticMixin(BaseMixin, metaclass=SanicMeta):
    def __init__(self, *args, **kwargs) -> None:
        self._future_statics: set[FutureStatic] = set()

    def _apply_static(self, static: FutureStatic):
        raise NotImplementedError  # noqa

    def static(
        self,
        uri: str,
        file_or_directory: PathLike | str,
        pattern: str = r"/?.+",
        use_modified_since: bool = True,
        use_content_range: bool = False,
        stream_large_files: bool | int = False,
        name: str = "static",
        host: str | None = None,
        strict_slashes: bool | None = None,
        content_type: str | None = None,
        apply: bool = True,
        resource_type: str | None = None,
        index: str | Sequence[str] | None = None,
        directory_view: bool = False,
        directory_handler: DirectoryHandler | None = None,
        follow_external_symlink_files: bool = False,
        follow_external_symlink_dirs: bool = False,
    ):
        """Register a root to serve files from. The input can either be a file or a directory.

        This method provides an easy and simple way to set up the route necessary to serve static files.

        Args:
            uri (str): URL path to be used for serving static content.
            file_or_directory (Union[PathLike, str]): Path to the static file
                or directory with static files.
            pattern (str, optional): Regex pattern identifying the valid
                static files. Defaults to `r"/?.+"`.
            use_modified_since (bool, optional): If true, send file modified
                time, and return not modified if the browser's matches the
                server's. Defaults to `True`.
            use_content_range (bool, optional): If true, process header for
                range requests and sends  the file part that is requested.
                Defaults to `False`.
            stream_large_files (Union[bool, int], optional): If `True`, use
                the `StreamingHTTPResponse.file_stream` handler rather than
                the `HTTPResponse.file handler` to send the file. If this
                is an integer, it represents the threshold size to switch
                to `StreamingHTTPResponse.file_stream`. Defaults to `False`,
                which means that the response will not be streamed.
            name (str, optional): User-defined name used for url_for.
                Defaults to `"static"`.
            host (Optional[str], optional): Host IP or FQDN for the
                service to use.
            strict_slashes (Optional[bool], optional): Instruct Sanic to
                check if the request URLs need to terminate with a slash.
            content_type (Optional[str], optional): User-defined content type
                for header.
            apply (bool, optional): If true, will register the route
                immediately. Defaults to `True`.
            resource_type (Optional[str], optional): Explicitly declare a
                resource to be a `"file"` or a `"dir"`.
            index (Optional[Union[str, Sequence[str]]], optional): When
                exposing against a directory, index is  the name that will
                be served as the default file. When multiple file names are
                passed, then they will be tried in order.
            directory_view (bool, optional): Whether to fallback to showing
                the directory viewer when exposing a directory. Defaults
                to `False`.
            directory_handler (Optional[DirectoryHandler], optional): An
                instance of DirectoryHandler that can be used for explicitly
                controlling and subclassing the behavior of the default
                directory handler.
            follow_external_symlink_files (bool, optional): Whether to serve
                files that are symlinks pointing outside the static root.
                Defaults to `False` for security.
            follow_external_symlink_dirs (bool, optional): Whether to serve
                files from directories that are symlinks pointing outside
                the static root. Defaults to `False` for security.

        Returns:
            List[sanic.router.Route]: Routes registered on the router.

        Examples:
            Serving a single file:
            ```python
            app.static('/foo', 'path/to/static/file.txt')
            ```

            Serving all files from a directory:
            ```python
            app.static('/static', 'path/to/static/directory')
            ```

            Serving large files with a specific threshold:
            ```python
            app.static('/static', 'path/to/large/files', stream_large_files=1000000)
            ```
        """  # noqa: E501

        name = self.generate_name(name)

        if strict_slashes is None and self.strict_slashes is not None:
            strict_slashes = self.strict_slashes

        if not isinstance(file_or_directory, (str, bytes, PurePath)):
            raise ValueError(
                f"Static route must be a valid path, not {file_or_directory}"
            )

        try:
            file_or_directory = Path(file_or_directory).resolve()
        except TypeError:
            raise TypeError(
                "Static file or directory must be a path-like object or string"
            )

        if directory_handler and (directory_view or index):
            raise ValueError(
                "When explicitly setting directory_handler, you cannot "
                "set either directory_view or index. Instead, pass "
                "these arguments to your DirectoryHandler instance."
            )

        if not directory_handler:
            directory_handler = DirectoryHandler(
                uri=uri,
                directory=file_or_directory,
                directory_view=directory_view,
                index=index,
                root_path=file_or_directory,
                follow_external_symlink_files=follow_external_symlink_files,
                follow_external_symlink_dirs=follow_external_symlink_dirs,
            )

        static = FutureStatic(
            uri,
            file_or_directory,
            pattern,
            use_modified_since,
            use_content_range,
            stream_large_files,
            name,
            host,
            strict_slashes,
            content_type,
            resource_type,
            directory_handler,
            follow_external_symlink_files,
            follow_external_symlink_dirs,
        )
        self._future_statics.add(static)

        if apply:
            self._apply_static(static)
