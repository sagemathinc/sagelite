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
    assert result.suggested_package == "sagelite-maxima-runtime >=10.9.post13"
    assert (
        report["top_examples"]["optional-external"][0]["suggested_package"]
        == "sagelite-maxima-runtime >=10.9.post13"
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
    assert result.suggested_package == "sagelite-maxima-runtime >=10.9.post13"
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


def test_report_identifies_numeric_tolerance_mismatch(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/geometry/polyhedron/base.py", line 42, in sage.geometry.polyhedron.base
Failed example:
    P.volume()
Expected:
    2.598076211353316
Got:
    2.5980762113533165
**********************************************************************
1 item had failures:
   1 of  10 in sage.geometry.polyhedron.base
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    report = analyzer.build_report(results)
    result = results["sage.geometry.polyhedron.base"]

    assert result.fingerprint == "numeric-tolerance"
    assert report["fingerprint_counts"] == {"numeric-tolerance": 1}


def test_report_identifies_symbolic_output_variant(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/calculus/tests.py", line 42, in sage.calculus.tests
Failed example:
    integrate(1/(x^3+1), x)
Expected:
    1/3*sqrt(3)*arctan(1/3*sqrt(3)*(2*x - 1))
Got:
    1/3*sqrt(3)*arctan(2/3*sqrt(3)*x - 1/3*sqrt(3))
**********************************************************************
1 item had failures:
   1 of  10 in sage.calculus.tests
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.calculus.tests"]

    assert result.fingerprint == "symbolic-output-variant"


def test_report_identifies_maxima_symbolic_runtime_variant(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/interfaces/maxima_lib.py", line 973, in sage.interfaces.maxima_lib.MaximaLib.sr_integral
Failed example:
    integral(x^n,x)
Expected:
    Traceback (most recent call last):
    ...
    ValueError: Computation failed since Maxima requested additional
    constraints; using the 'assume' command before evaluation
    Is n equal to -1?
Got:
    cases(((n != -1, x^(n + 1)/(n + 1)), (1, log(x))))
**********************************************************************
1 item had failures:
   1 of  10 in sage.interfaces.maxima_lib.MaximaLib.sr_integral
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.interfaces.maxima_lib"]

    assert result.category == "optional-external"
    assert result.fingerprint == "maxima-symbolic-runtime-variant"
    assert (
        result.suggested_package
        == "sagelite-maxima-runtime parity investigation"
    )


def test_report_identifies_external_output_variant(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/geometry/polyhedron/base_QQ.py", line 42, in sage.geometry.polyhedron.base_QQ
Failed example:
    P.integral_points(verbose=True)
Expected:
    []
Got:
    Computing hermitean normal form.
    Time for reading and preprocessing: 0 sec
    Computing vertices and edges with cdd...done.
**********************************************************************
1 item had failures:
   1 of  10 in sage.geometry.polyhedron.base_QQ
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.geometry.polyhedron.base_QQ"]

    assert result.category == "optional-external"
    assert result.fingerprint == "external-output-variant"


def test_report_identifies_representative_choice(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/graphs/graph.py", line 42, in sage.graphs.graph
Failed example:
    g.topological_minor(H)
Expected:
    False
Got:
    Subgraph of (RandomGNP(15,0.300000000000000)): Graph on 0 vertices
**********************************************************************
1 item had failures:
   1 of  10 in sage.graphs.graph
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.graphs.graph"]

    assert result.fingerprint == "representative-choice"


def test_report_identifies_tropical_ordering_representative_choice(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/rings/semirings/tropical_variety.py", line 42, in sage.rings.semirings.tropical_variety
Failed example:
    tv._components_intersection()
Expected:
    {3: [((t1, t1, t1), {0 <= t1}), ((t1, 2*t1, 2*t1), {t1 <= 0})]}
Got:
    {3: [((t1, 2*t1, 2*t1), {t1 <= 0}), ((t1, t1, t1), {0 <= t1})]}
**********************************************************************
1 item had failures:
   1 of  10 in sage.rings.semirings.tropical_variety
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.rings.semirings.tropical_variety"]

    assert result.fingerprint == "representative-choice"


def test_report_identifies_riemann_surface_monodromy_representative_choice(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/schemes/riemann_surfaces/riemann_surface.py", line 42, in sage.schemes.riemann_surfaces.riemann_surface
Failed example:
    S.monodromy_group()
Expected:
    [(0,1,2), (0,1), (0,2)]
Got:
    [(0,2,1), (0,1), (1,2)]
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/schemes/riemann_surfaces/riemann_surface.py", line 57, in sage.schemes.riemann_surfaces.riemann_surface
Failed example:
    list(zip(S.branch_locus + [unsigned_infinity], G)) # abs tol 1e-7
Expected:
    [(0.000000000000000, (0,1,2)), (-1.31362670141929, (0,1))]
Got:
    [(0.000000000000000, (0,2,1)), (-1.31362670141929, (0,1))]
Tolerance exceeded in 1 of 6:
    1 vs 2, tolerance 1e0 > 1e-7
**********************************************************************
1 item had failures:
   1 of  10 in sage.schemes.riemann_surfaces.riemann_surface
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.schemes.riemann_surfaces.riemann_surface"]

    assert result.fingerprint == "representative-choice"


def test_report_identifies_color_hex_precision_variant(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/graphs/graph_coloring.py", line 42, in sage.graphs.graph_coloring
Failed example:
    sorted(d)
Expected:
    ['#0066ff', '#00ff66']
Got:
    ['#0065ff', '#00ff66']
**********************************************************************
1 item had failures:
   1 of  10 in sage.graphs.graph_coloring
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.graphs.graph_coloring"]

    assert result.category == "core-supported"
    assert result.fingerprint == "color-output-variant"


def test_report_identifies_gap_interrupt_behavior(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/interfaces/gap.py", line 42, in sage.interfaces.gap
Failed example:
    gap('"finished computation"'); gap.interrupt(); gap('"ok"')
Expected:
    finished computation
    True
    ok
Got:
    finished computation
    False
    ok
**********************************************************************
1 item had failures:
   1 of  10 in sage.interfaces.gap
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.interfaces.gap"]

    assert result.category == "optional-external"
    assert result.fingerprint == "gap-interrupt-behavior"
    assert result.suggested_package == "sagelite-gap-runtime"


def test_report_identifies_external_path_output_variant(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/interfaces/gp.py", line 42, in sage.interfaces.gp
Failed example:
    gp.get_default('datadir')
Expected:
    '.../share/pari'
Got:
    '/venv/lib/python3.12/site-packages/sagelite_pari_data/data/pari'
**********************************************************************
1 item had failures:
   1 of  10 in sage.interfaces.gp
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.interfaces.gp"]

    assert result.category == "optional-external"
    assert result.fingerprint == "external-path-output-variant"


def test_report_identifies_installed_sage_cli_option_gap(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/tests/cmdline.py", line 42, in sage.tests.cmdline
Failed example:
    err
Expected:
    ''
Got:
    'usage: sage [-h] [-v] [-q] [--simple-prompt] [-V] [-n [{jupyter,jupyterlab}]]\\n            [-c [COMMAND]]\\n            [file ...]\\nsage: error: unrecognized arguments: --python\\n'
**********************************************************************
1 item had failures:
   1 of  10 in sage.tests.cmdline
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.tests.cmdline"]

    assert result.category == "packaging-runtime"
    assert result.fingerprint == "installed-sage-cli-incomplete"


def test_report_identifies_installed_sage_cli_advanced_option_gap(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/tests/cmdline.py", line 146, in sage.tests.cmdline
Failed example:
    err
Expected:
    ''
Got:
    'usage: sage [-h] [-v] [-q] [--simple-prompt] [-V] [-n [{jupyter,jupyterlab}]]\\n            [-c [COMMAND]]\\n            [file ...]\\nsage: error: unrecognized arguments: --advanced\\n'
**********************************************************************
1 item had failures:
   1 of  10 in sage.tests.cmdline
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.tests.cmdline"]

    assert result.category == "packaging-runtime"
    assert result.fingerprint == "installed-sage-cli-incomplete"


def test_report_identifies_missing_doc_source(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage_docbuild/builders.py", line 42, in sage_docbuild.builders
Failed example:
    documents = get_all_documents(Path(SAGE_DOC_SRC))
Exception raised:
    Traceback (most recent call last):
    FileNotFoundError: [Errno 2] No such file or directory: '/venv/share/doc/sage'
**********************************************************************
1 item had failures:
   1 of  10 in sage_docbuild.builders
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage_docbuild.builders"]

    assert result.category == "optional-data"
    assert result.fingerprint == "missing-doc-source"


def test_report_identifies_build_tree_source_path_leak(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/misc/sageinspect.py", line 42, in sage.misc.sageinspect
Failed example:
    sage_getfile_relative(sage.rings.rational)
Expected:
    'sage/rings/rational.pyx'
Got:
    '/scratch/sagelite-build/src/sage/rings/rational.pyx'
**********************************************************************
1 item had failures:
   1 of  10 in sage.misc.sageinspect
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.misc.sageinspect"]

    assert result.category == "optional-external"
    assert result.fingerprint == "stale-build-path"


def test_report_identifies_slow_doctest_warning(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/functions/log.py", line 42, in sage.functions.log
Warning: slow doctest:
    integrate(cos(log(cos(x))), x, 0, pi/4)
Test ran for 41.67s cpu, 67.59s wall
Check ran for 0.00s cpu, 0.00s wall
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    report = analyzer.build_report(results)
    result = results["sage.functions.log"]

    assert result.category == "performance-only"
    assert result.fingerprint == "slow-doctest"
    assert result.traceback_lines[0] == "Warning: slow doctest:"
    assert report["fingerprint_counts"] == {"slow-doctest": 1}


def test_report_identifies_doctest_dependency_warning(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/matrix/matrix2.pyx", line 17195, in sage.matrix.matrix2.Matrix._echelon_form_PID
Warning: Variable 'OL' referenced here was set only in doctest marked '# needs sage.rings.number_field'
    m = matrix(OL, 0, 0, []); r,s,p = m._echelon_form_PID()
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.matrix.matrix2"]

    assert result.category == "core-supported"
    assert result.fingerprint == "doctest-dependency-warning"


def test_warning_does_not_override_failed_example(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/symbolic/expression.pyx", line 42, in sage.symbolic.expression
Warning: slow doctest:
    integral((1+v^2/c^2)^3/(1-v^2/c^2)^(3/2), v)
Test ran for 5.47s cpu, 5.53s wall
Check ran for 0.00s cpu, 0.00s wall
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/symbolic/expression.pyx", line 57, in sage.symbolic.expression
Failed example:
    integral(x^n, x)
Expected:
    x^(n + 1)/(n + 1)
Got:
    cases(((n != -1, x^(n + 1)/(n + 1)), (1, log(x))))
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.symbolic.expression"]

    assert result.failed_examples == 1
    assert result.fingerprint == "symbolic-output-variant"


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


def test_report_groups_failures_by_actionable_bucket(tmp_path):
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
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/geometry/polyhedron/backend_cdd_rdf.py", line 42, in sage.geometry.polyhedron.backend_cdd_rdf
Failed example:
    polytopes.simplex(3).Hrepresentation()
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: cddexec is not available.
    Executable 'cddexec' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.geometry.polyhedron.backend_cdd_rdf
**********************************************************************
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
    markdown = analyzer.render_markdown(report, log, None)

    assert report["actionable_buckets"][0] == {
        "category": "optional-external",
        "fingerprint": "missing-executable",
        "suggested_package": "sagelite-cddlib-runtime",
        "count": 2,
        "failed_examples": 2,
        "evidence": "standalone executable not found",
        "modules": [
            "sage.geometry.polyhedron.backend_cdd",
            "sage.geometry.polyhedron.backend_cdd_rdf",
        ],
    }
    assert "## Top Actionable Buckets" in markdown
    assert (
        "- `optional-external` / `missing-executable`: "
        "2 modules -> `sagelite-cddlib-runtime`"
    ) in markdown


def test_report_suggests_runtime_for_topcom_executable(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/geometry/triangulation/point_configuration.py", line 42, in sage.geometry.triangulation.point_configuration
Failed example:
    PointConfiguration([(0,0), (1,0), (0,1)]).triangulations()
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: topcom_points2allfinetriangs is not available.
    Executable 'points2allfinetriangs' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.geometry.triangulation.point_configuration
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    report = analyzer.build_report(results)
    result = results["sage.geometry.triangulation.point_configuration"]

    assert result.fingerprint == "missing-executable"
    assert result.suggested_package == "sagelite-topcom-runtime"
    assert (
        report["top_examples"]["optional-external"][0]["suggested_package"]
        == "sagelite-topcom-runtime"
    )


def test_report_suggests_runtime_for_alternate_executable_names(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/graphs/graph_plot.py", line 42, in sage.graphs.graph_plot
Failed example:
    g.graphplot(layout='acyclic')
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: neato is not available.
    Executable 'neato' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.graphs.graph_plot
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/plot/animate.py", line 42, in sage.plot.animate
Failed example:
    animate([]).gif()
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: magick is not available.
    Executable 'convert' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.plot.animate
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/geometry/lattice_polytope.py", line 42, in sage.geometry.lattice_polytope
Failed example:
    LatticePolytope(...).points()
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: palp_poly is not available.
    Executable 'poly.x' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.geometry.lattice_polytope
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/plot/plot.py", line 42, in sage.plot.plot
Failed example:
    plot(sin(x)).save('/tmp/a.gif')
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: magick is not available.
    Executable 'magick' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.plot.plot
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)

    assert (
        results["sage.graphs.graph_plot"].suggested_package
        == "sagelite-graphviz-runtime"
    )
    assert (
        results["sage.plot.animate"].suggested_package
        == "sagelite-imagemagick-runtime"
    )
    assert (
        results["sage.geometry.lattice_polytope"].suggested_package
        == "sagelite-palp-runtime"
    )
    assert (
        results["sage.plot.plot"].suggested_package
        == "sagelite-imagemagick-runtime"
    )


def test_report_suggests_runtime_for_feature_executable_names(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/geometry/polyhedron/base.py", line 42, in sage.geometry.polyhedron.base
Failed example:
    MixedIntegerLinearProgram(solver='csdp')
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: csdp is not available.
    Executable 'theta' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.geometry.polyhedron.base
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/rings/polynomial/groebner_fan.py", line 42, in sage.rings.polynomial.groebner_fan
Failed example:
    GroebnerFan(I).reduced_groebner_bases()
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: gfan_bases is not available.
    Executable 'gfan_bases' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.rings.polynomial.groebner_fan
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/interfaces/four_ti_2.py", line 42, in sage.interfaces.four_ti_2
Failed example:
    four_ti_2.hilbert(...)
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: 4ti2-hilbert is not available.
    Executable 'hilbert' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.interfaces.four_ti_2
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/graphs/generators/basic.py", line 42, in sage.graphs.generators.basic
Failed example:
    graphs.nauty_geng("3")
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: nauty_geng is not available.
    Executable 'geng' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.graphs.generators.basic
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/games/quantumino.py", line 42, in sage.games.quantumino
Failed example:
    solve("cu2")
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: cu2 is not available.
    Executable 'cu2' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.games.quantumino
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/geometry/triangulation/base.pyx", line 42, in sage.geometry.triangulation.base
Failed example:
    PointConfiguration([(0,0), (1,0), (0,1)]).placing_triangulation()
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: topcom_points2placingtriang is not available.
    Executable 'points2placingtriang' not found on PATH.
**********************************************************************
1 item had failures:
   1 of  10 in sage.geometry.triangulation.base
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)

    assert (
        results["sage.geometry.polyhedron.base"].suggested_package
        == "sagelite-csdp-runtime"
    )
    assert (
        results["sage.rings.polynomial.groebner_fan"].suggested_package
        == "sagelite-gfan-runtime"
    )
    assert (
        results["sage.interfaces.four_ti_2"].suggested_package
        == "sagelite-4ti2-runtime"
    )
    assert (
        results["sage.graphs.generators.basic"].suggested_package
        == "sagelite-nauty-runtime"
    )
    assert (
        results["sage.games.quantumino"].suggested_package
        == "sagelite-rubiks-runtime"
    )
    assert (
        results["sage.geometry.triangulation.base"].suggested_package
        == "sagelite-topcom-runtime"
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


def test_report_identifies_missing_required_native_extension(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/categories/coxeter_groups.py", line 42, in sage.categories.coxeter_groups
Failed example:
    CoxeterGroup(['B',3], implementation="coxeter3")
Exception raised:
    Traceback (most recent call last):
    ModuleNotFoundError: No module named 'sage.libs.coxeter3.coxeter'
    sage.features.FeatureNotPresentError: coxeter3 is not available.
    Importing get_CoxGroup failed: No module named 'sage.libs.coxeter3.coxeter'
**********************************************************************
1 item had failures:
   1 of  10 in sage.categories.coxeter_groups
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    report = analyzer.build_report(results)
    result = results["sage.categories.coxeter_groups"]

    assert result.category == "optional-external"
    assert result.fingerprint == "optional-native-lib-missing"
    assert (
        result.evidence
        == "required Sage native extension is not bundled in the installed wheel"
    )
    assert (
        result.suggested_package
        == "sagelite repaired wheel native catalog: coxeter3"
    )
    assert report["fingerprint_counts"] == {"optional-native-lib-missing": 1}


def test_report_identifies_required_native_library_load_failure(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/libs/ntl/error.pyx", line 42, in sage.libs.ntl.error
Failed example:
    import sage.all
Exception raised:
    Traceback (most recent call last):
    ImportError: libntl.so.45: cannot open shared object file: No such file or directory
**********************************************************************
1 item had failures:
   1 of  10 in sage.libs.ntl.error
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    report = analyzer.build_report(results)
    result = results["sage.libs.ntl.error"]

    assert result.category == "optional-external"
    assert result.fingerprint == "native-library-load-failure"
    assert (
        result.evidence
        == "required native shared library failed to load from the installed wheel"
    )
    assert result.suggested_package == "sagelite repaired wheel native catalog: ntl"
    assert report["fingerprint_counts"] == {"native-library-load-failure": 1}


def test_report_suggests_pypi_data_wheels_for_named_missing_databases(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/databases/cubic_hecke_db.py", line 42, in sage.databases.cubic_hecke_db
Failed example:
    CubicHeckeDataBase().version()
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: database_cubic_hecke is not available.
    No module named 'database_cubic_hecke'
**********************************************************************
1 item had failures:
   1 of   5 in sage.databases.cubic_hecke_db
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/databases/knotinfo_db.py", line 42, in sage.databases.knotinfo_db
Failed example:
    KnotInfoDataBase().version()
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: database_knotinfo is not available.
    No module named 'database_knotinfo'
**********************************************************************
1 item had failures:
   1 of   5 in sage.databases.knotinfo_db
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/matroids/database_collections.py", line 42, in sage.matroids.database_collections
Failed example:
    list(AllMatroids(2))
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: database_matroids is not available.
    No module named 'matroid_database'
**********************************************************************
1 item had failures:
   1 of   5 in sage.matroids.database_collections
**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/databases/conway.py", line 42, in sage.databases.conway
Failed example:
    ConwayPolynomials()
Exception raised:
    Traceback (most recent call last):
    sage.features.FeatureNotPresentError: conway_polynomials is not available.
    No module named 'conway_polynomials'
**********************************************************************
1 item had failures:
   1 of   5 in sage.databases.conway
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)

    assert (
        results["sage.databases.cubic_hecke_db"].suggested_package
        == "database-cubic-hecke"
    )
    assert (
        results["sage.databases.knotinfo_db"].suggested_package
        == "database-knotinfo"
    )
    assert (
        results["sage.matroids.database_collections"].suggested_package
        == "matroid-database"
    )
    assert (
        results["sage.databases.conway"].suggested_package
        == "conway-polynomials"
    )


def test_report_identifies_gap_guava_host_program_leak(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/coding/linear_code.py", line 1830, in sage.coding.linear_code.AbstractLinearCode.weight_distribution
Failed example:
    C.weight_distribution(algorithm='leon')   # optional - gap_package_guava
Exception raised:
    Traceback (most recent call last):
    FileNotFoundError: [Errno 2] No such file or directory: '/usr/share/gap/pkg/guava//bin/wtdist'
**********************************************************************
1 item had failures:
   1 of  10 in sage.coding.linear_code.AbstractLinearCode.weight_distribution
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    report = analyzer.build_report(results)
    result = results["sage.coding.linear_code"]

    assert result.category == "optional-external"
    assert result.fingerprint == "gap-guava-program-missing"
    assert result.suggested_package == "sagelite-gap-package-guava"
    assert report["fingerprint_counts"] == {"gap-guava-program-missing": 1}


def test_report_identifies_gap3_runtime_error(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/interfaces/gap3.py", line 42, in sage.interfaces.gap3
Failed example:
    f([1,2,3])                                   # optional - gap3
Exception raised:
    Traceback (most recent call last):
    RuntimeError: Gap3 produced error output
    Error, List Element: <position> must be a positive integer
**********************************************************************
1 item had failures:
   1 of  10 in sage.interfaces.gap3
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.interfaces.gap3"]

    assert result.category == "optional-external"
    assert result.fingerprint == "gap3-runtime-error"
    assert result.suggested_package == "sagelite-gap3-runtime"


def test_report_identifies_maxima_lisp_module_missing(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/interfaces/maxima.py", line 42, in sage.interfaces.maxima
Failed example:
    maxima.help("gcd")
Exception raised:
    Traceback (most recent call last):
    Module error: Don't know how to REQUIRE SB-BSD-SOCKETS.
**********************************************************************
1 item had failures:
   1 of  10 in sage.interfaces.maxima
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.interfaces.maxima"]

    assert result.category == "optional-external"
    assert result.fingerprint == "maxima-lisp-module-missing"
    assert result.suggested_package == "sagelite-maxima-runtime"


def test_report_identifies_fricas_unaryexport_runtime_error(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/interfaces/fricas_translator.py", line 42, in sage.interfaces.fricas_translator
Failed example:
    fricas("sol.basis").sage()
Exception raised:
    Traceback (most recent call last):
    RuntimeError: An error occurred when FriCAS evaluated 'sageprint(...)':
       INTERNAL-SIMPLE-UNDEFINED-FUNCTION: Cell error on |UnaryExport|: Undefined function:
**********************************************************************
1 item had failures:
   1 of  10 in sage.interfaces.fricas_translator
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.interfaces.fricas_translator"]

    assert result.category == "optional-external"
    assert result.fingerprint == "fricas-runtime-error"
    assert result.suggested_package == "sagelite-fricas-runtime"


def test_report_identifies_msolve_diagnostic_parser_failure(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/rings/polynomial/msolve.py", line 191, in sage.rings.polynomial.msolve.variety
Failed example:
    Ideal(x^2 - 1, y^2 - 1).variety(QQ, algorithm='msolve', proof=False)
Exception raised:
    Traceback (most recent call last):
    File "<string>", line 2
        Restarting with another random linear form
    SyntaxError: invalid syntax
    UnboundLocalError: cannot access local variable 'data' where it is not associated with a value
**********************************************************************
1 item had failures:
   1 of  10 in sage.rings.polynomial.msolve.variety
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.rings.polynomial.msolve"]

    assert result.category == "core-supported"
    assert result.fingerprint == "msolve-parser-diagnostic"
    assert result.suggested_package == "Sage msolve parser"


def test_report_identifies_fpylll_reduction_failure(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/schemes/projective/projective_rational_point.py", line 42, in sage.schemes.projective.projective_rational_point
Failed example:
    sieve(X, 3)
Exception raised:
    Traceback (most recent call last):
    RuntimeError: forked subprocess raised:
    fpylll.util.ReductionError: b'infinite loop in babai'
**********************************************************************
1 item had failures:
   1 of  10 in sage.schemes.projective.projective_rational_point
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.schemes.projective.projective_rational_point"]

    assert result.category == "optional-external"
    assert result.fingerprint == "fpylll-reduction-failure"
    assert result.suggested_package == "sagelite-fplll-data or fpylll portability fix"


def test_report_identifies_fpylll_strategy_path_leak(tmp_path):
    analyzer = _load_analyzer()
    log = tmp_path / "doctest.log"
    log.write_text(
        """**********************************************************************
File ".venv/lib/python3.12/site-packages/sage/modules/free_module_integer.py", line 42, in sage.modules.free_module_integer
Failed example:
    M.shortest_vector()
Exception raised:
    Traceback (most recent call last):
    FileNotFoundError: [Errno 2] No such file or directory: '/project/local/share/fplll/strategies/default.json'
**********************************************************************
1 item had failures:
   1 of  10 in sage.modules.free_module_integer
""",
        encoding="utf-8",
    )

    results = analyzer.parse_log(log)
    analyzer.build_report(results)
    result = results["sage.modules.free_module_integer"]

    assert result.category == "optional-external"
    assert result.fingerprint == "fpylll-strategy-path-leak"
    assert result.suggested_package == "sagelite-fplll-data or rebuilt fpylll runtime"
