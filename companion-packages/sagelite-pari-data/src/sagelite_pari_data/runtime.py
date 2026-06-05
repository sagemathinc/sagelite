import os
from importlib.resources import files


def pari_data_dir() -> str:
    """
    Return the bundled PARI data directory.
    """
    return os.fspath(files(__package__).joinpath("data", "pari"))


__all__ = ["pari_data_dir"]
