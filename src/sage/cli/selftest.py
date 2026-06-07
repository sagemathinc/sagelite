"""
Small runtime self-test for sagelite installations.
"""

from __future__ import annotations

import sys
import traceback
from typing import TYPE_CHECKING

if TYPE_CHECKING:
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


def _check_eclib_mwrank():
    from sage.all import EllipticCurve
    from sage.libs.eclib.all import mwrank_EllipticCurve

    curve = EllipticCurve([0, 0, 1, -7, 6]).mwrank_curve()
    if not isinstance(curve, mwrank_EllipticCurve):
        raise TypeError(f"expected mwrank_EllipticCurve, got {type(curve)!r}")
    return curve.conductor()


def _check_brial_pbori():
    from sage.rings.polynomial.pbori.pbori import BooleanPolynomialRing

    ring = BooleanPolynomialRing(3, "x")
    x0, x1, x2 = ring.gens()
    return (x0 * x1 + x1 * x0 + x2).degree()


def _check_lrcalc():
    from sage.libs.lrcalc.lrcalc import lrcoef

    return lrcoef([2], [1], [1])


def _check_pari_data():
    try:
        import sagelite_pari_data  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.libs.pari import pari

    result = pari("polgalois(x^8 - 2)")
    return f"datadir={pari.default('datadir')}, polgalois={result}"


def _check_singular_runtime():
    try:
        import sagelite_singular_runtime  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.all import GF, ProjectiveSpace
    from sage.libs.singular.function import lib as singular_lib
    from sage.libs.singular.function import singular_function

    singular_lib("freegb.lib")
    free_algebra = singular_function("freeAlgebra")

    P = ProjectiveSpace(GF(2), 3, names="x,y,z,w")
    x, y, z, w = P.coordinate_ring().gens()
    curve = P.curve(
        [
            (x - y) * (x - z) * (x - w) * (y - z) * (y - w),
            x * y * z * w * (x + y + z + w),
        ]
    )
    try:
        curve.projection()
    except NotImplementedError:
        pass

    return free_algebra


def _check_libbraiding():
    from sage.all import BraidGroup
    from sage.libs.braiding import leftnormalform

    braid = BraidGroup(3)([1, 2, 1, -2])
    return leftnormalform(braid)


def _check_libhomfly():
    from sage.libs.homfly import homfly_polynomial_dict

    trefoil = "1 6 0 1  1 -1  2 1  0 -1  1 1  2 -1 0 1 1 1 2 1"
    return homfly_polynomial_dict(trefoil)


def _check_gapdoc_runtime():
    try:
        import sagelite_gap_runtime  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.libs.gap.libgap import libgap

    loaded = libgap.LoadPackage("gapdoc")
    if not bool(loaded):
        raise RuntimeError('GAP package "gapdoc" did not load')
    small_groups = libgap.eval("NumberSmallGroups(16)")
    transitive_groups = libgap.eval("NrTransitiveGroups(5)")
    return (
        "gapdoc loaded, "
        f"SmallGroups(16)={small_groups}, TransitiveGroups(5)={transitive_groups}"
    )


def _check_gfan_runtime():
    try:
        import sagelite_gfan  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.gfan import GfanExecutable
    from sage.interfaces.gfan import gfan

    feature = GfanExecutable().is_present()
    if not bool(feature):
        raise RuntimeError(f"gfan executable is not available: {feature.reason}")
    result = gfan("Q[x,y]{x^2-y-1,y^2-x*y-2/3}", cmd="bases")
    if "Q[x,y]" not in result:
        raise RuntimeError(f"unexpected gfan output: {result!r}")
    return "gfan executable available"


def _check_maxima_runtime():
    try:
        import sagelite_maxima  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.interfaces.maxima_lib import maxima_lib

    return maxima_lib.eval("1+1")


def _check_meataxe_runtime():
    try:
        import sagelite_meataxe  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.all import GF, matrix

    field = GF(9, "a")
    mat = matrix(field, 2, [1, 0, 0, 1], implementation="meataxe")
    return f"MTXLIB matrix over {field}: {mat.nrows()}x{mat.ncols()}"


