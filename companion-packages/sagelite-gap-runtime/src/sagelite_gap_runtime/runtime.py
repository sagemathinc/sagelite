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
    core_roots = []
    package_roots = []
    for root in sorted(data.iterdir(), key=lambda path: path.name):
        if not root.is_dir():
            continue
        if (
            root.joinpath("lib", "init.g").is_file()
            and root.joinpath("lib", "system.g").is_file()
            and root.joinpath("lib", "package.gi").is_file()
        ):
            core_roots.append(os.fspath(root))
            continue
        pkg = root.joinpath("pkg")
        if pkg.is_dir() and any(
            package.joinpath("PackageInfo.g").is_file()
            for package in pkg.iterdir()
            if package.is_dir()
        ):
            package_roots.append(os.fspath(root))
    return ";".join(core_roots + package_roots)


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
