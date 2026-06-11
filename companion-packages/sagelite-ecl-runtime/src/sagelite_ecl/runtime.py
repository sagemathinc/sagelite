from __future__ import annotations

import os
import sys
from pathlib import Path


def data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


def executable_path() -> Path:
    return data_dir() / "bin" / "ecl"


def ecl_command() -> Path:
    return executable_path()


def ecl_config_command() -> Path:
    return data_dir() / "bin" / "ecl-config"


def ecl_dir() -> Path:
    root = data_dir() / "lib"
    versions = sorted(
        path for path in root.iterdir() if path.is_dir() and path.name.startswith("ecl-")
    )
    if not versions:
        raise RuntimeError("bundled ECL support directory is missing")
    return versions[-1]


def include_dir() -> Path:
    return data_dir() / "include"


def library_dir() -> Path:
    return data_dir() / "lib"


def ecl() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("ECL executable is missing from companion package")
    os.execv(os.fspath(executable), ["ecl", *sys.argv[1:]])
    return 127


def ecl_config() -> int:
    executable = ecl_config_command()
    if not executable.is_file():
        raise RuntimeError("ecl-config executable is missing from companion package")
    os.execv(os.fspath(executable), ["ecl-config", *sys.argv[1:]])
    return 127
