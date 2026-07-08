from __future__ import annotations

import ctypes
from importlib.util import find_spec
import os
from pathlib import Path
import sys


_HANDLES: list[ctypes.CDLL] = []


def _should_preload() -> bool:
    if os.environ.get("SAGELITE_GRAPHVIZ_PRELOAD", "").lower() in {
        "0",
        "false",
        "no",
        "off",
    }:
        return False
    return sys.platform.startswith("linux") and find_spec("pygraphviz") is not None


def _candidate_libraries(libdir: Path) -> list[Path]:
    return sorted(path for path in libdir.glob("*.so*") if path.is_file())


def preload_libraries() -> None:
    if not _should_preload():
        return

    libdir = Path(__file__).resolve().parent / "data" / "lib"
    libraries = _candidate_libraries(libdir)
    loaded: set[Path] = set()

    for _ in range(len(libraries)):
        progress = False
        for library in libraries:
            if library in loaded:
                continue
            try:
                handle = ctypes.CDLL(os.fspath(library), mode=ctypes.RTLD_GLOBAL)
            except OSError:
                continue
            _HANDLES.append(handle)
            loaded.add(library)
            progress = True
        if not progress:
            break


try:
    preload_libraries()
except Exception:
    # Startup hooks must not make unrelated Python commands fail. If loading is
    # incomplete, the eventual pygraphviz import will report the real error.
    pass
