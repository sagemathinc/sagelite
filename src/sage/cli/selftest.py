"""
Small runtime self-test for sagelite installations.
"""

from __future__ import annotations

import argparse
import ctypes
import importlib
import importlib.metadata as importlib_metadata
import importlib.util
import inspect
import os
import re
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path
from typing import TYPE_CHECKING

from packaging.requirements import Requirement
from packaging.version import Version

if TYPE_CHECKING:
    from collections.abc import Callable


def _run_check(name: str, check: Callable[[], object]) -> bool:
    print(f"checking {name} ... ", end="", flush=True)
    try:
        result = check()
    except (KeyboardInterrupt, SystemExit):
        raise
    except BaseException:
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


def _check_installed_requirements(distribution_name: str = "sagelite"):
    distribution = importlib_metadata.distribution(distribution_name)
    issues = []

    for requirement_text in distribution.requires or []:
        requirement = Requirement(requirement_text)
        if requirement.marker is not None and not requirement.marker.evaluate():
            continue

        try:
            installed_version = Version(importlib_metadata.version(requirement.name))
        except importlib_metadata.PackageNotFoundError:
            issues.append(f"{requirement.name} is not installed")
            continue

        if requirement.specifier and not requirement.specifier.contains(
            installed_version, prereleases=True
        ):
            issues.append(
                f"{requirement.name} {installed_version} does not satisfy "
                f"{requirement.specifier}"
            )

    if issues:
        raise RuntimeError(
            f"{distribution_name} has installed requirement version conflicts:\n  "
            + "\n  ".join(issues)
        )

    return "installed requirement versions satisfy metadata"


def _check_single_pari_runtime():
    """
    Reject installed wheels that can load two different PARI runtimes.

    A prebuilt ``cypari2`` wheel can carry its own ``cypari2.libs/libpari*``.
    Loading that beside the PARI library used by Sage extension modules has
    caused installed-wheel doctests to segfault.  Release builds vendor a
    source-built cypari2 package that shares sagelite's repaired PARI runtime.
    """
    spec = importlib.util.find_spec("cypari2")
    if spec is None or spec.origin is None:
        return "cypari2 not importable"

    package_dir = Path(spec.origin).parent
    private_lib_dir = package_dir.parent / "cypari2.libs"
    private_pari = sorted(private_lib_dir.glob("libpari*"))
    if private_pari:
        libraries = ", ".join(path.name for path in private_pari)
        raise RuntimeError(
            "cypari2 is installed with a private PARI runtime "
            f"({libraries}). Rebuild the sagelite wheel with source-built "
            "cypari2 so Sage and cypari2 share the same repaired libpari."
        )

    return "cypari2 does not carry a private PARI runtime"


_PARI_RUNTIME_PROBE = """
from sage.cli.selftest import _check_loaded_pari_runtime

_check_loaded_pari_runtime()

from sage.arith.misc import primitive_root

print(primitive_root(389, check=False))
"""


def _loaded_libpari_paths() -> list[Path]:
    """
    Return PARI shared libraries currently mapped in this process.
    """
    maps = Path("/proc/self/maps")
    if not maps.is_file():
        return []

    paths = []
    seen = set()
    for line in maps.read_text(encoding="utf-8", errors="replace").splitlines():
        if "libpari" not in line:
            continue
        path_text = line.rsplit(maxsplit=1)[-1]
        path = Path(path_text)
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        paths.append(path)
    return paths


def _check_loaded_pari_runtime():
    """
    Reject installed wheels that have already loaded multiple PARI runtimes.

    The packaging check catches the common prebuilt ``cypari2`` wheel case
    before imports.  This runtime check catches lower-level repair mistakes,
    such as Sage extensions resolving a system PARI while cypari2 resolves a
    bundled one.
    """
    importlib.import_module("sage.libs.pari.convert_gmp")
    importlib.import_module("cypari2.pari_instance")

    loaded_libpari = sorted({path.resolve() for path in _loaded_libpari_paths()})
    if len(loaded_libpari) > 1:
        loaded = ", ".join(os.fspath(path) for path in loaded_libpari)
        raise RuntimeError(
            "multiple PARI runtime libraries are loaded in this process. "
            f"Loaded libpari: {loaded}. Rebuild the sagelite wheel so Sage "
            "extension modules and cypari2 share the same repaired libpari."
        )

    if loaded_libpari:
        return f"loaded PARI runtime: {loaded_libpari[0].name}"
    return "no loaded PARI shared library found"


def _check_pari_runtime_roundtrip():
    """
    Exercise the Sage Integer to cypari2 conversion in a subprocess.

    Mixed PARI runtimes can segfault during this conversion.  Keep the probe
    isolated so ``sagelite-selftest`` reports the packaging problem instead of
    dying later in a broader smoke test such as modular symbols.
    """
    return _run_subprocess_probe(_PARI_RUNTIME_PROBE, "PARI runtime probe")


_FALLBACK_REQUIRED_NATIVE_IMPORT_MODULES = [
    "sage.graphs.bliss",
    "sage.graphs.cliquer",
    "sage.graphs.graph_decompositions.rankwidth",
    "sage.graphs.graph_decompositions.tdlib",
    "sage.graphs.mcqd",
    "sage.graphs.planarity",
    "sage.libs.braiding",
    "sage.libs.coxeter3.coxeter",
    "sage.libs.eclib.mwrank",
    "sage.libs.eclib.newforms",
    "sage.libs.homfly",
    "sage.libs.meataxe",
    "sage.libs.ntl.error",
    "sage.libs.sirocco",
    "sage.libs.symmetrica.symmetrica",
    "sage.numerical.backends.glpk_backend",
    "sage.numerical.backends.glpk_exact_backend",
    "sage.numerical.backends.glpk_graph_backend",
    "sage.rings.polynomial.pbori.pbori",
]

