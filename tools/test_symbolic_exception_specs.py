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
