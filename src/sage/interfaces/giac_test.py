from __future__ import annotations

import importlib.util
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "interfaces" / "giac.py"
spec = importlib.util.spec_from_file_location("sage.interfaces.giac", MODULE_PATH)
giac_module = importlib.util.module_from_spec(spec)
sys.modules["sage.interfaces.giac"] = giac_module
spec.loader.exec_module(giac_module)


def test_giac_command_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_giac"
    bindir = package / "data" / "bin"
    executable = bindir / "giac"
    bindir.mkdir(parents=True)
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n"
        "def giac_command():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'giac'\n"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    sys.modules.pop("sagelite_giac", None)
    sys.modules.pop("sagelite_giac.runtime", None)

    assert giac_module._giac_command() == os.fspath(executable)