_FALLBACK_COLD_IMPORT_INITIALIZATION_SENSITIVE_MODULES = {
    "sage.graphs.graph_decompositions.tdlib",
    "sage.libs.eclib.newforms",
}

_FALLBACK_REQUIRED_NATIVE_SMOKE_IMPORT_MODULES = [
    module_name
    for module_name in _FALLBACK_REQUIRED_NATIVE_IMPORT_MODULES
    if module_name not in _FALLBACK_COLD_IMPORT_INITIALIZATION_SENSITIVE_MODULES
]


def _required_native_import_modules() -> list[str]:
    """
    Return the cold-importable native smoke surface for Linux sagelite wheels.

    Source checkouts keep the authoritative release catalog in ``tools/``.
    Installed wheels do not ship that helper, so keep a synchronized fallback
    list in this self-test.
    """
    for parent in Path(__file__).resolve().parents:
        catalog_path = parent / "tools" / "sagelite_native_wheel_catalog.py"
        if not catalog_path.is_file():
            continue

        spec = importlib.util.spec_from_file_location(
            "sagelite_native_wheel_catalog", catalog_path
        )
        if spec is None or spec.loader is None:
            break
        catalog_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(catalog_module)
        catalog = catalog_module.catalog()
        return list(
            catalog.get(
                "required_native_smoke_import_modules",
                catalog["required_native_import_modules"],
            )
        )

    return list(_FALLBACK_REQUIRED_NATIVE_SMOKE_IMPORT_MODULES)


def _check_required_native_imports():
    failures = []
    modules = _required_native_import_modules()
    for module_name in modules:
        try:
            importlib.import_module(module_name)
        except Exception as exc:  # noqa: BLE001 - report all broken imports together
            failures.append(f"{module_name}: {type(exc).__name__}: {exc}")

    if failures:
        raise RuntimeError(
            "required sagelite native modules failed to import:\n  "
            + "\n  ".join(failures)
        )

    return f"{len(modules)} required native modules import"


_SOURCE_INSPECTION_MODULES = [
    "sage.rings.integer",
    "sage.rings.rational",
    "sage.libs.braiding",
    "sage.rings.polynomial.pbori.pbori",
]
_ABSOLUTE_PATH_RE = re.compile(r"(?<![A-Za-z0-9_.-])/[^\s:'\"`]+")


def _source_path_is_portable(path_text: str | None, allowed_roots: list[Path]) -> bool:
    if not path_text:
        return True

    path_candidates = []
    path = Path(path_text)
    if path.is_absolute():
        path_candidates.append(path)
    else:
        path_candidates.extend(
            Path(match.group(0).rstrip(".,;)]}"))
            for match in _ABSOLUTE_PATH_RE.finditer(path_text)
        )
    if not path_candidates:
        return True

    for candidate in path_candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            resolved = candidate.absolute()
        if not any(
            resolved == root or root in resolved.parents for root in allowed_roots
        ):
            return False
    return True


def _check_source_inspection_paths():
    """
    Reject wheels whose compiled modules expose build-tree source paths.

    Cython metadata can preserve absolute ``.pyx`` paths.  Those paths confused
    installed doctests that exercise Sage source inspection, so repaired wheels
    should report package-relative paths or files under the installed prefix.
    """
    from sage.misc import sageinspect

    allowed_roots = [Path(sys.prefix).resolve(), Path(sys.exec_prefix).resolve()]
    leaks = []

    for module_name in _SOURCE_INSPECTION_MODULES:
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue

        values = []
        try:
            values.append(("inspect.getsourcefile", inspect.getsourcefile(module)))
        except Exception as exc:  # noqa: BLE001 - report source metadata failures
            values.append(
                ("inspect.getsourcefile error", f"{type(exc).__name__}: {exc}")
            )
        try:
            values.append(
                ("sage_getfile_relative", sageinspect.sage_getfile_relative(module))
            )
        except Exception as exc:  # noqa: BLE001 - error messages can contain leaks
            values.append(
                ("sage_getfile_relative error", f"{type(exc).__name__}: {exc}")
            )

        for label, path_text in values:
            if not _source_path_is_portable(path_text, allowed_roots):
                leaks.append(f"{module_name} {label}: {path_text}")

    if leaks:
        raise RuntimeError(
            "compiled Sage modules expose build-tree source paths:\n  "
            + "\n  ".join(leaks)
        )

    return f"{len(_SOURCE_INSPECTION_MODULES)} compiled module source paths portable"


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
    try:
        from sage.rings.polynomial.pbori.pbori import BooleanPolynomialRing
    except ImportError:
        return "not installed"

    ring = BooleanPolynomialRing(3, "x")
    x0, x1, x2 = ring.gens()
    return (x0 * x1 + x1 * x0 + x2).degree()


def _check_lrcalc():
    from sage.libs.lrcalc.lrcalc import lrcoef

    return lrcoef([2], [1], [1])


def _check_companion_feature(
    module_name: str,
    feature_factory: Callable[[], object],
    description: str,
):
    try:
        importlib.import_module(module_name)
    except ImportError:
        return "not installed"

    feature = feature_factory()
    result = feature.is_present()
    if not bool(result):
        raise RuntimeError(f"{description} is not available: {result.reason}")
    return f"{description} available"


def _same_existing_path(left, right) -> bool:
    try:
        return os.path.samefile(left, right)
    except (OSError, TypeError, ValueError):
        return False


