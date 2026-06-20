from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
import types
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _stub_sage_env(monkeypatch, maxima_fas=""):
    sage = types.ModuleType("sage")
    sage.__path__ = []
    env = types.ModuleType("sage.env")
    env.MAXIMA_FAS = maxima_fas
    monkeypatch.setitem(sys.modules, "sage", sage)
    monkeypatch.setitem(sys.modules, "sage.env", env)


def _load_selftest():
    path = ROOT / "src" / "sage" / "cli" / "selftest.py"
    spec = importlib.util.spec_from_file_location("sage_cli_selftest", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _load_native_catalog():
    path = ROOT / "tools" / "sagelite_native_wheel_catalog.py"
    spec = importlib.util.spec_from_file_location("sagelite_native_wheel_catalog", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_selftest_rejects_private_cypari_pari_runtime(monkeypatch, tmp_path):
    selftest = _load_selftest()
    package_dir = tmp_path / "site-packages" / "cypari2"
    package_dir.mkdir(parents=True)
    origin = package_dir / "__init__.py"
    origin.write_text("", encoding="utf-8")
    private_libs = tmp_path / "site-packages" / "cypari2.libs"
    private_libs.mkdir()
    (private_libs / "libpari-3a78ce10.so.2.17.2").write_text(
        "private pari runtime\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        selftest.importlib.util,
        "find_spec",
        lambda name: importlib.machinery.ModuleSpec(name, loader=None, origin=origin),
    )

    with pytest.raises(RuntimeError, match="private PARI runtime"):
        selftest._check_single_pari_runtime()


def test_selftest_accepts_cypari_without_private_pari_runtime(
    monkeypatch, tmp_path
):
    selftest = _load_selftest()
    package_dir = tmp_path / "site-packages" / "cypari2"
    package_dir.mkdir(parents=True)
    origin = package_dir / "__init__.py"
    origin.write_text("", encoding="utf-8")

    monkeypatch.setattr(
        selftest.importlib.util,
        "find_spec",
        lambda name: importlib.machinery.ModuleSpec(name, loader=None, origin=origin),
    )

    assert (
        selftest._check_single_pari_runtime()
        == "cypari2 does not carry a private PARI runtime"
    )


def test_selftest_continues_after_pari_runtime_packaging_failure(monkeypatch):
    selftest = _load_selftest()
    calls = []

    def run_check(name, check):
        calls.append(name)
        return name != "PARI runtime packaging"

    monkeypatch.setattr(selftest, "_run_check", run_check)

    assert selftest.main([]) == 1
    assert calls[:3] == [
        "installed package requirements",
        "PARI runtime packaging",
        "PARI runtime conversion",
    ]
    assert "Maxima library runtime" in calls
    assert "required native imports" in calls
    assert "import sage.all" in calls


def test_selftest_help_does_not_run_runtime_checks(monkeypatch, capsys):
    selftest = _load_selftest()

    def run_check(name, check):
        raise AssertionError(f"unexpected runtime check: {name}")

    monkeypatch.setattr(selftest, "_run_check", run_check)

    with pytest.raises(SystemExit) as exc:
        selftest.main(["--help"])

    assert exc.value.code == 0
    assert "Run a quick smoke test" in capsys.readouterr().out


def test_selftest_main_accepts_explicit_empty_argv(monkeypatch):
    selftest = _load_selftest()
    calls = []

    def run_check(name, check):
        calls.append(name)
        return name != "PARI runtime packaging"

    monkeypatch.setattr(selftest, "_run_check", run_check)

    assert selftest.main([]) == 1
    assert calls[:3] == [
        "installed package requirements",
        "PARI runtime packaging",
        "PARI runtime conversion",
    ]
    assert "required native imports" in calls
    assert "import sage.all" in calls


def test_selftest_runs_pari_conversion_before_broader_checks(monkeypatch):
    selftest = _load_selftest()
    calls = []

    def run_check(name, check):
        calls.append(name)
        return name != "PARI runtime conversion"

    monkeypatch.setattr(selftest, "_run_check", run_check)

    assert selftest.main([]) == 1
    assert calls[:4] == [
        "installed package requirements",
        "PARI runtime packaging",
        "PARI runtime conversion",
        "Maxima library runtime",
    ]
    assert calls.index("PARI runtime conversion") < calls.index("import sage.all")


def test_selftest_pari_conversion_uses_labeled_subprocess_probe(monkeypatch):
    selftest = _load_selftest()
    probes = []

    def run_subprocess_probe(script, description="runtime probe", timeout=30):
        probes.append((script, description, timeout))
        return "5"

    monkeypatch.setattr(selftest, "_run_subprocess_probe", run_subprocess_probe)

    assert selftest._check_pari_runtime_roundtrip() == "5"
    assert probes == [(selftest._PARI_RUNTIME_PROBE, "PARI runtime probe", 30)]


def test_selftest_pari_probe_checks_loaded_runtime_before_conversion():
    selftest = _load_selftest()

    assert (
        "from sage.cli.selftest import _check_loaded_pari_runtime"
        in selftest._PARI_RUNTIME_PROBE
    )
    assert (
        selftest._PARI_RUNTIME_PROBE.index("_check_loaded_pari_runtime()")
        < selftest._PARI_RUNTIME_PROBE.index("primitive_root")
    )


def test_selftest_rejects_multiple_loaded_pari_runtimes(monkeypatch, tmp_path):
    selftest = _load_selftest()
    system_pari = tmp_path / "usr" / "libpari-gmp-tls.so.2.17.3"
    bundled_pari = (
        tmp_path / "site-packages" / "sagelite.libs" / "libpari-abc.so.2.17.3"
    )
    system_pari.parent.mkdir(parents=True)
    bundled_pari.parent.mkdir(parents=True)
    system_pari.write_text("system pari\n", encoding="utf-8")
    bundled_pari.write_text("bundled pari\n", encoding="utf-8")

    imported = []

    def import_module(name):
        imported.append(name)
        return object()

    monkeypatch.setattr(selftest.importlib, "import_module", import_module)
    monkeypatch.setattr(
        selftest, "_loaded_libpari_paths", lambda: [system_pari, bundled_pari]
    )

    with pytest.raises(RuntimeError, match="multiple PARI runtime libraries"):
        selftest._check_loaded_pari_runtime()

    assert imported == ["sage.libs.pari.convert_gmp", "cypari2.pari_instance"]


def test_selftest_accepts_single_loaded_pari_runtime(monkeypatch, tmp_path):
    selftest = _load_selftest()
    bundled_pari = (
        tmp_path / "site-packages" / "sagelite.libs" / "libpari-abc.so.2.17.3"
    )
    bundled_pari.parent.mkdir(parents=True)
    bundled_pari.write_text("bundled pari\n", encoding="utf-8")

    monkeypatch.setattr(selftest.importlib, "import_module", lambda name: object())
    monkeypatch.setattr(selftest, "_loaded_libpari_paths", lambda: [bundled_pari])

    assert (
        selftest._check_loaded_pari_runtime()
        == "loaded PARI runtime: libpari-abc.so.2.17.3"
    )


def test_selftest_rejects_maxima_fas_with_mismatched_loaded_ecl(
    monkeypatch, tmp_path
):
    selftest = _load_selftest()
    maxima_fas = tmp_path / "maxima.fas"
    loaded_libecl = tmp_path / "libecl.so.24.5"
    maxima_fas.write_bytes(b"compiled image needs FEstack_advance")
    loaded_libecl.write_text("loaded ecl runtime\n", encoding="utf-8")

    class Runtime:
        @staticmethod
        def maxima_fas():
            return str(maxima_fas)

    original_import_module = selftest.importlib.import_module

    def import_module(name):
        if name == "sagelite_maxima.runtime":
            return Runtime
        if name == "sage.libs.ecl":
            return object()
        return original_import_module(name)

    monkeypatch.setattr(selftest.importlib, "import_module", import_module)
    monkeypatch.setattr(selftest, "_loaded_libecl_paths", lambda: [loaded_libecl])
    monkeypatch.setattr(selftest, "_library_exports_symbol", lambda path, symbol: False)
    _stub_sage_env(monkeypatch, str(maxima_fas))

    with pytest.raises(RuntimeError, match="requires FEstack_advance"):
        selftest._check_loaded_ecl_matches_maxima_runtime()


def test_selftest_accepts_maxima_fas_with_matching_loaded_ecl(
    monkeypatch, tmp_path
):
    selftest = _load_selftest()
    maxima_fas = tmp_path / "maxima.fas"
    loaded_libecl = tmp_path / "libecl.so.24.5"
    maxima_fas.write_bytes(b"compiled image needs FEstack_advance")
    loaded_libecl.write_text("loaded ecl runtime\n", encoding="utf-8")

    class Runtime:
        @staticmethod
        def maxima_fas():
            return str(maxima_fas)

    original_import_module = selftest.importlib.import_module

    def import_module(name):
        if name == "sagelite_maxima.runtime":
            return Runtime
        if name == "sage.libs.ecl":
            return object()
        return original_import_module(name)

    monkeypatch.setattr(selftest.importlib, "import_module", import_module)
    monkeypatch.setattr(selftest, "_loaded_libecl_paths", lambda: [loaded_libecl])
    monkeypatch.setattr(selftest, "_library_exports_symbol", lambda path, symbol: True)
    _stub_sage_env(monkeypatch, str(maxima_fas))

    assert (
        selftest._check_loaded_ecl_matches_maxima_runtime()
        == "loaded ECL exports Maxima image symbols"
    )


def test_selftest_continues_after_maxima_runtime_packaging_failure(monkeypatch):
    selftest = _load_selftest()
    calls = []

    def run_check(name, check):
        calls.append(name)
        return name != "Maxima library runtime"

    monkeypatch.setattr(selftest, "_run_check", run_check)

    assert selftest.main([]) == 1
    assert calls[:6] == [
        "installed package requirements",
        "PARI runtime packaging",
        "PARI runtime conversion",
        "Maxima library runtime",
        "required native imports",
        "import sage.all",
    ]
    assert "symbolic integration" in calls


def test_selftest_rejects_required_native_import_failures(monkeypatch):
    selftest = _load_selftest()

    def import_module(name):
        if name == "broken.module":
            raise ImportError("libbroken.so: cannot open shared object file")
        return object()

    monkeypatch.setattr(
        selftest,
        "_required_native_import_modules",
        lambda: ["ok.module", "broken.module"],
    )
    monkeypatch.setattr(selftest.importlib, "import_module", import_module)

    with pytest.raises(RuntimeError, match="required sagelite native modules"):
        selftest._check_required_native_imports()


def test_selftest_accepts_required_native_imports(monkeypatch):
    selftest = _load_selftest()

    monkeypatch.setattr(
        selftest,
        "_required_native_import_modules",
        lambda: ["ok.module", "other.module"],
    )
    monkeypatch.setattr(selftest.importlib, "import_module", lambda name: object())

    assert (
        selftest._check_required_native_imports()
        == "2 required native modules import"
    )


def test_selftest_native_import_fallback_matches_catalog():
    selftest = _load_selftest()
    catalog = _load_native_catalog()

    assert selftest._FALLBACK_REQUIRED_NATIVE_IMPORT_MODULES == (
        catalog.REQUIRED_NATIVE_IMPORT_MODULES
    )


def test_selftest_continues_after_required_native_import_failure(monkeypatch):
    selftest = _load_selftest()
    calls = []

    def run_check(name, check):
        calls.append(name)
        return name != "required native imports"

    monkeypatch.setattr(selftest, "_run_check", run_check)

    assert selftest.main([]) == 1
    assert calls[:6] == [
        "installed package requirements",
        "PARI runtime packaging",
        "PARI runtime conversion",
        "Maxima library runtime",
        "required native imports",
        "import sage.all",
    ]
    assert "symbolic integration" in calls


def test_selftest_maxima_probe_exercises_runtime_parity_checks():
    selftest = _load_selftest()
    probe = selftest._MAXIMA_RUNTIME_PROBE

    assert 'maxima.help("gcd")' in probe
    assert 'maxima.example("arrays")' in probe
    assert "maxima_lib.sr_integral(sin(x), x)._sage_()" in probe
    assert "Maxima help is not available" in probe
    assert "Maxima examples are not available" in probe
    assert "Maxima library-mode integration is not available" in probe


def test_selftest_runs_maxima_before_symbolic_integration(monkeypatch):
    selftest = _load_selftest()
    calls = []

    def run_check(name, check):
        calls.append(name)
        return name != "symbolic integration"

    monkeypatch.setattr(selftest, "_run_check", run_check)
    monkeypatch.setattr(selftest, "_optional_runtime_summary", lambda: None)

    assert selftest.main([]) == 1
    assert calls[:5] == [
        "installed package requirements",
        "PARI runtime packaging",
        "PARI runtime conversion",
        "Maxima library runtime",
        "required native imports",
    ]
    assert calls[:6] == [
        "installed package requirements",
        "PARI runtime packaging",
        "PARI runtime conversion",
        "Maxima library runtime",
        "required native imports",
        "import sage.all",
    ]
    assert calls.index("Maxima library runtime") < calls.index("symbolic integration")


def test_selftest_exercises_remaining_standard_companion_runtimes(monkeypatch):
    selftest = _load_selftest()
    calls = []

    def run_check(name, check):
        calls.append(name)
        return True

    monkeypatch.setattr(selftest, "_run_check", run_check)
    monkeypatch.setattr(selftest, "_optional_runtime_summary", lambda: None)

    assert selftest.main([]) == 0

    for name in (
        "ECL executable runtime",
        "sympow executable runtime",
        "Tachyon executable runtime",
        "MathJax static runtime",
        "Cubic Hecke database runtime",
        "KnotInfo database runtime",
        "matroid database runtime",
    ):
        assert name in calls


def test_subprocess_probe_reports_probe_description(tmp_path):
    selftest = _load_selftest()
    script = tmp_path / "fail.py"
    script.write_text(
        "import sys; print('out'); print('err', file=sys.stderr); sys.exit(7)"
    )

    with pytest.raises(RuntimeError, match="PARI runtime probe exited with status 7"):
        selftest._run_subprocess_probe(
            f"exec({script.read_text()!r})", "PARI runtime probe"
        )
