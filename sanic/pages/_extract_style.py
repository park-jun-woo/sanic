# ff:func feature=page type=util control=sequence
# ff:what Extract CSS style from a file path, string, or default styles directo

from pathlib import Path

CURRENT_DIR = Path(__file__).parent


def _extract_style(maybe_style: str | None, name: str) -> str:
    if maybe_style is not None:
        maybe_path = Path(maybe_style)
        if maybe_path.exists():
            return maybe_path.read_text(encoding="UTF-8")
        return maybe_style
    maybe_path = CURRENT_DIR / "styles" / f"{name}.css"
    if maybe_path.exists():
        return maybe_path.read_text(encoding="UTF-8")
    return ""
