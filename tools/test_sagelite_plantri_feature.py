import importlib.util
import os
import subprocess
import sys
import types
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


def _load_source_module(relative_path, fullname):
    path = ROOT / relative_path
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
sage.env.SAGE_GAP3_COMMAND = getattr(sage.env, "SAGE_GAP3_COMMAND", "gap3")

ecm_module = _load_source_feature_module("ecm")
cddlib_module = _load_source_feature_module("cddlib")
csdp_module = _load_source_feature_module("csdp")
four_ti_2_module = _load_source_feature_module("four_ti_2")
frobby_module = _load_source_feature_module("frobby")
gfan_module = _load_source_feature_module("gfan")
graph_generators_module = _load_source_feature_module("graph_generators")
gap3_module = _load_source_feature_module("gap3")
latte_module = _load_source_feature_module("latte")
flatter_module = _load_source_feature_module("flatter")
lrs_module = _load_source_feature_module("lrs")
msolve_module = _load_source_feature_module("msolve")
nauty_module = _load_source_feature_module("nauty")
palp_module = _load_source_feature_module("palp")
planarity_module = _load_source_feature_module("planarity")
qepcad_module = _load_source_feature_module("qepcad")
rubiks_module = _load_source_feature_module("rubiks")
sat_module = _load_source_feature_module("sat")
topcom_module = _load_source_feature_module("topcom")

Ecm = ecm_module.Ecm
CddExecutable = cddlib_module.CddExecutable
CSDP = csdp_module.CSDP
FourTi2Executable = four_ti_2_module.FourTi2Executable
Frobby = frobby_module.Frobby
GfanExecutable = gfan_module.GfanExecutable
Gap3 = gap3_module.Gap3
Benzene = graph_generators_module.Benzene
Plantri = graph_generators_module.Plantri
Latte_count = latte_module.Latte_count
Latte_integrate = latte_module.Latte_integrate
Lrs = lrs_module.Lrs
LrsNash = lrs_module.LrsNash
msolve = msolve_module.msolve
NautyExecutable = nauty_module.NautyExecutable
PalpExecutable = palp_module.PalpExecutable
Planarity = planarity_module.Planarity
Qepcad = qepcad_module.Qepcad
RubiksExecutable = rubiks_module.RubiksExecutable
Glucose = sat_module.Glucose
Kissat = sat_module.Kissat
TOPCOMExecutable = topcom_module.TOPCOMExecutable


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


def _load_lcalc_module(monkeypatch):
    modules = {
        "sage.structure": types.ModuleType("sage.structure"),
        "sage.structure.sage_object": types.ModuleType("sage.structure.sage_object"),
        "sage.misc.lazy_import": types.ModuleType("sage.misc.lazy_import"),
        "sage.misc.pager": types.ModuleType("sage.misc.pager"),
        "sage.rings.integer_ring": types.ModuleType("sage.rings.integer_ring"),
        "sage.rings.rational_field": types.ModuleType("sage.rings.rational_field"),
    }
    modules["sage.structure.sage_object"].SageObject = object
    modules["sage.misc.lazy_import"].lazy_import = lambda *args, **kwargs: None
    modules["sage.misc.pager"].pager = lambda: (lambda text: None)
    modules["sage.rings.integer_ring"].ZZ = int
    modules["sage.rings.rational_field"].QQ = object()
    for name, module in modules.items():
        monkeypatch.setitem(sys.modules, name, module)
    return _load_source_module("src/sage/lfunctions/lcalc.py", "sage.lfunctions.lcalc")


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


def test_sagelite_selftest_nauty_runtime_uses_companion_paths(monkeypatch, tmp_path):
    geng = _write_fake_runtime(
        tmp_path, "sagelite_nauty", "geng", "executable_path"
    )
    bindir = geng.parent
    for program in (
        "directg",
        "gentourng",
        "genbg",
        "gentreeg",
        "genktreeg",
        "genposetg",
    ):
        executable = bindir / program
        executable.write_text("#!/bin/sh\n")
        executable.chmod(0o755)
    genposetg = bindir / "genposetg"
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    monkeypatch.setattr(subprocess, "run", fake_run)
    sys.modules.pop("sagelite_nauty", None)
    sys.modules.pop("sagelite_nauty.runtime", None)
    sys.modules.pop("sage.features.nauty", None)
    monkeypatch.delattr(sage.features, "nauty", raising=False)
    sage.features._trivial_unique_representation_cache.clear()

    from sagelite_nauty.runtime import executable_path

    assert executable_path("geng") == geng
    assert executable_path("genposetg") == genposetg

    loaded_nauty = _load_source_feature_module("nauty")
    assert loaded_nauty.NautyExecutable("geng").absolute_filename() == os.fspath(geng)
    sage.features._trivial_unique_representation_cache.clear()

    selftest = _load_source_module("src/sage/cli/selftest.py", "sage.cli.selftest")

    assert selftest._check_nauty_runtime() == "geng and genposetg available"
    assert [call[0] for call in calls] == [
        [os.fspath(geng), "-q", "3"],
        [os.fspath(genposetg), "-q", "3"],
    ]


