from __future__ import annotations

import os
from pathlib import Path
import sys


def executable_path(program: str = "magick") -> Path:
    root = Path(__file__).resolve().parent / "data" / "bin"
    candidate = root / program
    if candidate.is_file():
        return candidate
    if program == "magick":
        return root / "convert"
    if program == "convert":
        return root / "magick"
    return candidate


def run(program: str) -> int:
    executable = executable_path(program)
    if not executable.is_file():
        raise RuntimeError(f"{program} executable is missing from companion package")
    os.execv(os.fspath(executable), [program, *sys.argv[1:]])
    return 127


def magick() -> int:
    return run("magick")


def convert() -> int:
    return run("convert")
