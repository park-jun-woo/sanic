# ff:type feature=page type=model
# ff:what Metaclass that cascades stylesheets by combining all ancestor CSS sty

from abc import ABCMeta

from sanic.pages._extract_style import _extract_style


class CSS(ABCMeta):
    """Cascade stylesheets, i.e. combine all ancestor styles"""

    def __new__(cls, name, bases, attrs):
        Page = super().__new__(cls, name, bases, attrs)
        # Use a locally defined STYLE or the one from styles directory
        Page.STYLE = _extract_style(attrs.get("STYLE_FILE"), name)
        Page.STYLE += attrs.get("STYLE_APPEND", "")
        # Combine with all ancestor styles
        Page.CSS = "".join(
            Class.STYLE
            for Class in reversed(Page.__mro__)
            if type(Class) is CSS
        )
        return Page
