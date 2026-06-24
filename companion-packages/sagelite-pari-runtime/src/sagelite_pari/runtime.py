from __future__ import annotations

import os
from pathlib import Path
import sys


def _bin_dir() -> Path:
    return Path(__file__).resolve().parent / "data" / "bin"


def _executable(name: str) -> Path:
    return _bin_dir() / name


def gp_command() -> Path:
    return _executable("gp")


def gphelp_command() -> Path:
    return _executable("gphelp")


def tex2mail_command() -> Path:
    return _executable("tex2mail")


def _run(name: str) -> int:
    executable = _executable(name)
    if not executable.is_file():
        raise RuntimeError(f"{name} executable is missing from companion package")
    os.execv(os.fspath(executable), [name, *sys.argv[1:]])
    return 127


def gp() -> int:
    return _run("gp")


def gphelp() -> int:
    return _run("gphelp")


def tex2mail() -> int:
    return _run("tex2mail")
