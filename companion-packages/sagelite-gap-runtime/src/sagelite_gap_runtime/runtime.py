from importlib.resources import files
import os


def gap_root() -> str:
    """
    Return the primary bundled GAP root directory.
    """
    return os.fspath(files(__package__).joinpath("data", "gap0"))


def gap_root_paths() -> str:
    """
    Return the semicolon-separated GAP root path string expected by libgap.
    """
    data = files(__package__).joinpath("data")
    roots = []
    for root in sorted(data.iterdir(), key=lambda path: path.name):
        if root.is_dir():
            roots.append(os.fspath(root))
    return ";".join(roots)


__all__ = ["gap_root", "gap_root_paths"]
