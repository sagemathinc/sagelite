import importlib.util
import os
import sys
from pathlib import Path

import sage.features


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "frobby.py"
spec = importlib.util.spec_from_file_location("sage.features.frobby", MODULE_PATH)
frobby_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.frobby"] = frobby_module
spec.loader.exec_module(frobby_module)

Frobby = frobby_module.Frobby


def test_frobby_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_frobby"
    bindir = package / "data" / "bin"
    executable = bindir / "frobby"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'frobby'\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_frobby", None)
    sys.modules.pop("sagelite_frobby.runtime", None)

    feature = Frobby()

    assert feature.absolute_filename() == os.fspath(executable)
