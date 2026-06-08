import importlib.util
import os
import sys
from pathlib import Path

import sage.features


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "topcom.py"
spec = importlib.util.spec_from_file_location("sage.features.topcom", MODULE_PATH)
topcom_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.topcom"] = topcom_module
spec.loader.exec_module(topcom_module)

TOPCOMExecutable = topcom_module.TOPCOMExecutable


def test_topcom_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_topcom"
    bindir = package / "data" / "bin"
    libdir = package / "data" / "lib"
    executable = bindir / "points2placingtriang"
    package.mkdir()
    bindir.mkdir(parents=True)
    libdir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path(program):\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / program\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.delenv("LD_LIBRARY_PATH", raising=False)
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_topcom", None)
    sys.modules.pop("sagelite_topcom.runtime", None)

    feature = TOPCOMExecutable("points2placingtriang")

    assert feature.absolute_filename() == os.fspath(executable)
    assert os.environ["LD_LIBRARY_PATH"] == os.fspath(libdir)
