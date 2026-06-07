from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def jmol_path() -> str:
    """
    Return the bundled Jmol runtime directory.
    """
    return os.fspath(files(__package__).joinpath("data", "jmol"))


def jmol_data_jar_path() -> str:
    """
    Return the bundled ``JmolData.jar`` path.
    """
    return os.fspath(files(__package__).joinpath("data", "jmol", "JmolData.jar"))


__all__ = ["jmol_data_jar_path", "jmol_path", "sage_data_path"]
