"""
Small runtime self-test for sagelite installations.
"""

from __future__ import annotations

import sys
import traceback
from collections.abc import Callable


def _run_check(name: str, check: Callable[[], object]) -> bool:
    print(f"checking {name} ... ", end="", flush=True)
    try:
        result = check()
    except Exception:
        print("FAIL")
        traceback.print_exc()
        return False

    if result is None:
        print("ok")
    else:
        print(f"ok ({result})")
    return True


def _check_import_sage_all():
    import sage.all  # noqa: F401


def _check_factor():
    from sage.all import factor

    return factor(2026)


def _check_symbolic_integration():
    from sage.all import integrate, sin, var

    x = var("x")
    return integrate(sin(x), x)


def _check_modular_symbols():
    from sage.all import ModularSymbols

    return ModularSymbols(389, sign=1).T(2).fcp()


def _check_elliptic_curve_rank():
    from sage.all import EllipticCurve

    return EllipticCurve([1, 2, 3, 4, 5]).rank()


def _optional_runtime_summary() -> None:
    print()
    print("optional runtimes:")

    from sage.features.singular import Singular

    singular = Singular().is_present()
    print(f"  Singular executable: {'present' if singular else 'not found'}")

    try:
        from sage.interfaces.maxima_lib import maxima_lib
    except Exception:
        print("  Maxima library mode: not available")
    else:
        try:
            maxima_lib.eval("1+1")
        except Exception:
            print("  Maxima library mode: not available")
        else:
            print("  Maxima library mode: present")


def main() -> int:
    """
    Run a quick smoke test of the installed sagelite runtime.
    """
    checks = [
        ("import sage.all", _check_import_sage_all),
        ("integer factorization", _check_factor),
        ("symbolic integration", _check_symbolic_integration),
        ("modular symbols", _check_modular_symbols),
        ("elliptic curve rank", _check_elliptic_curve_rank),
    ]

    ok = True
    for name, check in checks:
        ok = _run_check(name, check) and ok

    _optional_runtime_summary()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
