from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "lcalc.py"
spec = importlib.util.spec_from_file_location("sage.features.lcalc", MODULE_PATH)
lcalc_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.lcalc"] = lcalc_module
spec.loader.exec_module(lcalc_module)

Lcalc = lcalc_module.Lcalc


def test_lcalc_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_lcalc"
    bindir = package / "data" / "bin"
    executable = bindir / "lcalc"
    bindir.mkdir(parents=True)
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n"
        "def lcalc_command():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'lcalc'\n"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    sys.modules.pop("sagelite_lcalc", None)
    sys.modules.pop("sagelite_lcalc.runtime", None)

    feature = Lcalc()

    assert feature.absolute_filename() == os.fspath(executable)
