import importlib.util
import os
import sys
from pathlib import Path

import sage.features


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "lrs.py"
spec = importlib.util.spec_from_file_location("sage.features.lrs", MODULE_PATH)
lrs_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.lrs"] = lrs_module
spec.loader.exec_module(lrs_module)

Lrs = lrs_module.Lrs
LrsNash = lrs_module.LrsNash


def test_lrs_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_lrslib"
    bindir = package / "data" / "bin"
    lrs = bindir / "lrs"
    lrsnash = bindir / "lrsnash"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path(program):\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / program\n"
    )
    lrs.write_text("#!/bin/sh\n")
    lrs.chmod(0o755)
    lrsnash.write_text("#!/bin/sh\n")
    lrsnash.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_lrslib", None)
    sys.modules.pop("sagelite_lrslib.runtime", None)

    assert Lrs().absolute_filename() == os.fspath(lrs)
    assert LrsNash().absolute_filename() == os.fspath(lrsnash)
