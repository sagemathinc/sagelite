import os
from importlib.resources import files


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


def maxima_command() -> str:
    """
    Return the bundled Maxima command used as ``MAXIMA``.
    """
    return os.fspath(files(__package__).joinpath("data", "bin", "maxima"))


def ecl_dir() -> str:
    """
    Return the bundled ECL support directory used as ``ECLDIR``.
    """
    root = files(__package__).joinpath("data", "lib")
    versions = sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and path.name.startswith("ecl-")
    )
    if not versions:
        raise RuntimeError("bundled ECL support directory is missing")
    return os.fspath(versions[-1]) + os.sep


__all__ = ["ecl_dir", "maxima_command", "maxima_fas", "maxima_prefix"]
