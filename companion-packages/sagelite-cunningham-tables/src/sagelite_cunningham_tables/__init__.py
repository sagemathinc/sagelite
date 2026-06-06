from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def cunningham_tables_path() -> str:
    """
    Return the bundled Cunningham tables directory.
    """
    return os.fspath(files(__package__).joinpath("data", "cunningham_tables"))


def cunningham_prime_factors_path() -> str:
    """
    Return the bundled ``cunningham_prime_factors.sobj`` path.
    """
    return os.fspath(
        files(__package__).joinpath(
            "data", "cunningham_tables", "cunningham_prime_factors.sobj"
        )
    )


__all__ = [
    "cunningham_prime_factors_path",
    "cunningham_tables_path",
    "sage_data_path",
]
