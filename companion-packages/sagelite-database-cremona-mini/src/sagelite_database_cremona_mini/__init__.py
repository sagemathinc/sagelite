from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def cremona_mini_path() -> str:
    """
    Return the bundled mini Cremona database path.
    """
    return os.fspath(files(__package__).joinpath("data", "cremona", "cremona_mini.db"))


__all__ = ["cremona_mini_path", "sage_data_path"]
