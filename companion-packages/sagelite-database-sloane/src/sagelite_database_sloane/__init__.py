from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def sloane_data_path() -> str:
    """
    Return the bundled Sloane/OEIS database directory.
    """
    return os.fspath(files(__package__).joinpath("data", "sloane"))


def sloane_oeis_path() -> str:
    """
    Return the bundled ``sloane-oeis.bz2`` path.
    """
    return os.fspath(files(__package__).joinpath("data", "sloane", "sloane-oeis.bz2"))


def sloane_names_path() -> str:
    """
    Return the bundled ``sloane-names.bz2`` path.
    """
    return os.fspath(
        files(__package__).joinpath("data", "sloane", "sloane-names.bz2")
    )


__all__ = [
    "sage_data_path",
    "sloane_data_path",
    "sloane_names_path",
    "sloane_oeis_path",
]
