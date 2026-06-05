from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def jones_data_path() -> str:
    """
    Return the bundled Jones number field database directory.
    """
    return os.fspath(files(__package__).joinpath("data", "jones"))


def jones_sobj_path() -> str:
    """
    Return the bundled ``jones.sobj`` path.
    """
    return os.fspath(files(__package__).joinpath("data", "jones", "jones.sobj"))


__all__ = ["jones_data_path", "jones_sobj_path", "sage_data_path"]