GAP_PACKAGE_COMPANIONS = [
    ("atlasrep", "sagelite_gap_package_atlasrep", "AtlasRep"),
    ("ctbllib", "sagelite_gap_package_ctbllib", "CTblLib"),
    ("design", "sagelite_gap_package_design", "Design"),
    ("grape", "sagelite_gap_package_grape", "GRAPE"),
    ("guava", "sagelite_gap_package_guava", "GUAVA"),
    ("hap", "sagelite_gap_package_hap", "HAP"),
    ("polenta", "sagelite_gap_package_polenta", "Polenta"),
    ("polycyclic", "sagelite_gap_package_polycyclic", "Polycyclic"),
    ("primgrp", "sagelite_gap_package_primgrp", "PrimGrp"),
    ("qpa", "sagelite_gap_package_qpa", "QPA"),
    ("quagroup", "sagelite_gap_package_quagroup", "QuaGroup"),
    ("repsn", "sagelite_gap_package_repsn", "Repsn"),
    ("smallgrp", "sagelite_gap_package_smallgrp", "SmallGrp"),
    ("tomlib", "sagelite_gap_package_tomlib", "TomLib"),
    ("transgrp", "sagelite_gap_package_transgrp", "TransGrp"),
]


_GAP_GUAVA_RUNTIME_PROBE = """
import os
from pathlib import Path

from sage.coding.linear_code import LinearCode
from sage.libs.gap.libgap import libgap
from sage.matrix.constructor import matrix
from sage.rings.finite_rings.finite_field_constructor import GF

loaded = libgap.LoadPackage("guava")
program_dirs = libgap.DirectoriesPackagePrograms("guava")
program_dir_paths = [Path(str(path).strip('"')) for path in program_dirs]
wtdist_paths = [path / "wtdist" for path in program_dir_paths]
wtdist_executable = any(
    path.is_file() and os.access(path, os.X_OK) for path in wtdist_paths
)
code = LinearCode(matrix(GF(2), [[1, 0, 1], [0, 1, 1]]))
weight_distribution = code.weight_distribution(algorithm="leon")
if not loaded or not wtdist_executable or weight_distribution != [1, 0, 3, 0]:
    raise RuntimeError(
        "GUAVA Leon runtime is not usable: "
        f"loaded={bool(loaded)!r}, "
        f"wtdist_paths={[str(path) for path in wtdist_paths]!r}, "
        f"weight_distribution={weight_distribution!r}"
    )
print("GUAVA Leon weight distribution available")
"""


def _check_gap_package_runtime(
    package: str,
    module_name: str,
    display_name: str,
):
    try:
        importlib.import_module(module_name)
    except ImportError:
        return "not installed"

    from sage.features.gap import GapPackage
    from sage.env import GAP_ROOT_PATHS

    try:
        runtime = importlib.import_module(f"{module_name}.runtime")
    except ImportError:
        companion_roots = set()
    else:
        root_paths = getattr(runtime, "gap_root_paths", lambda: "")()
        companion_roots = {path for path in root_paths.split(";") if path}

    feature = GapPackage(package, spkg=f"gap_package_{package}").is_present()
    if not bool(feature):
        active_roots = {path for path in GAP_ROOT_PATHS.split(";") if path}
        if companion_roots and not companion_roots.intersection(active_roots):
            return (
                f"GAP package {display_name} installed but not active with "
                "the current GAP runtime"
            )
        raise RuntimeError(
            f"GAP package {display_name} is not available: {feature.reason}"
        )
    return f"GAP package {display_name} available"


def _check_gap_guava_leon_runtime():
    package_status = _check_gap_package_runtime(
        "guava", "sagelite_gap_package_guava", "GUAVA"
    )
    if package_status == "not installed":
        return package_status
    return _run_subprocess_probe(_GAP_GUAVA_RUNTIME_PROBE, "GAP GUAVA Leon probe")


def _check_cddlib_runtime():
    try:
        import sagelite_cddlib  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.cddlib import CddExecutable

    executables = {}
    for program in ("cddexec", "cddexec_gmp"):
        feature = CddExecutable(program)
        presence = feature.is_present()
        if not bool(presence):
            raise RuntimeError(
                f"cddlib executable {program!r} is not available: {presence.reason}"
            )
        executables[program] = feature.absolute_filename()
    return (
        f"cddexec={executables['cddexec']}, "
        f"cddexec_gmp={executables['cddexec_gmp']}"
    )


def _check_lie_runtime():
    try:
        import sagelite_lie  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.env import SAGE_LIE_COMMAND
    from sage.interfaces.lie import lie

    if lie.command() != SAGE_LIE_COMMAND:
        raise RuntimeError(
            f"LiE interface is not using companion runtime: {lie.command()}"
        )
    if lie.eval("19+68") != "87":
        raise RuntimeError("LiE companion runtime did not evaluate a basic command")
    return "LiE executable and info directory available"


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
    try:
        from sage.all import BraidGroup
        from sage.libs.braiding import leftnormalform
    except ImportError:
        return "not installed"

    braid = BraidGroup(3)([1, 2, 1, -2])
    return leftnormalform(braid)


def _check_libhomfly():
    from sage.libs.homfly import homfly_polynomial_dict

    trefoil = "1 6 0 1  1 -1  2 1  0 -1  1 1  2 -1 0 1 1 1 2 1"
    return homfly_polynomial_dict(trefoil)


def _check_bliss_library():
    from sage.all import graphs

    graph = graphs.PetersenGraph()
    try:
        canonical = graph.canonical_label(algorithm="bliss")
    except ImportError:
        return "not installed"
    return f"canonical Petersen graph has {canonical.num_verts()} vertices"


def _check_coxeter3_library():
    from sage.combinat.root_system.coxeter_group import CoxeterGroup

    try:
        group = CoxeterGroup(["A", 3], implementation="coxeter3")
    except ImportError:
        return "not installed"
    except Exception as error:
        from sage.features import FeatureNotPresentError

        if isinstance(error, FeatureNotPresentError):
            return "not installed"
        raise
    return f"A3 long element length {group.long_element().length()}"


