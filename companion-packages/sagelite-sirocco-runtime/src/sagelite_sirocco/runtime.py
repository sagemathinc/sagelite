from __future__ import annotations

from pathlib import Path


def data_dir() -> Path:
    return Path(__file__).resolve().parent / "data"


def include_dir() -> Path:
    return data_dir() / "include"


def library_dir() -> Path:
    return data_dir() / "lib"


def library_path() -> Path:
    for name in ("libsirocco.so", "libsirocco.dylib"):
        candidate = library_dir() / name
        if candidate.exists():
            return candidate

    candidates = sorted(library_dir().glob("libsirocco*"))
    if candidates:
        return candidates[0]

    return library_dir() / "libsirocco.so"
