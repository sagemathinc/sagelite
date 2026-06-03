from importlib.resources import files
import os


def gap_root() -> str:
    """
    Return the bundled GAP root directory.
    """
    return os.fspath(files(__package__).joinpath("data", "gap"))


def gap_root_paths() -> str:
    """
    Return the semicolon-separated GAP root path string expected by libgap.
    """
    return gap_root()


__all__ = ["gap_root", "gap_root_paths"]
