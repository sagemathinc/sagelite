from __future__ import annotations

import importlib.util
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_source_tides():
    fullname = "sage.calculus.tides"
    path = ROOT / "src" / "sage" / "calculus" / "tides.py"
    sys.modules.pop(fullname, None)
    spec = importlib.util.spec_from_file_location(fullname, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[fullname] = module
    spec.loader.exec_module(module)
    return module


def test_tides_compile_flags_fall_back_to_sage_local(monkeypatch):
    monkeypatch.setitem(sys.modules, "sagelite_tides", None)
    monkeypatch.delitem(sys.modules, "sagelite_tides.runtime", raising=False)
    monkeypatch.setenv("SAGE_LOCAL", "/sage/local")
    tides = _load_source_tides()

    assert tides._tides_compile_flags() == (
        "/sage/local/lib/libTIDES.a",
        "-L/sage/local/lib ",
        "-I/sage/local/include ",
    )


def test_tides_compile_flags_use_sagelite_companion(monkeypatch, tmp_path):
    include = tmp_path / "include"
    lib = tmp_path / "lib"
    include.mkdir()
    lib.mkdir()
    library = lib / "libTIDES.a"
    library.write_bytes(b"")

    package = types.ModuleType("sagelite_tides")
    package.__path__ = []
    runtime = types.ModuleType("sagelite_tides.runtime")
    runtime.include_dir = lambda: include
    runtime.library_path = lambda: library
    monkeypatch.setitem(sys.modules, "sagelite_tides", package)
    monkeypatch.setitem(sys.modules, "sagelite_tides.runtime", runtime)
    tides = _load_source_tides()

    assert tides._tides_compile_flags() == (
        str(library),
        f"-L{lib} ",
        f"-I{include} ",
    )
