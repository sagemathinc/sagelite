from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def stein_watkins_data_path() -> str:
    """
    Return the bundled Stein-Watkins database directory.
    """
    return os.fspath(files(__package__).joinpath("data", "stein_watkins"))


def all_data_path(n: int) -> str:
    """
    Return the bundled all-conductor database file for index ``n``.
    """
    return os.fspath(
        files(__package__).joinpath("data", "stein_watkins", f"a.{n:03d}.bz2")
    )


def prime_data_path(n: int) -> str:
    """
    Return the bundled prime-conductor database file for index ``n``.
    """
    return os.fspath(
        files(__package__).joinpath("data", "stein_watkins", f"p.{n:02d}.bz2")
    )


__all__ = [
    "all_data_path",
    "prime_data_path",
    "sage_data_path",
    "stein_watkins_data_path",
]
