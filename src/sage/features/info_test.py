import importlib.util
import os
import sys
from pathlib import Path

import sage.features


ROOT = Path(__file__).resolve().parents[3]
SOURCE_MODULE = ROOT / "src" / "sage" / "features" / "info.py"


def _load_source_info_module():
    if not SOURCE_MODULE.exists():
        from sage.features import info

        return info

    fullname = "sage.features.info"
    sys.modules.pop(fullname, None)
    spec = importlib.util.spec_from_file_location(fullname, SOURCE_MODULE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[fullname] = module
    spec.loader.exec_module(module)
    return module


info = _load_source_info_module()


def test_info_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_info"
    bindir = package / "data" / "bin"
    executable = bindir / "info"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'info'\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_info", None)
    sys.modules.pop("sagelite_info.runtime", None)

    feature = info.Info()

    assert feature.absolute_filename() == os.fspath(executable)