def _check_nauty_runtime():
    try:
        import sagelite_nauty  # noqa: F401
    except ImportError:
        return "not installed"

    import subprocess

    from sage.features.nauty import Nauty

    nauty = Nauty().is_present()
    if not bool(nauty):
        raise RuntimeError(f"nauty executables are not available: {nauty.reason}")
    subprocess.run(["geng", "-q", "3"], check=True, capture_output=True, text=True)
    subprocess.run(["genposetg", "-q", "3"], check=True, capture_output=True, text=True)
    return "geng and genposetg available"


def _check_four_ti_2_runtime():
    try:
        import sagelite_four_ti_2  # noqa: F401
    except ImportError:
        return "not installed"

    import subprocess

    from sage.env import FOURTITWO_HILBERT
    from sage.features.four_ti_2 import FourTi2

    four_ti_2 = FourTi2().is_present()
    if not bool(four_ti_2):
        raise RuntimeError(f"4ti2 executables are not available: {four_ti_2.reason}")
    subprocess.run([FOURTITWO_HILBERT, "-h"], check=True, capture_output=True, text=True)
    return "4ti2 executables available"


def _check_ecm_runtime():
    try:
        import sagelite_ecm  # noqa: F401
    except ImportError:
        return "not installed"

    import subprocess

    from sage.env import SAGE_ECMBIN
    from sage.features.ecm import Ecm
    ecm_feature = Ecm().is_present()
    if not bool(ecm_feature):
        raise RuntimeError(f"ecm executable is not available: {ecm_feature.reason}")
    result = subprocess.run(
        [SAGE_ECMBIN, "-h"],
        check=True,
        capture_output=True,
        text=True,
    )
    if "Usage:" not in result.stdout:
        raise RuntimeError(f"unexpected ecm help output: {result.stdout!r}")
    return "ecm executable available"


def _check_mwrank_runtime():
    try:
        import sagelite_mwrank  # noqa: F401
    except ImportError:
        return "not installed"

    import shlex

    from sage.env import MWRANK
    from sage.interfaces.mwrank import Mwrank_class

    command = Mwrank_class("-v 0").command()
    if not command.startswith(shlex.quote(MWRANK)):
        raise RuntimeError(f"mwrank interface is not using companion runtime: {command}")
    return "mwrank executable available"


def _check_palp_runtime():
    try:
        import sagelite_palp  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.palp import Palp

    palp = Palp().is_present()
    if not bool(palp):
        raise RuntimeError(f"PALP executables are not available: {palp.reason}")
    return "PALP executables available"


def _check_rubiks_runtime():
    try:
        import sagelite_rubiks  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.rubiks import Rubiks

    rubiks = Rubiks().is_present()
    if not bool(rubiks):
        raise RuntimeError(f"Rubiks executables are not available: {rubiks.reason}")
    return "Rubiks executables available"


def _check_database_graphs():
    try:
        import sagelite_database_graphs  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.databases import DatabaseGraphs

    database = DatabaseGraphs().is_present()
    if not bool(database):
        raise RuntimeError(f"graphs database is not available: {database.reason}")
    return "graphs.db available"


def _check_cunningham_tables():
    try:
        import sagelite_cunningham_tables  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.databases.cunningham_tables import cunningham_prime_factors

    factors = cunningham_prime_factors()
    if len(factors) < 100:
        raise RuntimeError("Cunningham tables did not provide enough factors")
    return f"{len(factors)} Cunningham prime factors available"


def _check_database_cremona_mini():
    try:
        import sagelite_database_cremona_mini  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.databases import DatabaseCremona

    database = DatabaseCremona("cremona_mini").is_present()
    if not bool(database):
        raise RuntimeError(
            f"Cremona mini database is not available: {database.reason}"
        )
    return "cremona_mini.db available"


def _check_database_ellcurves():
    try:
        import sagelite_database_ellcurves  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.databases import DatabaseEllcurves

    database = DatabaseEllcurves().is_present()
    if not bool(database):
        raise RuntimeError(f"ellcurves database is not available: {database.reason}")
    return "rank files available"


def _check_database_jones_numfield():
    try:
        import sagelite_database_jones_numfield  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.databases.jones import JonesDatabase
    from sage.features.databases import DatabaseJones

    database = DatabaseJones().is_present()
    if not bool(database):
        raise RuntimeError(
            f"Jones number field database is not available: {database.reason}"
        )
    from sage.rings.integer_ring import ZZ

    fields = JonesDatabase().unramified_outside([ZZ(2)], ZZ(2))
    return f"{len(fields)} quadratic fields unramified outside 2"


