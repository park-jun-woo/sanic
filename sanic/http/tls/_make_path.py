# ff:func feature=http type=util control=sequence
# ff:what Resolve a certificate file path from either an absolute path or a tmp
from pathlib import Path


def _make_path(maybe_path: Path | str, tmpdir: Path | None) -> Path:
    if isinstance(maybe_path, Path):
        return maybe_path
    path = Path(maybe_path)
    if path.exists():
        return path
    if not tmpdir:
        raise RuntimeError("Reached an unknown state. No tmpdir.")
    return tmpdir / maybe_path