def test_ecm_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(tmp_path, "sagelite_ecm", "ecm", "executable_path")

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_ecm", None)
    sys.modules.pop("sagelite_ecm.runtime", None)

    feature = Ecm()

    assert feature.absolute_filename() == os.fspath(executable)


def test_cddlib_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_cddlib", "cddexec_gmp", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_cddlib", None)
    sys.modules.pop("sagelite_cddlib.runtime", None)

    feature = CddExecutable()

    assert feature.absolute_filename() == os.fspath(executable)


def test_csdp_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_csdp", "theta", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_csdp", None)
    sys.modules.pop("sagelite_csdp.runtime", None)

    feature = CSDP()

    assert feature.absolute_filename() == os.fspath(executable)


def test_frobby_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_frobby", "frobby", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_frobby", None)
    sys.modules.pop("sagelite_frobby.runtime", None)

    feature = Frobby()

    assert feature.absolute_filename() == os.fspath(executable)


def test_planarity_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_planarity", "planarity", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_planarity", None)
    sys.modules.pop("sagelite_planarity.runtime", None)

    feature = Planarity()

    assert feature.absolute_filename() == os.fspath(executable)


def test_qepcad_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_qepcad", "qepcad", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_qepcad", None)
    sys.modules.pop("sagelite_qepcad.runtime", None)

    feature = Qepcad()

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


def test_lrslib_lrs_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_lrslib", "lrs", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_lrslib", None)
    sys.modules.pop("sagelite_lrslib.runtime", None)

    feature = Lrs()

    assert feature.absolute_filename() == os.fspath(executable)


def test_lrslib_lrsnash_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_lrslib", "lrsnash", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_lrslib", None)
    sys.modules.pop("sagelite_lrslib.runtime", None)

    feature = LrsNash()

    assert feature.absolute_filename() == os.fspath(executable)


def test_rubiks_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_rubiks", "cubex", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    monkeypatch.setattr(rubiks_module, "RUBIKS_BINS_PREFIX", "")
    sys.modules.pop("sagelite_rubiks", None)
    sys.modules.pop("sagelite_rubiks.runtime", None)

    feature = RubiksExecutable("cubex")

    assert feature.absolute_filename() == os.fspath(executable)


def test_glucose_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_glucose", "glucose", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_glucose", None)
    sys.modules.pop("sagelite_glucose.runtime", None)

    feature = Glucose()

    assert feature.absolute_filename() == os.fspath(executable)


def test_kissat_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_kissat", "kissat", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_kissat", None)
    sys.modules.pop("sagelite_kissat.runtime", None)

    feature = Kissat()

    assert feature.absolute_filename() == os.fspath(executable)


def test_topcom_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_topcom", "points2allfinetriangs", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.delenv("LD_LIBRARY_PATH", raising=False)
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_topcom", None)
    sys.modules.pop("sagelite_topcom.runtime", None)

    feature = TOPCOMExecutable("points2allfinetriangs")

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


def test_flatter_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_flatter", "flatter", "executable_path"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_flatter", None)
    sys.modules.pop("sagelite_flatter.runtime", None)

    feature = flatter_module.flatter()

    assert feature.absolute_filename() == os.fspath(executable)


def test_lcalc_interface_discovers_sagelite_companion(monkeypatch, tmp_path):
    executable = _write_fake_runtime(
        tmp_path, "sagelite_lcalc", "lcalc", "lcalc_command"
    )
    calls = []

    def fake_run(command, **kwargs):
        calls.append((command, kwargs))
        return subprocess.CompletedProcess(command, 0, "14.1347251\n", "")

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(subprocess, "run", fake_run)
    sys.modules.pop("sagelite_lcalc", None)
    sys.modules.pop("sagelite_lcalc.runtime", None)

    assert _load_lcalc_module(monkeypatch).LCalc()("-z 1") == "14.1347251"
    assert calls == [
        (
            [os.fspath(executable), "-z", "1"],
            {"stdout": subprocess.PIPE, "text": True},
        )
    ]


def test_gap3_executable_discovers_sagelite_companion(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_gap3"
    bindir = package / "data" / "gap3" / "bin"
    executable = bindir / "gap.sh"
    package.mkdir()
    bindir.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def gap3_command():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'gap3' / 'bin' / 'gap.sh'\n"
    )
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(gap3_module, "SAGE_GAP3_COMMAND", "gap3")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_gap3", None)
    sys.modules.pop("sagelite_gap3.runtime", None)

    feature = Gap3()

    assert feature.absolute_filename() == os.fspath(executable)
