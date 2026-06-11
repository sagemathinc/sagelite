import os
from importlib.resources import files


def gap_root_paths() -> str:
    """
    Return the GAP package root contributed by this companion wheel.
    """
    root = files(__package__).joinpath("data", "gaproot")
    if root.joinpath("pkg").is_dir():
        return os.fspath(root)
    return ""


__all__ = ["gap_root_paths"]
