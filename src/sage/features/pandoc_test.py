import importlib.util
import os
import sys
import types
from pathlib import Path

import sage.features


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "pandoc.py"
spec = importlib.util.spec_from_file_location("sage.features.pandoc", MODULE_PATH)
pandoc_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.pandoc"] = pandoc_module
spec.loader.exec_module(pandoc_module)

Pandoc = pandoc_module.Pandoc


def test_pandoc_executable_discovers_pypandoc_binary_runtime(monkeypatch, tmp_path):
    executable = tmp_path / "pandoc"
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)
    pypandoc = types.ModuleType("pypandoc")
    pypandoc.get_pandoc_path = lambda: os.fspath(executable)

    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    monkeypatch.setitem(sys.modules, "pypandoc", pypandoc)

    feature = Pandoc()

    assert feature.absolute_filename() == os.fspath(executable)
