# ff:func feature=server type=util control=sequence
# ff:what Check if a path after resolution is within the root directory for sym

from pathlib import Path


def _is_path_within_root(path: Path, root: Path) -> bool:
    """Check if a path (after resolution) is within the root directory.

    Returns False for:
    - Broken symlinks (cannot be resolved)
    - Paths that resolve outside the root directory
    - Any errors during resolution
    """
    try:
        resolved = path.resolve()
        resolved.relative_to(root.resolve())
    except (ValueError, OSError, RuntimeError):
        return False
    else:
        return True
