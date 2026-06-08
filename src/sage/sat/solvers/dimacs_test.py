import importlib.util
import os
import sys
from pathlib import Path

import sage.features


ROOT = Path(__file__).resolve().parents[4]
FEATURE_MODULE_PATH = ROOT / "src" / "sage" / "features" / "sat.py"
feature_spec = importlib.util.spec_from_file_location(
    "sage.features.sat", FEATURE_MODULE_PATH
)
feature_module = importlib.util.module_from_spec(feature_spec)
sys.modules["sage.features.sat"] = feature_module
feature_spec.loader.exec_module(feature_module)

MODULE_PATH = ROOT / "src" / "sage" / "sat" / "solvers" / "dimacs.py"
spec = importlib.util.spec_from_file_location("sage.sat.solvers.dimacs", MODULE_PATH)
dimacs_module = importlib.util.module_from_spec(spec)
sys.modules["sage.sat.solvers.dimacs"] = dimacs_module
spec.loader.exec_module(dimacs_module)

Glucose = dimacs_module.Glucose
GlucoseSyrup = dimacs_module.GlucoseSyrup
Kissat = dimacs_module.Kissat


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
