import importlib.util
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "dvipng.py"
spec = importlib.util.spec_from_file_location("sage.features.dvipng", MODULE_PATH)
dvipng_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.dvipng"] = dvipng_module
spec.loader.exec_module(dvipng_module)

dvipng = dvipng_module.dvipng


def test_dvipng_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_dvipng"
    bindir = package / "data" / "bin"
    executable = bindir / "dvipng"
    bindir.mkdir(parents=True)
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n"
        "def executable_path():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'dvipng'\n"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    sys.modules.pop("sagelite_dvipng", None)
    sys.modules.pop("sagelite_dvipng.runtime", None)

    feature = dvipng()

    assert feature.absolute_filename() == os.fspath(executable)
