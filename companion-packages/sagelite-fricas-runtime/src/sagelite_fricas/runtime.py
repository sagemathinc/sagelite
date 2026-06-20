from __future__ import annotations

import os
from pathlib import Path
import sys


def _data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


def fricas_prefix() -> Path:
    return _data_dir()


def executable_path() -> Path:
    return _data_dir() / "bin" / "fricas"


def library_dir() -> Path:
    return _data_dir() / "lib" / "fricas"


def share_dir() -> Path:
    return _data_dir() / "share" / "fricas"


def initfile_path() -> Path | None:
    for root in (library_dir(), share_dir()):
        if not root.is_dir():
            continue
        for candidate in sorted(root.rglob("fricas.input")):
            if candidate.is_file():
                return candidate
    return None


def fricas() -> int:
    executable = executable_path()
    if not executable.is_file():
        raise RuntimeError("fricas executable is missing from companion package")
    os.execv(os.fspath(executable), ["fricas", *sys.argv[1:]])
    return 127


__all__ = [
    "executable_path",
    "fricas",
    "fricas_prefix",
    "initfile_path",
    "library_dir",
    "share_dir",
]
