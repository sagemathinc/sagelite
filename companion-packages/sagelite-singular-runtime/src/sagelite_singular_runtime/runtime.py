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


def executable_path() -> str:
    """
    Return the bundled Singular executable path.
    """
    return os.fspath(files(__package__).joinpath("data", "bin", "Singular"))


__all__ = ["executable_path", "singular_default_dir", "singular_root_dir"]
