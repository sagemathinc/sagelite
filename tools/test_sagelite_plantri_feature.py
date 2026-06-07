import importlib.util
import os
import sys
from pathlib import Path

import sage


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "build" / "sage-distro" / "src" / "sage" / "config.py"
if not hasattr(sage, "config") and CONFIG_PATH.exists():
    spec = importlib.util.spec_from_file_location("sage.config", CONFIG_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["sage.config"] = module
    spec.loader.exec_module(module)
    sage.config = module

import sage.features
from sage.features.graph_generators import Benzene, Plantri


def test_benzene_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_benzene"
    bindir = package / "data" / "bin"
    executable = bindir / "benzene"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'benzene'\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_benzene", None)
    sys.modules.pop("sagelite_benzene.runtime", None)

    feature = Benzene()

    assert feature.absolute_filename() == os.fspath(executable)


def test_plantri_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_plantri"
    bindir = package / "data" / "bin"
    executable = bindir / "plantri"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'plantri'\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_plantri", None)
    sys.modules.pop("sagelite_plantri.runtime", None)

    feature = Plantri()

    assert feature.absolute_filename() == os.fspath(executable)
