# ff:func feature=error type=resolver control=sequence
# ff:what Lazy loader for error page renderer registry

from sanic.errorpages._init_renderers import _init_renderers
from sanic.errorpages.base_renderer import BaseRenderer

RENDERERS_BY_CONTENT_TYPE: dict[str, type[BaseRenderer]] = {}


def _get_renderers():
    # Lazy import to avoid circular imports
    if not RENDERERS_BY_CONTENT_TYPE:
        _init_renderers(RENDERERS_BY_CONTENT_TYPE)
    return RENDERERS_BY_CONTENT_TYPE