def _check_database_kohel():
    try:
        import sagelite_database_kohel  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.databases.db_class_polynomials import HilbertClassPolynomialDatabase
    from sage.databases.db_modular_polynomials import ClassicalModularPolynomialDatabase

    mod_poly = ClassicalModularPolynomialDatabase()[29]
    class_poly = HilbertClassPolynomialDatabase()[-23]
    return (
        "Kohel database available: "
        f"Phi_29 degree={mod_poly.degree()}, H_-23 degree={class_poly.degree()}"
    )


def _check_database_polytopes():
    try:
        import sagelite_database_polytopes  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.databases import DatabaseReflexivePolytopes

    database = DatabaseReflexivePolytopes().is_present()
    if not bool(database):
        raise RuntimeError(
            f"reflexive polytope database is not available: {database.reason}"
        )
    return "2d/3d reflexive polytope data available"


def _check_database_mutation_class():
    try:
        import sagelite_database_mutation_class  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.combinat.cluster_algebra_quiver.mutation_type import load_data

    data = load_data(2, user=False)
    if ("G", 2) not in data:
        raise RuntimeError("cluster algebra quiver mutation class data is unavailable")
    return f"{len(data)} rank-2 mutation class entries available"


def _check_database_symbolic_data():
    try:
        import sagelite_database_symbolic_data  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.databases.symbolic_data import SymbolicData

    data = SymbolicData()
    ideal = data.get_ideal("Katsura_3")
    return f"{len(data.__dir__())} ideals available; Katsura_3 has {len(ideal.gens())} generators"


def _check_database_odlyzko_zeta():
    try:
        import sagelite_database_odlyzko_zeta  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.databases.odlyzko import zeta_zeros

    zeros = zeta_zeros()
    return f"{len(zeros)} zeta zeros available; zero 13 is {zeros[12]}"


def _check_database_stein_watkins_mini():
    try:
        import sagelite_database_stein_watkins_mini  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.databases.stein_watkins import SteinWatkinsAllData
    from sage.databases.stein_watkins import SteinWatkinsPrimeData

    first_all = next(SteinWatkinsAllData(0))
    first_all_1 = next(SteinWatkinsAllData(1))
    first_prime = next(SteinWatkinsPrimeData(0))
    return (
        "first conductors: "
        f"all={first_all.conductor}, all1={first_all_1.conductor}, "
        f"prime={first_prime.conductor}"
    )


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
        ("eclib mwrank library", _check_eclib_mwrank),
        ("brial pbori library", _check_brial_pbori),
        ("lrcalc python library", _check_lrcalc),
        ("PARI data runtime", _check_pari_data),
        ("Singular library runtime", _check_singular_runtime),
        ("libbraiding library", _check_libbraiding),
        ("libhomfly library", _check_libhomfly),
        ("GAPDoc package runtime", _check_gapdoc_runtime),
        ("gfan executable runtime", _check_gfan_runtime),
        ("Maxima library runtime", _check_maxima_runtime),
        ("MeatAxe table runtime", _check_meataxe_runtime),
        ("nauty executable runtime", _check_nauty_runtime),
        ("4ti2 executable runtime", _check_four_ti_2_runtime),
        ("ECM executable runtime", _check_ecm_runtime),
        ("mwrank executable runtime", _check_mwrank_runtime),
        ("PALP executable runtime", _check_palp_runtime),
        ("Rubiks executable runtime", _check_rubiks_runtime),
        ("Cunningham tables runtime", _check_cunningham_tables),
        ("graphs database runtime", _check_database_graphs),
        ("Cremona mini database runtime", _check_database_cremona_mini),
        ("ellcurves database runtime", _check_database_ellcurves),
        ("Jones number field database runtime", _check_database_jones_numfield),
        ("Kohel polynomial database runtime", _check_database_kohel),
        ("reflexive polytopes database runtime", _check_database_polytopes),
        ("mutation class database runtime", _check_database_mutation_class),
        ("SymbolicData database runtime", _check_database_symbolic_data),
        ("Odlyzko zeta database runtime", _check_database_odlyzko_zeta),
        ("Stein-Watkins mini database runtime", _check_database_stein_watkins_mini),
    ]

    ok = True
    for name, check in checks:
        ok = _run_check(name, check) and ok

    _optional_runtime_summary()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
