import os
import sys

import sage.features
from sage.features.sat import Glucose, Kissat


def test_glucose_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_glucose"
    bindir = package / "data" / "bin"
    glucose = bindir / "glucose"
    glucose_syrup = bindir / "glucose-syrup"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path(program):\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / program\n"
    )
    glucose.write_text("#!/bin/sh\n")
    glucose.chmod(0o755)
    glucose_syrup.write_text("#!/bin/sh\n")
    glucose_syrup.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_glucose", None)
    sys.modules.pop("sagelite_glucose.runtime", None)

    assert Glucose().absolute_filename() == os.fspath(glucose)
    assert Glucose("glucose-syrup").absolute_filename() == os.fspath(glucose_syrup)


def test_kissat_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_kissat"
    bindir = package / "data" / "bin"
    executable = bindir / "kissat"
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
    sys.modules.pop("sagelite_kissat", None)
    sys.modules.pop("sagelite_kissat.runtime", None)

    assert Kissat().absolute_filename() == os.fspath(executable)
