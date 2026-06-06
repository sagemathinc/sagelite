from __future__ import annotations

from importlib.resources import as_file, files
import os
import sys


def gap3_root() -> str:
    """
    Return the bundled GAP3 root directory.
    """
    return os.fspath(files(__package__).joinpath("data", "gap3"))


def main() -> None:
    """
    Execute the bundled GAP3 startup script.
    """
    resource = files(__package__).joinpath("data", "gap3", "bin", "gap.sh")
    with as_file(resource) as executable:
        os.execv(os.fspath(executable), ["gap3", *sys.argv[1:]])


__all__ = ["gap3_root", "main"]
