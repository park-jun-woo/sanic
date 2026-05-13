# Re-export inspector classes and functions for backward compatibility
from sanic.cli._add_shared import _add_shared
from sanic.cli.inspector_sub_parser import InspectorSubParser
from sanic.cli.make_inspector_parser import make_inspector_parser

__all__ = (
    "InspectorSubParser",
    "_add_shared",
    "make_inspector_parser",
)
