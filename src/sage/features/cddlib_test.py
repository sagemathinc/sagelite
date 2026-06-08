import importlib.util
import os
import sys
from pathlib import Path

import sage.features


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "cddlib.py"
spec = importlib.util.spec_from_file_location("sage.features.cddlib", MODULE_PATH)
cddlib_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.cddlib"] = cddlib_module
spec.loader.exec_module(cddlib_module)

CddExecutable = cddlib_module.CddExecutable


def test_cddlib_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_cddlib"
    bindir = package / "data" / "bin"
    executable = bindir / "cddexec_gmp"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path(program='cddexec_gmp'):\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / program\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_cddlib", None)
    sys.modules.pop("sagelite_cddlib.runtime", None)

    feature = CddExecutable()

    assert feature.absolute_filename() == os.fspath(executable)
