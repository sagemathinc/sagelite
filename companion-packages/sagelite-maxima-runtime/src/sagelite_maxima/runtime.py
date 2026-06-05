from importlib.resources import files
import os


def _maxima_version_dir():
    root = files(__package__).joinpath("data", "share", "maxima")
    versions = sorted(path for path in root.iterdir() if path.is_dir())
    if not versions:
        raise RuntimeError("bundled Maxima share tree is missing")
    return versions[-1]


def maxima_prefix() -> str:
    """
    Return the bundled Maxima share directory used as ``MAXIMA_PREFIX``.
    """
    return os.fspath(_maxima_version_dir())


def maxima_fas() -> str:
    """
    Return the bundled ECL Maxima image used as ``MAXIMA_FAS``.
    """
    return os.fspath(files(__package__).joinpath("data", "lib", "ecl", "maxima.fas"))


__all__ = ["maxima_fas", "maxima_prefix"]
