from __future__ import annotations

from pathlib import Path


def data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


def include_dir() -> Path:
    return data_dir() / "include"


def library_path() -> Path:
    return data_dir() / "lib" / "libTIDES.a"
