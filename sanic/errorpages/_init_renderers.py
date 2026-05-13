# ff:func feature=error type=resolver control=sequence
# ff:what Populates the renderer registry with content-type mappings


def _init_renderers(registry):
    from sanic.errorpages.html_renderer import HTMLRenderer
    from sanic.errorpages.json_renderer import JSONRenderer
    from sanic.errorpages.text_renderer import TextRenderer

    registry.update(
        {
            "text/plain": TextRenderer,
            "application/json": JSONRenderer,
            "multipart/form-data": HTMLRenderer,
            "text/html": HTMLRenderer,
        }
    )
