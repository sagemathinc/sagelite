import os
from importlib.resources import files


def singular_root_dir() -> str:
    """
    Return the bundled Singular root directory.
    """
    return os.fspath(files(__package__).joinpath("data", "singular"))


def singular_default_dir() -> str:
    """
    Return the bundled Singular default directory.
    """
    return os.fspath(
        files(__package__).joinpath("data", "singular", "share", "singular")
    )


__all__ = ["singular_default_dir", "singular_root_dir"]
