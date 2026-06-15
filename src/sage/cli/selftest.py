"""
Small runtime self-test for sagelite installations.
"""

from __future__ import annotations

import argparse
import ctypes
import importlib
import importlib.metadata as importlib_metadata
import importlib.util
import os
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
from sage.arith.misc import primitive_root

print(primitive_root(389, check=False))
"""


def _check_pari_runtime_roundtrip():
    """
    Exercise the Sage Integer to cypari2 conversion in a subprocess.

    Mixed PARI runtimes can segfault during this conversion.  Keep the probe
    isolated so ``sagelite-selftest`` reports the packaging problem instead of
    dying later in a broader smoke test such as modular symbols.
    """
    return _run_subprocess_probe(_PARI_RUNTIME_PROBE, "PARI runtime probe")


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


def _check_cddlib_runtime():
    try:
        import sagelite_cddlib  # noqa: F401
    except ImportError:
        return "not installed"

    from sage.features.cddlib import CddExecutable

    executables = {}
    for program in ("cddexec", "cddexec_gmp"):
        feature = CddExecutable(program).is_present()
        if not bool(feature):
            raise RuntimeError(
                f"cddlib executable {program!r} is not available: {feature.reason}"
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
    from sage.all import BraidGroup
    from sage.libs.braiding import leftnormalform

    braid = BraidGroup(3)([1, 2, 1, -2])
    return leftnormalform(braid)


def _check_libhomfly():
    from sage.libs.homfly import homfly_polynomial_dict

    trefoil = "1 6 0 1  1 -1  2 1  0 -1  1 1  2 -1 0 1 1 1 2 1"
    return homfly_polynomial_dict(trefoil)


def _check_bliss_library():
    from sage.all import graphs

    graph = graphs.PetersenGraph()
    canonical = graph.canonical_label(algorithm="bliss")
    return f"canonical Petersen graph has {canonical.num_verts()} vertices"


def _check_coxeter3_library():
    from sage.combinat.root_system.coxeter_group import CoxeterGroup

    group = CoxeterGroup(["A", 3], implementation="coxeter3")
    return f"A3 long element length {group.long_element().length()}"


def _check_mcqd_library():
    from sage.all import graphs

    graph = graphs.PetersenGraph()
    cover_size = graph.vertex_cover(algorithm="mcqd", value_only=True)
    return f"Petersen vertex cover size {cover_size}"


def _check_tdlib_library():
    from sage.all import graphs

    graph = graphs.PetersenGraph()
    return f"Petersen treewidth {graph.treewidth(algorithm='tdlib')}"


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
    if os.fspath(command) != ECL_CONFIG:
        raise RuntimeError(
            f"Sage is not using the ECL companion ecl-config: {ECL_CONFIG}"
        )

    ecldir = Path(runtime.ecl_dir())
    if not ecldir.is_dir():
        raise RuntimeError(f"ECL support directory is not available: {ecldir}")
    return "ECL command and support directory available"


def _check_gap3_runtime():
    from sage.features.gap3 import Gap3

    return _check_companion_feature(
        "sagelite_gap3", Gap3, "GAP3 executable runtime"
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


def _check_fricas_runtime():
    from sage.features.fricas import FriCAS

    return _check_companion_feature(
        "sagelite_fricas", FriCAS, "FriCAS executable runtime"
    )


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
    if os.fspath(command) != SYMPOW:
        raise RuntimeError(f"Sage is not using the sympow companion runtime: {SYMPOW}")
    return "sympow executable runtime available"


_MAXIMA_RUNTIME_PROBE = """
from sage.cli.selftest import _check_loaded_ecl_matches_maxima_runtime

_check_loaded_ecl_matches_maxima_runtime()

from sage.all import RR, var
from sage.interfaces.maxima_lib import maxima_lib

value = maxima_lib.eval("1+1")
x = var("x", domain=RR)
if x.conjugate() != x:
    raise RuntimeError("Maxima-backed symbolic assumptions are not available")
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

    importlib.import_module("sage.libs.ecl")

    maxima_fas = Path(runtime.maxima_fas())
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
    from sage.features.planarity import Planarity

    return _check_companion_feature(
        "sagelite_planarity", Planarity, "planarity executable runtime"
    )


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
    if os.fspath(command) != TACHYON:
        raise RuntimeError(f"Sage is not using the Tachyon companion runtime: {TACHYON}")
    return "Tachyon executable runtime available"


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

    ok = _run_check("installed package requirements", _check_installed_requirements)
    if not _run_check("PARI runtime packaging", _check_single_pari_runtime):
        return 1
    if not _run_check("PARI runtime conversion", _check_pari_runtime_roundtrip):
        return 1
    if not _run_check("Maxima library runtime", _check_maxima_runtime):
        return 1

    checks = [
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

    for name, check in checks:
        ok = _run_check(name, check) and ok

    _optional_runtime_summary()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