def _check_mcqd_library():
    from sage.all import graphs

    graph = graphs.PetersenGraph()
    try:
        cover_size = graph.vertex_cover(algorithm="mcqd", value_only=True)
    except ImportError:
        return "not installed"
    except Exception as error:
        from sage.features import FeatureNotPresentError

        if isinstance(error, FeatureNotPresentError):
            return "not installed"
        raise
    return f"Petersen vertex cover size {cover_size}"


def _check_tdlib_library():
    from sage.all import graphs

    graph = graphs.PetersenGraph()
    try:
        treewidth = graph.treewidth(algorithm="tdlib")
    except ImportError:
        return "not installed"
    except Exception as error:
        from sage.features import FeatureNotPresentError

        if isinstance(error, FeatureNotPresentError):
            return "not installed"
        raise
    return f"Petersen treewidth {treewidth}"


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


def _check_ecl_runtime():
    try:
        from sagelite_ecl import runtime
    except ImportError:
        return "not installed"

    from sage.env import ECL_CONFIG

    command = Path(runtime.ecl_config_command())
    if not command.is_file() or not os.access(command, os.X_OK):
        raise RuntimeError(f"ecl-config companion command is not executable: {command}")
    if not _same_existing_path(command, ECL_CONFIG):
        return f"Sage is using non-companion ECL runtime: {ECL_CONFIG}"

    ecldir = Path(runtime.ecl_dir())
    if not ecldir.is_dir():
        raise RuntimeError(f"ECL support directory is not available: {ecldir}")
    return "ECL command and support directory available"


_GAP3_RUNTIME_PROBE = r"""
from sage.interfaces.gap3 import gap3
from sage.misc.latex import latex

normal_output, error_output = gap3._execute_line("2+3;")
if error_output or "5" not in str(normal_output):
    raise RuntimeError(
        "GAP3 _execute_line returned unexpected output: "
        f"normal={normal_output!r}, error={error_output!r}"
    )

help_text = str(gap3.help("help", pager=False))
if "GAP help system" not in help_text and "help system" not in help_text:
    raise RuntimeError("GAP3 help output is not available")

values = gap3([1, 2, 3])
if str(values[1]) != "1" or str(values[2]) != "2":
    raise RuntimeError(f"GAP3 list indexing is not 1-based: {values!r}")

matrix = gap3([[1, 2], [3, 4]])
matrix_latex = latex(matrix)
if r"\begin{array}" not in matrix_latex or "3&4" not in matrix_latex:
    raise RuntimeError(f"GAP3 LaTeX output is not available: {matrix_latex!r}")

print("GAP3 prompt, help, indexing, and LaTeX available")
"""


def _check_gap3_runtime():
    from sage.features.gap3 import Gap3

    feature_status = _check_companion_feature(
        "sagelite_gap3", Gap3, "GAP3 executable runtime"
    )
    if feature_status == "not installed":
        return feature_status
    return _run_subprocess_probe(_GAP3_RUNTIME_PROBE, "GAP3 runtime probe")


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


def _check_csdp_runtime():
    from sage.features.csdp import CSDP

    return _check_companion_feature(
        "sagelite_csdp", CSDP, "CSDP executable runtime"
    )


def _check_plantri_runtime():
    from sage.features.graph_generators import Plantri

    return _check_companion_feature(
        "sagelite_plantri", Plantri, "plantri graph generator runtime"
    )


def _check_buckygen_runtime():
    from sage.features.graph_generators import Buckygen

    return _check_companion_feature(
        "sagelite_buckygen", Buckygen, "buckygen graph generator runtime"
    )


def _check_benzene_runtime():
    from sage.features.graph_generators import Benzene

    return _check_companion_feature(
        "sagelite_benzene", Benzene, "benzene graph generator runtime"
    )


_FRICAS_RUNTIME_PROBE = """
from sage.all import PolynomialRing, QQ
from sage.interfaces.fricas import fricas
from sage.interfaces.fricas_translator import (
    LazyParent,
    SEXEvaluator,
    SEXParser,
    SEXPorter,
)


def translated_sage(element):
    process = element._check_valid()
    domain = SEXParser(
        process.get_string(f"sageprint(dom({element._name})::Any)")
    ).parse()
    export = SEXPorter(domain).export_call()
    exported = process.get_string(f"sageprint({export}({element._name}))")
    return SEXEvaluator(SEXParser(exported).parse(), LazyParent(domain)).eval()

R = PolynomialRing(QQ, "x")
x = R.gen()
factorization = fricas(x**2 - 1).factor().sage()
if factorization.prod() != x**2 - 1:
    raise RuntimeError(f"unexpected FriCAS factorization conversion: {factorization!r}")

fricas("sol := solve([x^2 - 1], [x])")
basis = fricas("sol.basis").sage()
if len(basis) != 1:
    raise RuntimeError(f"unexpected FriCAS solution basis conversion: {basis!r}")

S = PolynomialRing(QQ, ("x", "y", "z"))
sx, sy, sz = S.gens()
polynomial = translated_sage(fricas("x^2*y - 3*z + 1"))
if polynomial != sx**2 * sy - 3 * sz + 1:
    raise RuntimeError(f"unexpected FriCAS translator polynomial: {polynomial!r}")
translated_factorization = translated_sage(fricas("-48").factor())
if translated_factorization.prod() != -48:
    raise RuntimeError(
        "unexpected FriCAS translator factorization: "
        f"{translated_factorization!r}"
    )

print("FriCAS conversions available")
"""


def _check_fricas_runtime():
    from sage.features.fricas import FriCAS

    feature_status = _check_companion_feature(
        "sagelite_fricas", FriCAS, "FriCAS executable runtime"
    )
    if feature_status == "not installed":
        return feature_status
    return _run_subprocess_probe(_FRICAS_RUNTIME_PROBE, "FriCAS runtime probe")


