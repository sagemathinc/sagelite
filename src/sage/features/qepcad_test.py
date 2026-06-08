import importlib.util
import os
import sys
from pathlib import Path

import sage.features


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "qepcad.py"
spec = importlib.util.spec_from_file_location("sage.features.qepcad", MODULE_PATH)
qepcad_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.qepcad"] = qepcad_module
spec.loader.exec_module(qepcad_module)

Qepcad = qepcad_module.Qepcad


def test_qepcad_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_qepcad"
    bindir = package / "data" / "root" / "bin"
    executable = bindir / "qepcad"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'root' / 'bin' / 'qepcad'\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_qepcad", None)
    sys.modules.pop("sagelite_qepcad.runtime", None)

    feature = Qepcad()

    assert feature.absolute_filename() == os.fspath(executable)
