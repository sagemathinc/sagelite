import os
import sys

import sage.features
from sage.features.graph_generators import Buckygen


def test_buckygen_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_buckygen"
    bindir = package / "data" / "bin"
    executable = bindir / "buckygen"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'buckygen'\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_buckygen", None)
    sys.modules.pop("sagelite_buckygen.runtime", None)

    feature = Buckygen()

    assert feature.absolute_filename() == os.fspath(executable)
