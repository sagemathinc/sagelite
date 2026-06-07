import os
import subprocess
import sys
from importlib.resources import files


def gap_root() -> str:
    """
    Return the primary bundled GAP root directory.
    """
    return os.fspath(files(__package__).joinpath("data", "gap0"))


def gap_root_paths() -> str:
    """
    Return the semicolon-separated GAP root path string expected by libgap.
    """
    data = files(__package__).joinpath("data")
    roots = []
    for root in sorted(data.iterdir(), key=lambda path: path.name):
        if root.is_dir() and root.joinpath("lib", "init.g").is_file():
            roots.append(os.fspath(root))
    return ";".join(roots)


def gap_command() -> str | None:
    """
    Return the bundled GAP executable command, if present.
    """
    command = files(__package__).joinpath("data", "bin", "gap")
    if not command.is_file():
        return None
    return os.fspath(command)


def gap() -> None:
    """
    Run the bundled GAP executable.
    """
    command = gap_command()
    if command is None:
        raise RuntimeError("gap executable is missing from companion package")
    raise SystemExit(subprocess.call([command, *sys.argv[1:]]))


__all__ = ["gap", "gap_command", "gap_root", "gap_root_paths"]
