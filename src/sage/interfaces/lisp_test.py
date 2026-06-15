import os
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "interfaces" / "lisp.py"


def _lisp_helpers():
    source = MODULE_PATH.read_text()
    start = source.index("def _lisp_command")
    end = source.index("\nclass Lisp")
    namespace = {"os": os}
    exec(source[start:end], namespace)
    return namespace


def test_lisp_command_uses_sagelite_ecl_runtime(monkeypatch, tmp_path):
    command = tmp_path / "ecl"
    command.write_text("#!/bin/sh\n")
    command.chmod(0o755)
    runtime = types.SimpleNamespace(ecl_command=lambda: command)
    package = types.ModuleType("sagelite_ecl")

    monkeypatch.setitem(sys.modules, "sagelite_ecl", package)
    monkeypatch.setitem(sys.modules, "sagelite_ecl.runtime", runtime)

    assert _lisp_helpers()["_lisp_command"]() == os.fspath(command)


def test_lisp_command_falls_back_to_system_ecl(monkeypatch, tmp_path):
    command = tmp_path / "missing-ecl"
    runtime = types.SimpleNamespace(ecl_command=lambda: command)
    package = types.ModuleType("sagelite_ecl")

    monkeypatch.setitem(sys.modules, "sagelite_ecl", package)
    monkeypatch.setitem(sys.modules, "sagelite_ecl.runtime", runtime)

    assert _lisp_helpers()["_lisp_command"]() == "ecl"
