from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_symbol_domain_sync_propagates_python_exceptions():
    source = (ROOT / "src" / "sage" / "symbolic" / "expression.pyx").read_text(
        encoding="utf-8"
    )

    assert (
        "cdef void send_sage_domain_to_maxima(Expression v, object domain) except *:"
        in source
    )


def test_gap_stress_tests_do_not_expose_libgap_during_collection():
    source = (ROOT / "src" / "sage" / "libs" / "gap" / "gap_test.py").read_text(
        encoding="utf-8"
    )

    assert "from sage.libs.gap.libgap import libgap" not in source.split(
        "def _libgap():", 1
    )[0]
