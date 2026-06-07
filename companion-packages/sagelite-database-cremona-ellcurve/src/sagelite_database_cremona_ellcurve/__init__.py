from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def cremona_ellcurve_path() -> str:
    """
    Return the bundled full Cremona elliptic-curve database path.
    """
    return os.fspath(files(__package__).joinpath("data", "cremona", "cremona.db"))


__all__ = ["cremona_ellcurve_path", "sage_data_path"]
