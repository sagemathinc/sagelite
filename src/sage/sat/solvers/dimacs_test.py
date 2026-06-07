import os
import sys

import sage.features
from sage.sat.solvers.dimacs import Glucose, GlucoseSyrup, Kissat


def _write_fake_sat_runtime(tmp_path, package_name, *programs):
    package = tmp_path / package_name
    bindir = package / "data" / "bin"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path(program):\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / program\n"
    )
    for program in programs:
        executable = bindir / program
        executable.write_text("#!/bin/sh\n")
        executable.chmod(0o755)
    return bindir


def test_glucose_dimacs_command_discovers_sagelite_companion(monkeypatch, tmp_path):
    bindir = _write_fake_sat_runtime(
        tmp_path, "sagelite_glucose", "glucose", "glucose-syrup"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_glucose", None)
    sys.modules.pop("sagelite_glucose.runtime", None)

    assert Glucose()._command == f"{bindir / 'glucose'} -verb=0 -model {{input}}"
    assert GlucoseSyrup()._command == (
        f"{bindir / 'glucose-syrup'} -model -verb=0 {{input}}"
    )


def test_kissat_dimacs_command_discovers_sagelite_companion(monkeypatch, tmp_path):
    bindir = _write_fake_sat_runtime(tmp_path, "sagelite_kissat", "kissat")

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_kissat", None)
    sys.modules.pop("sagelite_kissat.runtime", None)

    assert Kissat()._command == f"{bindir / 'kissat'} -q {{input}}"


def test_dimacs_sat_solver_explicit_command_takes_precedence():
    assert Glucose(command="custom-glucose {input}")._command == "custom-glucose {input}"
    assert (
        GlucoseSyrup(command="custom-glucose-syrup {input}")._command
        == "custom-glucose-syrup {input}"
    )
    assert Kissat(command="custom-kissat {input}")._command == "custom-kissat {input}"
