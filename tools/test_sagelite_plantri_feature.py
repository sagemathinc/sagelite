import importlib.util
import os
import sys
from pathlib import Path

import sage


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "build" / "sage-distro" / "src" / "sage" / "config.py"
if not hasattr(sage, "config") and CONFIG_PATH.exists():
    spec = importlib.util.spec_from_file_location("sage.config", CONFIG_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["sage.config"] = module
    spec.loader.exec_module(module)
    sage.config = module

import sage.features
import sage.env


def _load_source_feature_module(name):
    path = ROOT / "src" / "sage" / "features" / f"{name}.py"
    fullname = f"sage.features.{name}"
    if not path.exists():
        return __import__(fullname, fromlist=["*"])
    sys.modules.pop(fullname, None)
    spec = importlib.util.spec_from_file_location(fullname, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[fullname] = module
    spec.loader.exec_module(module)
    return module


sage.env.GFAN_BINS_PREFIX = getattr(sage.env, "GFAN_BINS_PREFIX", "")
sage.env.LATTE_BINS_PREFIX = getattr(sage.env, "LATTE_BINS_PREFIX", "")
sage.env.PALP_BINS_PREFIX = getattr(sage.env, "PALP_BINS_PREFIX", "")
sage.env.SAGE_NAUTY_BINS_PREFIX = getattr(sage.env, "SAGE_NAUTY_BINS_PREFIX", "")
sage.env.SAGE_ECMBIN = getattr(sage.env, "SAGE_ECMBIN", "ecm")

ecm_module = _load_source_feature_module("ecm")
four_ti_2_module = _load_source_feature_module("four_ti_2")
gfan_module = _load_source_feature_module("gfan")
graph_generators_module = _load_source_feature_module("graph_generators")
latte_module = _load_source_feature_module("latte")
msolve_module = _load_source_feature_module("msolve")
nauty_module = _load_source_feature_module("nauty")
palp_module = _load_source_feature_module("palp")

Ecm = ecm_module.Ecm
FourTi2Executable = four_ti_2_module.FourTi2Executable
GfanExecutable = gfan_module.GfanExecutable
Benzene = graph_generators_module.Benzene
Plantri = graph_generators_module.Plantri
Latte_count = latte_module.Latte_count
Latte_integrate = latte_module.Latte_integrate
msolve = msolve_module.msolve
NautyExecutable = nauty_module.NautyExecutable
PalpExecutable = palp_module.PalpExecutable


def _write_fake_runtime(tmp_path, package_name, program, path_function):
    package = tmp_path / package_name
    bindir = package / "data" / "bin"
    executable = bindir / program
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        f"def {path_function}(*args):\n"
        f"    program = args[0] if args else {program!r}\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / program\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)
    return executable


def test_benzene_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_benzene"
    bindir = package / "data" / "bin"
    executable = bindir / "benzene"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'benzene'\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_benzene", None)
    sys.modules.pop("sagelite_benzene.runtime", None)

    feature = Benzene()

    assert feature.absolute_filename() == os.fspath(executable)


def test_plantri_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_plantri"
    bindir = package / "data" / "bin"
    executable = bindir / "plantri"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'plantri'\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_plantri", None)
    sys.modules.pop("sagelite_plantri.runtime", None)

    feature = Plantri()

    assert feature.absolute_filename() == os.fspath(executable)


def test_msolve_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_msolve"
    bindir = package / "data" / "bin"
    executable = bindir / "msolve"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'msolve'\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_msolve", None)
    sys.modules.pop("sagelite_msolve.runtime", None)

    feature = msolve()

    assert feature.absolute_filename() == os.fspath(executable)


def test_four_ti_2_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_four_ti_2", "hilbert", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_four_ti_2", None)
    sys.modules.pop("sagelite_four_ti_2.runtime", None)

    feature = FourTi2Executable("hilbert")

    assert feature.absolute_filename() == os.fspath(executable)


def test_gfan_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_gfan", "gfan_groebnercone", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_gfan", None)
    sys.modules.pop("sagelite_gfan.runtime", None)

    feature = GfanExecutable("groebnercone")

    assert feature.absolute_filename() == os.fspath(executable)


def test_nauty_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_nauty", "geng", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_nauty", None)
    sys.modules.pop("sagelite_nauty.runtime", None)

    feature = NautyExecutable("geng")

    assert feature.absolute_filename() == os.fspath(executable)


def test_ecm_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(tmp_path, "sagelite_ecm", "ecm", "executable_path")

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_ecm", None)
    sys.modules.pop("sagelite_ecm.runtime", None)

    feature = Ecm()

    assert feature.absolute_filename() == os.fspath(executable)


def test_palp_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_palp", "poly-4d.x", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_palp", None)
    sys.modules.pop("sagelite_palp.runtime", None)

    feature = PalpExecutable("poly", 4)

    assert feature.absolute_filename() == os.fspath(executable)


def test_latte_count_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_latte", "count", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_latte", None)
    sys.modules.pop("sagelite_latte.runtime", None)

    feature = Latte_count()

    assert feature.absolute_filename() == os.fspath(executable)


def test_latte_integrate_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_latte", "integrate", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_latte", None)
    sys.modules.pop("sagelite_latte.runtime", None)

    feature = Latte_integrate()

    assert feature.absolute_filename() == os.fspath(executable)