def _check_frobby_runtime():
    from sage.features.frobby import Frobby

    return _check_companion_feature(
        "sagelite_frobby", Frobby, "Frobby executable runtime"
    )


def _check_giac_runtime():
    from sage.features.giac import Giac

    return _check_companion_feature(
        "sagelite_giac", Giac, "Giac executable runtime"
    )


def _check_graphviz_runtime():
    from sage.features.graphviz import Graphviz

    return _check_companion_feature(
        "sagelite_graphviz", Graphviz, "Graphviz executable runtime"
    )


def _check_glucose_runtime():
    try:
        importlib.import_module("sagelite_glucose")
    except ImportError:
        return "not installed"

    from sage.features.sat import Glucose

    for program in ("glucose", "glucose-syrup"):
        presence = Glucose(program).is_present()
        if not bool(presence):
            raise RuntimeError(
                f"Glucose executable {program!r} is not available: {presence.reason}"
            )
    return "Glucose executable runtime available"


def _check_kissat_runtime():
    from sage.features.sat import Kissat

    return _check_companion_feature(
        "sagelite_kissat", Kissat, "Kissat executable runtime"
    )


def _check_imagemagick_runtime():
    from sage.features.imagemagick import ImageMagick

    return _check_companion_feature(
        "sagelite_imagemagick", ImageMagick, "ImageMagick executable runtime"
    )


def _check_dvipng_runtime():
    from sage.features.dvipng import dvipng

    return _check_companion_feature(
        "sagelite_dvipng", dvipng, "dvipng executable runtime"
    )


def _check_pdf2svg_runtime():
    from sage.features.pdf2svg import pdf2svg

    return _check_companion_feature(
        "sagelite_pdf2svg", pdf2svg, "pdf2svg executable runtime"
    )


def _check_poppler_runtime():
    from sage.features.poppler import pdftocairo

    return _check_companion_feature(
        "sagelite_poppler", pdftocairo, "Poppler pdftocairo executable runtime"
    )


def _check_info_runtime():
    from sage.features.info import Info

    return _check_companion_feature(
        "sagelite_info", Info, "GNU Info executable runtime"
    )


def _check_latte_runtime():
    from sage.features.latte import Latte

    return _check_companion_feature(
        "sagelite_latte", Latte, "LattE executable runtime"
    )


def _check_lcalc_runtime():
    from sage.features.lcalc import Lcalc

    return _check_companion_feature(
        "sagelite_lcalc", Lcalc, "lcalc executable runtime"
    )


def _check_lrslib_runtime():
    from sage.features.lrs import Lrslib

    return _check_companion_feature(
        "sagelite_lrslib", Lrslib, "lrslib executable runtime"
    )


def _check_sympow_runtime():
    try:
        from sagelite_sympow import runtime
    except ImportError:
        return "not installed"

    from sage.env import SYMPOW

    command = Path(runtime.sympow_command())
    if not command.is_file() or not os.access(command, os.X_OK):
        raise RuntimeError(f"sympow companion command is not executable: {command}")
    if not _same_existing_path(command, SYMPOW):
        return f"Sage is using non-companion sympow runtime: {SYMPOW}"
    return "sympow executable runtime available"


_MAXIMA_RUNTIME_PROBE = """
from sage.cli.selftest import _check_loaded_ecl_matches_maxima_runtime

_check_loaded_ecl_matches_maxima_runtime()

from sage.all import RR, cos, sin, var
from sage.interfaces.maxima_lib import maxima, maxima_lib

value = maxima_lib.eval("1+1")
if "-- Function: gcd" not in str(maxima.help("gcd")):
    raise RuntimeError("Maxima help is not available")
if "a[n]:=n*a[n-1]" not in str(maxima.example("arrays")):
    raise RuntimeError("Maxima examples are not available")
x = var("x", domain=RR)
if x.conjugate() != x:
    raise RuntimeError("Maxima-backed symbolic assumptions are not available")
if maxima_lib.sr_integral(sin(x), x)._sage_() != -cos(x):
    raise RuntimeError("Maxima library-mode integration is not available")
print(value)
"""


def _loaded_libecl_paths() -> list[Path]:
    """
    Return ECL shared libraries currently mapped in this process.
    """
    maps = Path("/proc/self/maps")
    if not maps.is_file():
        return []

    paths = []
    seen = set()
    for line in maps.read_text(encoding="utf-8", errors="replace").splitlines():
        if "libecl" not in line:
            continue
        path_text = line.rsplit(maxsplit=1)[-1]
        path = Path(path_text)
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        paths.append(path)
    return paths


def _library_exports_symbol(path: Path, symbol: str) -> bool:
    """
    Return whether ``path`` exports ``symbol`` through the dynamic loader.
    """
    try:
        library = ctypes.CDLL(os.fspath(path))
    except OSError:
        return False
    return hasattr(library, symbol)


def _check_loaded_ecl_matches_maxima_runtime():
    """
    Detect Maxima companion images that cannot load against Sage's ECL runtime.

    Installed-wheel processes cannot repair extension-module library choices by
    changing ``LD_LIBRARY_PATH`` after Python has started.  If ``sage.libs.ecl``
    has already loaded an ECL library that lacks symbols required by the
    companion ``maxima.fas``, fail before the broader symbolic probe reports a
    less direct Maxima import error.
    """
    try:
        runtime = importlib.import_module("sagelite_maxima.runtime")
    except ImportError:
        return "not installed"

    maxima_fas = Path(runtime.maxima_fas())
    try:
        from sage.env import MAXIMA_FAS

        if MAXIMA_FAS and not os.path.samefile(MAXIMA_FAS, maxima_fas):
            return "Sage is using a non-companion Maxima image"
    except OSError:
        pass

    importlib.import_module("sage.libs.ecl")

    try:
        requires_fe_stack = b"FEstack_advance" in maxima_fas.read_bytes()
    except OSError:
        return "maxima.fas not readable"
    if not requires_fe_stack:
        return "maxima.fas does not require FEstack_advance"

    loaded_libecl = _loaded_libecl_paths()
    if any(_library_exports_symbol(path, "FEstack_advance") for path in loaded_libecl):
        return "loaded ECL exports Maxima image symbols"

    loaded = ", ".join(os.fspath(path) for path in loaded_libecl) or "none"
    raise RuntimeError(
        "Maxima companion maxima.fas requires FEstack_advance, but the loaded "
        f"ECL runtime does not export it. Loaded libecl: {loaded}. Rebuild "
        "sagelite and sagelite-maxima-runtime from matching ECL inputs, or "
        "build the Maxima companion with SAGELITE_MAXIMA_ECL_LIBRARY pointing "
        "at the ECL shared library used by the sagelite wheel."
    )


