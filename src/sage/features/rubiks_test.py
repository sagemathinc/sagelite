import os
import sys

import sage.features
from sage.features.rubiks import cubex


def test_rubiks_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_rubiks"
    bindir = package / "data" / "bin"
    executable = bindir / "cubex"
    package.mkdir()
    bindir.mkdir(parents=True)
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
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_rubiks", None)
    sys.modules.pop("sagelite_rubiks.runtime", None)

    feature = cubex()

    assert feature.absolute_filename() == os.fspath(executable)
