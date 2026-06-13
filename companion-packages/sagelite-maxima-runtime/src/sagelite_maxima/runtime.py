import os
import sys
from importlib.resources import files


def _maxima_version_dir():
    root = files(__package__).joinpath("data", "share", "maxima")
    versions = sorted(path for path in root.iterdir() if path.is_dir())
    if not versions:
        raise RuntimeError("bundled Maxima share tree is missing")
    return versions[-1]


def _ecl_version_dir():
    root = files(__package__).joinpath("data", "lib")
    versions = sorted(
        path
        for path in root.iterdir()
        if path.is_dir() and path.name.startswith("ecl-")
    )
    if not versions:
        raise RuntimeError("bundled ECL support directory is missing")
    return versions[-1]


def maxima_prefix() -> str:
    """
    Return the bundled Maxima install root used as ``MAXIMA_PREFIX``.

    Maxima's autotools layout expects this directory to contain
    ``share/maxima/<version>``, not to point at ``<version>`` itself.
    """
    return os.fspath(files(__package__).joinpath("data"))


def maxima_library_path() -> str:
    """
    Return the bundled versioned Maxima library tree.

    Sage's ECL library mode searches this directory directly for Maxima
    ``.mac`` and ``.lisp`` files, while the standalone Maxima command uses
    :func:`maxima_prefix` as its autotools install root.
    """
    return os.fspath(_maxima_version_dir())


def maxima_layout_autotools() -> str:
    """
    Return the Maxima layout mode for the bundled install tree.
    """
    return "true"


def maxima_fas() -> str:
    """
    Return the bundled ECL Maxima image used as ``MAXIMA_FAS``.
    """
    return os.fspath(_ecl_version_dir().joinpath("maxima.fas"))


def maxima_command() -> str:
    """
    Return the bundled Maxima command used as ``MAXIMA``.
    """
    return os.fspath(files(__package__).joinpath("data", "bin", "maxima"))


def maxima() -> int:
    """
    Run the bundled Maxima executable.
    """
    executable = maxima_command()
    if not os.path.isfile(executable):
        raise RuntimeError("Maxima executable is missing from companion package")
    os.execv(executable, ["maxima", *sys.argv[1:]])
    return 127


def maxima_imagesdir() -> str:
    """
    Return the bundled ECL Maxima image directory.
    """
    return os.fspath(
        files(__package__).joinpath(
            "data", "lib", "maxima", _maxima_version_dir().name
        )
    )


def runtime_library_dir() -> str:
    """
    Return the bundled shared-library runtime directory.
    """
    return os.fspath(files(__package__).joinpath("data", "lib", "runtime"))


def ecl_dir() -> str:
    """
    Return the bundled ECL support directory used as ``ECLDIR``.
    """
    return os.fspath(_ecl_version_dir()) + os.sep


__all__ = [
    "ecl_dir",
    "maxima",
    "maxima_command",
    "maxima_fas",
    "maxima_imagesdir",
    "maxima_library_path",
    "maxima_layout_autotools",
    "maxima_prefix",
    "runtime_library_dir",
]
