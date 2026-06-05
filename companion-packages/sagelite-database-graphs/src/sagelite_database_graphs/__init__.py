from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def graphs_data_path() -> str:
    """
    Return the bundled graph database directory.
    """
    return os.fspath(files(__package__).joinpath("data", "graphs"))


def graphs_db_path() -> str:
    """
    Return the bundled ``graphs.db`` path.
    """
    return os.fspath(files(__package__).joinpath("data", "graphs", "graphs.db"))


__all__ = ["graphs_data_path", "graphs_db_path", "sage_data_path"]
