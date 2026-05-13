# ff:func feature=worker type=util control=sequence
# ff:what Sanitize a daemon name to contain only safe filesystem characters
def _sanitize_name(name: str) -> str:
    return (
        "".join(
            c if c.isalnum() or c in ("-", "_", ".") else "_" for c in name
        ).strip("._")
        or "sanic"
    )
