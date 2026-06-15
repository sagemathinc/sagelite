from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _load_analyzer():
    path = Path(__file__).with_name("analyze-doctest-log.py")
    spec = importlib.util.spec_from_file_location("analyze_doctest_log", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_parse_installed_module_failure_blocks(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """Running doctests with ID 2026-06-12-00-34-09-32ed3b2e.
Doctesting all installed modules of the Sage library.
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/calculus/calculus.py", line 64, in sage.calculus.calculus
Failed example:
    g = f.integral(x); g
Exception raised:
    Traceback (most recent call last):
    RuntimeError: ECL says: Module error: Don't know how to REQUIRE MAXIMA.
    ImportError: Maxima library mode is unavailable in this Sage installation: ECL says: Module error: Don't know how to REQUIRE MAXIMA.
**********************************************************************
1 item had failures:
   1 of  12 in sage.calculus.calculus
    7 tests not run because we ran out of time
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    report = analyzer.build_report(results)

    assert list(results) == ["sage.calculus.calculus"]
    result = results["sage.calculus.calculus"]
    assert result.status == "failed"
    assert result.failed_examples == 1
    assert result.traceback_lines[-1].startswith("ImportError: Maxima library mode")
    assert report["fingerprint_counts"] == {"maxima-library-mode-missing": 1}
    assert result.suggested_package == "sagelite-maxima-runtime >=10.9.post11"
    assert (
        report["top_examples"]["optional-external"][0]["suggested_package"]
        == "sagelite-maxima-runtime >=10.9.post11"
    )


def test_report_suggests_cremona_companion_package(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/calculus/expr.py", line 47, in sage.calculus.expr.symbolic_expression
Failed example:
    E = EllipticCurve('15a'); E
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: database_cremona_mini_ellcurve is not available.
    'cremona_mini.db' not found in any of ['/usr/share/cremona']
**********************************************************************
1 item had failures:
   1 of  11 in sage.calculus.expr.symbolic_expression
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    report = analyzer.build_report(results)
    result = results["sage.calculus.expr"]

    assert result.fingerprint == "missing-cremona-db"
    assert result.suggested_package == "sagelite-database-cremona-mini"
    assert (
        report["top_examples"]["optional-data"][0]["suggested_package"]
        == "sagelite-database-cremona-mini"
    )


def test_report_identifies_maxima_runtime_abi_mismatch(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/calculus/var.pyx", line 70, in sage.calculus.var.var
Failed example:
    x = var('x', domain=RR); x; x.conjugate()
Exception raised:
    Traceback (most recent call last):
    RuntimeError: ECL says: LOAD: Could not load file #P"/.venv/lib/python3.12/site-packages/sagelite_maxima/data/lib/ecl-24.5.10/maxima.fas" (Error: "/.venv/lib/python3.12/site-packages/sagelite_maxima/data/lib/ecl-24.5.10/maxima.fas: undefined symbol: FEstack_advance")
    ImportError: Maxima library mode is unavailable in this Sage installation: ECL says: LOAD: Could not load file #P"/.venv/lib/python3.12/site-packages/sagelite_maxima/data/lib/ecl-24.5.10/maxima.fas" (Error: "/.venv/lib/python3.12/site-packages/sagelite_maxima/data/lib/ecl-24.5.10/maxima.fas: undefined symbol: FEstack_advance")
**********************************************************************
1 item had failures:
   1 of  22 in sage.calculus.var.var
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    report = analyzer.build_report(results)
    result = results["sage.calculus.var"]

    assert result.fingerprint == "maxima-runtime-abi-mismatch"
    assert result.evidence == "Maxima runtime wheel is ABI-incompatible with the loaded ECL library"
    assert result.suggested_package == "sagelite-maxima-runtime >=10.9.post11"
    assert report["fingerprint_counts"] == {"maxima-runtime-abi-mismatch": 1}


def test_report_identifies_mixed_pari_runtime_crash(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/modular/modsym/modsym.py", line 64, in sage.modular.modsym.modsym
Failed example:
    ModularSymbols(389, sign=1).T(2).fcp()
Exception raised:
    Traceback (most recent call last):
    File "cypari2/gen.pyx", line 4782, in cypari2.gen.objtogen
    File "sage/libs/pari/convert_sage.pyx", line 401, in sage.libs.pari.convert_sage.new_gen_from_integer
    File "sage/libs/pari/convert_gmp.pyx", line 52, in sage.libs.pari.convert_gmp.new_gen_from_mpz_t
    cysignals.signals.SignalError: Segmentation fault
**********************************************************************
1 item had failures:
   1 of  8 in sage.modular.modsym.modsym
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    report = analyzer.build_report(results)
    result = results["sage.modular.modsym.modsym"]

    assert result.category == "optional-external"
    assert result.fingerprint == "mixed-pari-runtime"
    assert result.suggested_package == (
        "rebuild sagelite with source-built cypari2 and one repaired libpari"
    )
    assert report["fingerprint_counts"] == {"mixed-pari-runtime": 1}


def test_report_suggests_runtime_for_named_missing_executable(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/geometry/polyhedron/backend_cdd.py", line 42, in sage.geometry.polyhedron.backend_cdd
Failed example:
    polytopes.hypercube(3).Hrepresentation()
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: cddexec_gmp is not available.
    Executable 'cddexec_gmp' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.geometry.polyhedron.backend_cdd
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    report = analyzer.build_report(results)
    result = results["sage.geometry.polyhedron.backend_cdd"]

    assert result.fingerprint == "missing-executable"
    assert result.suggested_package == "sagelite-cddlib-runtime"
    assert (
        report["top_examples"]["optional-external"][0]["suggested_package"]
        == "sagelite-cddlib-runtime"
    )


def test_report_suggests_runtime_for_named_missing_database(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/rings/polynomial/kohel.py", line 42, in sage.rings.polynomial.kohel
Failed example:
    ClassicalModularPolynomialDatabase()[5]
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: database_kohel is not available.
    'PolMod/Cls/pol.005.dbz' not found in any of ['/usr/share/kohel']
**********************************************************************
1 item had failures:
   1 of   5 in sage.rings.polynomial.kohel
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    report = analyzer.build_report(results)
    result = results["sage.rings.polynomial.kohel"]

    assert result.fingerprint == "missing-database"
    assert result.suggested_package == "sagelite-database-kohel"
    assert (
        report["top_examples"]["optional-data"][0]["suggested_package"]
        == "sagelite-database-kohel"
    )
