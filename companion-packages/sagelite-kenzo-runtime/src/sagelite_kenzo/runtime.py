import os
from importlib.resources import files


def kenzo_fas() -> str:
    """
    Return the bundled Kenzo ECL image path.
    """
    return os.fspath(files(__package__).joinpath("data", "kenzo.fas"))


__all__ = ["kenzo_fas"]
