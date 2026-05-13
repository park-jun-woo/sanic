# ff:type feature=blueprint type=builder
# ff:what Container for grouping multiple blueprints under shared URL prefix an
from __future__ import annotations

from collections.abc import Iterable, Iterator, MutableSequence
from functools import partial
from typing import (
    TYPE_CHECKING,
    Callable,
    overload,
)

if TYPE_CHECKING:
    from sanic.blueprints.blueprint import Blueprint


bpg_base = MutableSequence["Blueprint"]


class BlueprintGroup(bpg_base):
    """This class provides a mechanism to implement a Blueprint Group.

    The `BlueprintGroup` class allows grouping blueprints under a common
    URL prefix, version, and other shared attributes. It integrates with
    Sanic's Blueprint system, offering a custom iterator to treat an
    object of this class as a list/tuple.

    Although possible to instantiate a group directly, it is recommended
    to use the `Blueprint.group` method to create a group of blueprints.

    Args:
        url_prefix (Optional[str]): URL to be prefixed before all the
            Blueprint Prefixes. Default is `None`.
        version (Optional[Union[int, str, float]]): API Version for the
            blueprint group, inherited by each Blueprint. Default is `None`.
        strict_slashes (Optional[bool]): URL Strict slash behavior
            indicator. Default is `None`.
        version_prefix (str): Prefix for the version in the URL.
            Default is `"/v"`.
        name_prefix (Optional[str]): Prefix for the name of the blueprints
            in the group. Default is an empty string.

    Examples:
        ```python
        bp1 = Blueprint("bp1", url_prefix="/bp1")
        bp2 = Blueprint("bp2", url_prefix="/bp2")

        bp3 = Blueprint("bp3", url_prefix="/bp4")
        bp4 = Blueprint("bp3", url_prefix="/bp4")


        group1 = Blueprint.group(bp1, bp2)
        group2 = Blueprint.group(bp3, bp4, version_prefix="/api/v", version="1")


        @bp1.on_request
        async def bp1_only_middleware(request):
            print("applied on Blueprint : bp1 Only")


        @bp1.route("/")
        async def bp1_route(request):
            return text("bp1")


        @bp2.route("/<param>")
        async def bp2_route(request, param):
            return text(param)


        @bp3.route("/")
        async def bp3_route(request):
            return text("bp3")


        @bp4.route("/<param>")
        async def bp4_route(request, param):
            return text(param)


        @group1.on_request
        async def group_middleware(request):
            print("common middleware applied for both bp1 and bp2")


        # Register Blueprint group under the app
        app.blueprint(group1)
        app.blueprint(group2)
        ```
    """  # noqa: E501

    __slots__ = (
        "_blueprints",
        "_url_prefix",
        "_version",
        "_strict_slashes",
        "_version_prefix",
        "_name_prefix",
    )

    def __init__(
        self,
        url_prefix: str | None = None,
        version: int | str | float | None = None,
        strict_slashes: bool | None = None,
        version_prefix: str = "/v",
        name_prefix: str | None = "",
    ):
        self._blueprints: list[Blueprint] = []
        self._url_prefix = url_prefix
        self._version = version
        self._version_prefix = version_prefix
        self._strict_slashes = strict_slashes
        self._name_prefix = name_prefix

    @property
    def url_prefix(self) -> int | str | float | None:
        """The URL prefix for the Blueprint Group.

        Returns:
            Optional[Union[int, str, float]]: URL prefix for the Blueprint
                Group.
        """
        return self._url_prefix

    @property
    def blueprints(self) -> list[Blueprint]:
        """A list of all the available blueprints under this group.

        Returns:
            List[Blueprint]: List of all the available blueprints under
                this group.
        """
        return self._blueprints

    @property
    def version(self) -> str | int | float | None:
        """API Version for the Blueprint Group, if any.

        Returns:
            Optional[Union[str, int, float]]: API Version for the Blueprint
        """
        return self._version

    @property
    def strict_slashes(self) -> bool | None:
        """Whether to enforce strict slashes for the Blueprint Group.

        Returns:
            Optional[bool]: Whether to enforce strict slashes for the
        """
        return self._strict_slashes

    @property
    def version_prefix(self) -> str:
        """Version prefix for the Blueprint Group.

        Returns:
            str: Version prefix for the Blueprint Group.
        """
        return self._version_prefix

    @property
    def name_prefix(self) -> str | None:
        """Name prefix for the Blueprint Group.

        This is mainly needed when blueprints are copied in order to
        avoid name conflicts.

        Returns:
            Optional[str]: Name prefix for the Blueprint Group.
        """
        return self._name_prefix

    def __iter__(self) -> Iterator[Blueprint]:
        """Iterate over the list of blueprints in the group.

        Returns:
            Iterator[Blueprint]: Iterator for the list of blueprints in
        """
        return iter(self._blueprints)

    @overload
    def __getitem__(self, item: int) -> Blueprint: ...

    @overload
    def __getitem__(self, item: slice) -> MutableSequence[Blueprint]: ...

    def __getitem__(
        self, item: int | slice
    ) -> Blueprint | MutableSequence[Blueprint]:
        """Get the Blueprint object at the specified index.

        This method returns a blueprint inside the group specified by
        an index value. This will enable indexing, splice and slicing
        of the blueprint group like we can do with regular list/tuple.

        This method is provided to ensure backward compatibility with
        any of the pre-existing usage that might break.

        Returns:
            Blueprint: Blueprint object at the specified index.

        Raises:
            IndexError: If the index is out of range.
        """
        return self._blueprints[item]

    @overload
    def __setitem__(self, index: int, item: Blueprint) -> None: ...

    @overload
    def __setitem__(self, index: slice, item: Iterable[Blueprint]) -> None: ...

    def __setitem__(
        self,
        index: int | slice,
        item: Blueprint | Iterable[Blueprint],
    ) -> None:
        """Set the Blueprint object at the specified index.

        Abstract method implemented to turn the `BlueprintGroup` class
        into a list like object to support all the existing behavior.

        This method is used to perform the list's indexed setter operation.

        Args:
            index (int): Index to use for removing a new Blueprint item
            item (Blueprint): New `Blueprint` object.

        Returns:
            None

        Raises:
            IndexError: If the index is out of range.
        """
        if isinstance(index, int):
            if not isinstance(item, self._get_blueprint_class()):
                raise TypeError("Expected a Blueprint instance")
            self._blueprints[index] = item
        elif isinstance(index, slice):
            if not isinstance(item, Iterable):
                raise TypeError("Expected an iterable of Blueprint instances")
            self._blueprints[index] = list(item)
        else:
            raise TypeError("Index must be int or slice")

    @overload
    def __delitem__(self, index: int) -> None: ...

    @overload
    def __delitem__(self, index: slice) -> None: ...

    def __delitem__(self, index: int | slice) -> None:
        """Delete the Blueprint object at the specified index.

        Abstract method implemented to turn the `BlueprintGroup` class
        into a list like object to support all the existing behavior.

        This method is used to delete an item from the list of blueprint
        groups like it can be done on a regular list with index.

        Args:
            index (int): Index to use for removing a new Blueprint item

        Returns:
            None

        Raises:
            IndexError: If the index is out of range.
        """
        del self._blueprints[index]

    def __len__(self) -> int:
        """Get the Length of the blueprint group object.

        Returns:
            int: Length of the blueprint group object.
        """
        return len(self._blueprints)

    def append(self, value: Blueprint) -> None:
        """Add a new Blueprint object to the group.

        The Abstract class `MutableSequence` leverages this append method to
        perform the `BlueprintGroup.append` operation.

        Args:
            value (Blueprint): New `Blueprint` object.

        Returns:
            None
        """
        self._blueprints.append(value)

    def exception(self, *exceptions: Exception, **kwargs) -> Callable:
        """Decorate a function to handle exceptions for all blueprints in the group.

        In case of nested Blueprint Groups, the same handler is applied
        across each of the Blueprints recursively.

        Args:
            *exceptions (Exception): Exceptions to handle
            **kwargs (dict): Optional Keyword arg to use with Middleware

        Returns:
            Partial function to apply the middleware

        Examples:
            ```python
            bp1 = Blueprint("bp1", url_prefix="/bp1")
            bp2 = Blueprint("bp2", url_prefix="/bp2")
            group1 = Blueprint.group(bp1, bp2)

            @group1.exception(Exception)
            def handler(request, exception):
                return text("Exception caught")
            ```
        """  # noqa: E501

        def register_exception_handler_for_blueprints(fn):
            for blueprint in self.blueprints:
                blueprint.exception(*exceptions, **kwargs)(fn)

        return register_exception_handler_for_blueprints

    def insert(self, index: int, item: Blueprint) -> None:
        """Insert a new Blueprint object to the group at the specified index.

        The Abstract class `MutableSequence` leverages this insert method to
        perform the `BlueprintGroup.append` operation.

        Args:
            index (int): Index to use for removing a new Blueprint item
            item (Blueprint): New `Blueprint` object.

        Returns:
            None
        """
        self._blueprints.insert(index, item)

    def middleware(self, *args, **kwargs):
        """A decorator that can be used to implement a Middleware for all blueprints in the group.

        In case of nested Blueprint Groups, the same middleware is applied
        across each of the Blueprints recursively.

        Args:
            *args (Optional): Optional positional Parameters to be use middleware
            **kwargs (Optional): Optional Keyword arg to use with Middleware

        Returns:
            Partial function to apply the middleware
        """  # noqa: E501

        def register_middleware_for_blueprints(fn):
            for blueprint in self.blueprints:
                blueprint.middleware(fn, *args, **kwargs)

        if args and callable(args[0]):
            fn = args[0]
            args = list(args)[1:]
            return register_middleware_for_blueprints(fn)
        return register_middleware_for_blueprints

    def on_request(self, middleware=None):
        """Convenience method to register a request middleware for all blueprints in the group.

        Args:
            middleware (Optional): Optional positional Parameters to be use middleware

        Returns:
            Partial function to apply the middleware
        """  # noqa: E501
        if callable(middleware):
            return self.middleware(middleware, "request")
        else:
            return partial(self.middleware, attach_to="request")

    def on_response(self, middleware=None):
        """Convenience method to register a response middleware for all blueprints in the group.

        Args:
            middleware (Optional): Optional positional Parameters to be use middleware

        Returns:
            Partial function to apply the middleware
        """  # noqa: E501
        if callable(middleware):
            return self.middleware(middleware, "response")
        else:
            return partial(self.middleware, attach_to="response")

    @staticmethod
    def _get_blueprint_class():
        from sanic.blueprints.blueprint import Blueprint

        return Blueprint
