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
    assert result.suggested_package == "sagelite-maxima-runtime"
    assert (
        report["top_examples"]["optional-external"][0]["suggested_package"]
        == "sagelite-maxima-runtime"
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
