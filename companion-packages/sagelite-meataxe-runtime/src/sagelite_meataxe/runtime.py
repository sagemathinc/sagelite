import os
from importlib.resources import files


def meataxe_dir() -> str:
    """
    Return the bundled MeatAxe multiplication-table directory.
    """
    return os.fspath(files(__package__).joinpath("data", "meataxe"))


__all__ = ["meataxe_dir"]