def _tail(file, limit: int = 4096) -> str:
    file.seek(0, 2)
    size = file.tell()
    file.seek(max(0, size - limit))
    return file.read().decode("utf-8", "replace")


def _run_subprocess_probe(
    script: str, description: str = "runtime probe", timeout: int = 30
) -> str:
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        process = subprocess.Popen(
            [sys.executable, "-c", script],
            stdout=stdout,
            stderr=stderr,
        )
        try:
            returncode = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired as err:
            process.kill()
            process.wait()
            raise RuntimeError(
                f"{description} timed out.\n"
                f"Last stdout:\n{_tail(stdout)}\n"
                f"Last stderr:\n{_tail(stderr)}"
            ) from err

        if returncode != 0:
            raise RuntimeError(
                f"{description} exited with status {returncode}.\n"
                f"Last stdout:\n{_tail(stdout)}\n"
                f"Last stderr:\n{_tail(stderr)}"
            )

        output = _tail(stdout).strip().splitlines()
        return output[-1] if output else "ok"


def _check_maxima_runtime():
    try:
        import sagelite_maxima  # noqa: F401
    except ImportError:
        return "not installed"

    return _run_subprocess_probe(_MAXIMA_RUNTIME_PROBE, "Maxima runtime probe")


def _check_kenzo_runtime():
    try:
        from sagelite_kenzo import runtime
    except ImportError:
        return "not installed"

    from sage.env import KENZO_FAS

    companion_fas = Path(runtime.kenzo_fas())
    if not companion_fas.is_file():
        raise RuntimeError(f"Kenzo companion FAS is not available: {companion_fas}")
    if not KENZO_FAS:
        return "Kenzo companion runtime is not active"
    if not _same_existing_path(companion_fas, KENZO_FAS):
        return f"Sage is using non-companion Kenzo runtime: {KENZO_FAS}"

    from sage.features.kenzo import Kenzo
    return _check_companion_feature(
        "sagelite_kenzo", Kenzo, "Kenzo ECL runtime"
    )


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

    from sage.features.nauty import NautyExecutable

    commands = []
    for program in ("geng", "genposetg"):
        feature = NautyExecutable(program)
        presence = feature.is_present()
        if not bool(presence):
            raise RuntimeError(
                f"nauty executable {program!r} is not available: {presence.reason}"
            )
        commands.append(feature.absolute_filename())
    geng, genposetg = commands
    subprocess.run([geng, "-q", "3"], check=True, capture_output=True, text=True)
    subprocess.run([genposetg, "-q", "3"], check=True, capture_output=True, text=True)
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


def _check_flatter_runtime():
    try:
        import sagelite_flatter  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.flatter import flatter

    flatter_feature = flatter().is_present()
    if not bool(flatter_feature):
        raise RuntimeError(
            f"flatter executable is not available: {flatter_feature.reason}"
        )
    return "flatter executable available"


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


def _check_msolve_runtime():
    from sage.features.msolve import msolve

    return _check_companion_feature(
        "sagelite_msolve", msolve, "msolve executable runtime"
    )


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


def _check_planarity_runtime():
    try:
        importlib.import_module("sagelite_planarity")
    except ImportError:
        return "not installed"

    from sage.features.planarity import Planarity

    feature = Planarity().is_present()
    if not bool(feature):
        raise RuntimeError(f"planarity executable runtime is not available: {feature.reason}")
    return "planarity executable runtime available"


def _check_qepcad_runtime():
    from sage.features.qepcad import Qepcad

    return _check_companion_feature(
        "sagelite_qepcad", Qepcad, "QEPCAD executable runtime"
    )


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


def _check_tides_runtime():
    from sage.features.tides import Tides

    return _check_companion_feature(
        "sagelite_tides", Tides, "TIDES compile-time runtime"
    )


def _check_tachyon_runtime():
    try:
        from sagelite_tachyon import runtime
    except ImportError:
        return "not installed"

    from sage.env import TACHYON

    command = Path(runtime.executable_path())
    if not command.is_file() or not os.access(command, os.X_OK):
        raise RuntimeError(f"tachyon companion command is not executable: {command}")
    if _same_existing_path(command, TACHYON):
        return "Tachyon executable runtime available"

    result = subprocess.run(
        [TACHYON],
        capture_output=True,
        text=True,
        timeout=10,
    )
    output = result.stdout + result.stderr
    if "tachyon" not in output.lower() or "modelfile" not in output.lower():
        raise RuntimeError(f"Tachyon command is not usable: {TACHYON}")
    return f"Sage is using non-companion Tachyon runtime: {TACHYON}"


def _check_sirocco_runtime():
    try:
        from sagelite_sirocco import runtime
    except ImportError:
        return "not installed"

    include_dir = Path(runtime.include_dir())
    library_dir = Path(runtime.library_dir())
    header = include_dir / "sirocco.h"
    libraries = sorted(
        path
        for path in library_dir.glob("libsirocco*")
        if path.is_file() and path.suffix != ".la"
    )

    if not header.is_file():
        raise RuntimeError(f"SIROCCO header is not available: {header}")
    if not libraries:
        raise RuntimeError(f"SIROCCO library is not available in {library_dir}")

    return f"{header.name} and {libraries[0].name} available"


