from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def reflexive_polytopes_path() -> str:
    """
    Return the bundled reflexive polytopes database directory.
    """
    return os.fspath(files(__package__).joinpath("data", "reflexive_polytopes"))


__all__ = ["reflexive_polytopes_path", "sage_data_path"]
