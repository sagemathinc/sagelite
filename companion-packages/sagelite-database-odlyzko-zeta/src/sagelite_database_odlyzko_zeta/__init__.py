from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def odlyzko_data_path() -> str:
    """
    Return the bundled Odlyzko zeta zero database directory.
    """
    return os.fspath(files(__package__).joinpath("data", "odlyzko"))


def zeros_sobj_path() -> str:
    """
    Return the bundled ``zeros.sobj`` path.
    """
    return os.fspath(files(__package__).joinpath("data", "odlyzko", "zeros.sobj"))


__all__ = ["odlyzko_data_path", "sage_data_path", "zeros_sobj_path"]