def _check_topcom_runtime():
    from sage.features.topcom import TOPCOM

    return _check_companion_feature(
        "sagelite_topcom", TOPCOM, "TOPCOM executable runtime"
    )


def _check_threejs_runtime():
    try:
        import sagelite_threejs_runtime  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.threejs import Threejs

    threejs = Threejs().is_present()
    if not bool(threejs):
        raise RuntimeError(f"Three.js runtime is not available: {threejs.reason}")
    return "Three.js static runtime available"


def _check_mathjax_runtime():
    try:
        import sagelite_mathjax_runtime
    except ImportError:
        return "not installed"

    from sage.env import MATHJAX_DIR

    tex_chtml = Path(sagelite_mathjax_runtime.tex_chtml_js_path())
    if not tex_chtml.is_file():
        raise RuntimeError(f"MathJax tex-chtml.js is not available: {tex_chtml}")
    if os.fspath(tex_chtml.parent) != MATHJAX_DIR:
        raise RuntimeError(
            f"Sage is not using the MathJax companion runtime: {MATHJAX_DIR}"
        )
    return "MathJax static runtime available"


def _check_d3js_runtime():
    try:
        import sagelite_d3js_runtime
    except ImportError:
        return "not installed"

    from pathlib import Path

    from sage.env import sage_data_paths

    d3js_file = Path(sagelite_d3js_runtime.d3_min_js_path())
    if not d3js_file.is_file():
        raise RuntimeError(f"D3.js runtime file is not available: {d3js_file}")
    if d3js_file.parent not in {Path(path) for path in sage_data_paths("d3js")}:
        raise RuntimeError("D3.js runtime is not registered in sage_data_paths")
    return "D3.js static runtime available"


def _check_jmol_runtime():
    try:
        import sagelite_jmol_runtime
    except ImportError:
        return "not installed"

    from pathlib import Path

    from sage.features.jmol import JmolDataJar

    jar = Path(sagelite_jmol_runtime.jmol_data_jar_path())
    if not jar.is_file():
        raise RuntimeError(f"JmolData.jar is not available: {jar}")
    jmol = JmolDataJar().is_present()
    if not bool(jmol):
        raise RuntimeError(f"JmolData.jar is not visible to Sage: {jmol.reason}")
    return "JmolData.jar available"


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


def _check_database_cremona_ellcurve():
    try:
        import sagelite_database_cremona_ellcurve  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.databases import DatabaseCremona

    database = DatabaseCremona().is_present()
    if not bool(database):
        raise RuntimeError(
            f"Cremona elliptic curve database is not available: {database.reason}"
        )
    return "cremona.db available"


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


def _check_database_cubic_hecke():
    from sage.databases.cubic_hecke_db import CubicHeckeDataBase

    database = CubicHeckeDataBase()
    version = database.version()
    basis = database.read(database.section.basis, nstrands=4)
    return f"database-cubic-hecke {version}, {len(basis)} basis elements"


def _check_database_knotinfo():
    from sage.databases.knotinfo_db import KnotInfoDataBase

    database = KnotInfoDataBase()
    version = database.version()
    return f"database-knotinfo {version}, {database.read_num_knots()} knots"


def _check_database_matroids():
    from sage.features.databases import DatabaseMatroids
    from sage.matroids.database_collections import AllMatroids

    database = DatabaseMatroids().is_present()
    if not bool(database):
        raise RuntimeError(f"matroid database is not available: {database.reason}")

    matroids = list(AllMatroids(2))
    return f"{len(matroids)} matroids on 2 elements available"


def _check_database_sloane():
    try:
        import sagelite_database_sloane  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.databases.sloane import SloaneEncyclopedia
    from sage.features.sloane_database import SloaneOEIS

    database = SloaneOEIS().is_present()
    if not bool(database):
        raise RuntimeError(f"Sloane/OEIS database is not available: {database.reason}")

    return SloaneEncyclopedia.sequence_name(1)


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


def _check_database_polytopes_4d():
    try:
        import sagelite_database_polytopes_4d  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.databases import DatabaseReflexivePolytopes

    database = DatabaseReflexivePolytopes("polytopes_db_4d").is_present()
    if not bool(database):
        raise RuntimeError(
            f"4D reflexive polytope database is not available: {database.reason}"
        )
    return "4D reflexive polytope data available"


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


def _check_database_stein_watkins():
    try:
        import sagelite_database_stein_watkins  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.databases.stein_watkins import SteinWatkinsAllData

    first_all = next(SteinWatkinsAllData(2))
    return f"first conductor in a.002: {first_all.conductor}"


