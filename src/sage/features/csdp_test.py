import os
import sys
import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "csdp.py"
spec = importlib.util.spec_from_file_location("sage.features.csdp", MODULE_PATH)
csdp_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.csdp"] = csdp_module
spec.loader.exec_module(csdp_module)

CSDP = csdp_module.CSDP


def test_csdp_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_csdp"
    bindir = package / "data" / "bin"
    executable = bindir / "theta"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'theta'\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    sys.modules.pop("sagelite_csdp", None)
    sys.modules.pop("sagelite_csdp.runtime", None)

    feature = CSDP()

    assert feature.absolute_filename() == os.fspath(executable)
