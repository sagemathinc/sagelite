from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def ellcurves_data_path() -> str:
    """
    Return the bundled elliptic curves database directory.
    """
    return os.fspath(files(__package__).joinpath("data", "ellcurves"))


def rank_file_path(rank: int) -> str:
    """
    Return the bundled rank file path for ``rank``.
    """
    return os.fspath(files(__package__).joinpath("data", "ellcurves", f"rank{rank}"))


__all__ = ["ellcurves_data_path", "rank_file_path", "sage_data_path"]
