# ff:func feature=error type=util control=sequence
# ff:what Minimal HTML escaping for error page text content
def escape(text):
    """Minimal HTML escaping, not for attribute values (unlike html.escape)."""
    return f"{text}".replace("&", "&amp;").replace("<", "&lt;")