def _optional_runtime_summary() -> None:
    print()
    print("optional runtimes:")

    try:
        from sage.features.singular import Singular
    except Exception as error:  # noqa: BLE001 - keep summary best-effort
        print(f"  Singular executable: unavailable ({error})")
    else:
        singular = Singular().is_present()
        print(f"  Singular executable: {'present' if singular else 'not found'}")

    try:
        import sagelite_maxima  # noqa: F401
    except Exception as error:  # noqa: BLE001 - keep summary best-effort
        print(f"  Maxima library mode: not available ({error})")
    else:
        print("  Maxima library mode: present")


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a quick smoke test of the installed sagelite runtime.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """
    Run a quick smoke test of the installed sagelite runtime.
    """
    _parse_args(argv)

    checks = [
        ("installed package requirements", _check_installed_requirements),
        ("PARI runtime packaging", _check_single_pari_runtime),
        ("PARI runtime conversion", _check_pari_runtime_roundtrip),
        ("Maxima library runtime", _check_maxima_runtime),
        ("required native imports", _check_required_native_imports),
        ("compiled source inspection paths", _check_source_inspection_paths),
        ("import sage.all", _check_import_sage_all),
        ("integer factorization", _check_factor),
        ("symbolic integration", _check_symbolic_integration),
        ("modular symbols", _check_modular_symbols),
        ("elliptic curve rank", _check_elliptic_curve_rank),
        ("eclib mwrank library", _check_eclib_mwrank),
        ("brial pbori library", _check_brial_pbori),
        ("lrcalc python library", _check_lrcalc),
        ("cddlib executable runtime", _check_cddlib_runtime),
        ("LiE executable runtime", _check_lie_runtime),
        ("PARI data runtime", _check_pari_data),
        ("Singular library runtime", _check_singular_runtime),
        ("libbraiding library", _check_libbraiding),
        ("libhomfly library", _check_libhomfly),
        ("bliss graph isomorphism library", _check_bliss_library),
        ("coxeter3 Coxeter group library", _check_coxeter3_library),
        ("mcqd clique library", _check_mcqd_library),
        ("tdlib tree decomposition library", _check_tdlib_library),
        ("CSDP executable runtime", _check_csdp_runtime),
        ("plantri graph generator runtime", _check_plantri_runtime),
        ("buckygen graph generator runtime", _check_buckygen_runtime),
        ("benzene graph generator runtime", _check_benzene_runtime),
        ("ECL executable runtime", _check_ecl_runtime),
        ("GAPDoc package runtime", _check_gapdoc_runtime),
        *[
            (
                f"GAP {display_name} package runtime",
                lambda package=package,
                module_name=module_name,
                display_name=display_name: _check_gap_package_runtime(
                    package, module_name, display_name
                ),
            )
            for package, module_name, display_name in GAP_PACKAGE_COMPANIONS
        ],
        ("GAP GUAVA Leon runtime", _check_gap_guava_leon_runtime),
        ("GAP3 executable runtime", _check_gap3_runtime),
        ("FriCAS executable runtime", _check_fricas_runtime),
        ("Frobby executable runtime", _check_frobby_runtime),
        ("gfan executable runtime", _check_gfan_runtime),
        ("Giac executable runtime", _check_giac_runtime),
        ("Graphviz executable runtime", _check_graphviz_runtime),
        ("Glucose executable runtime", _check_glucose_runtime),
        ("Kissat executable runtime", _check_kissat_runtime),
        ("ImageMagick executable runtime", _check_imagemagick_runtime),
        ("dvipng executable runtime", _check_dvipng_runtime),
        ("pdf2svg executable runtime", _check_pdf2svg_runtime),
        ("Poppler executable runtime", _check_poppler_runtime),
        ("GNU Info executable runtime", _check_info_runtime),
        ("LattE executable runtime", _check_latte_runtime),
        ("lcalc executable runtime", _check_lcalc_runtime),
        ("lrslib executable runtime", _check_lrslib_runtime),
        ("sympow executable runtime", _check_sympow_runtime),
        ("Kenzo ECL runtime", _check_kenzo_runtime),
        ("MeatAxe table runtime", _check_meataxe_runtime),
        ("nauty executable runtime", _check_nauty_runtime),
        ("4ti2 executable runtime", _check_four_ti_2_runtime),
        ("flatter executable runtime", _check_flatter_runtime),
        ("ECM executable runtime", _check_ecm_runtime),
        ("mwrank executable runtime", _check_mwrank_runtime),
        ("msolve executable runtime", _check_msolve_runtime),
        ("PALP executable runtime", _check_palp_runtime),
        ("planarity executable runtime", _check_planarity_runtime),
        ("QEPCAD executable runtime", _check_qepcad_runtime),
        ("Rubiks executable runtime", _check_rubiks_runtime),
        ("SIROCCO library runtime", _check_sirocco_runtime),
        ("TIDES compile-time runtime", _check_tides_runtime),
        ("Tachyon executable runtime", _check_tachyon_runtime),
        ("TOPCOM executable runtime", _check_topcom_runtime),
        ("MathJax static runtime", _check_mathjax_runtime),
        ("Three.js static runtime", _check_threejs_runtime),
        ("D3.js static runtime", _check_d3js_runtime),
        ("Jmol static runtime", _check_jmol_runtime),
        ("Cunningham tables runtime", _check_cunningham_tables),
        ("graphs database runtime", _check_database_graphs),
        ("Cremona mini database runtime", _check_database_cremona_mini),
        ("Cremona elliptic curve database runtime", _check_database_cremona_ellcurve),
        ("ellcurves database runtime", _check_database_ellcurves),
        ("Jones number field database runtime", _check_database_jones_numfield),
        ("Cubic Hecke database runtime", _check_database_cubic_hecke),
        ("KnotInfo database runtime", _check_database_knotinfo),
        ("matroid database runtime", _check_database_matroids),
        ("Sloane/OEIS database runtime", _check_database_sloane),
        ("Kohel polynomial database runtime", _check_database_kohel),
        ("reflexive polytopes database runtime", _check_database_polytopes),
        ("4D reflexive polytopes database runtime", _check_database_polytopes_4d),
        ("mutation class database runtime", _check_database_mutation_class),
        ("SymbolicData database runtime", _check_database_symbolic_data),
        ("Odlyzko zeta database runtime", _check_database_odlyzko_zeta),
        ("Stein-Watkins mini database runtime", _check_database_stein_watkins_mini),
        ("Stein-Watkins full database runtime", _check_database_stein_watkins),
    ]

    ok = True
    for name, check in checks:
        ok = _run_check(name, check) and ok

    _optional_runtime_summary()
    return 0 if ok else 1


if __name__ == "__main__":
    exit_code = main()
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(exit_code)
