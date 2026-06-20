#!/usr/bin/env python3
"""
Required native wheel surface for Linux sagelite release wheels.

The lists here are intentionally prefix-based because extension filenames carry
Python ABI tags and auditwheel-renamed shared libraries carry platform suffixes.
"""

from __future__ import annotations

import json
import sys


REQUIRED_MESON_OPTIONS = [
    "bliss",
    "brial",
    "coxeter3",
    "eclib",
    "libbraiding",
    "libhomfly",
    "meataxe",
    "mcqd",
    "rankwidth",
    "sirocco",
    "tdlib",
]

REQUIRED_NATIVE_EXTENSION_PREFIXES = [
    "sage/graphs/bliss.",
    "sage/graphs/cliquer.",
    "sage/graphs/graph_decompositions/rankwidth.",
    "sage/graphs/graph_decompositions/tdlib.",
    "sage/graphs/mcqd.",
    "sage/graphs/planarity.",
    "sage/libs/braiding.",
    "sage/libs/coxeter3/coxeter.",
    "sage/libs/eclib/mwrank.",
    "sage/libs/eclib/newforms.",
    "sage/libs/homfly.",
    "sage/libs/meataxe.",
    "sage/libs/sirocco.",
    "sage/libs/symmetrica/symmetrica.",
    "sage/numerical/backends/glpk_backend.",
    "sage/numerical/backends/glpk_exact_backend.",
    "sage/numerical/backends/glpk_graph_backend.",
    "sage/rings/polynomial/pbori/pbori.",
]

REQUIRED_NATIVE_LIBRARY_PREFIXES = [
    "libbliss",
    "libbraiding",
    "libbrial",
    "libbrial_groebner",
    "libcliquer",
    "libcoxeter3",
    "libhomfly",
    "libmtx",
    "libplanarity",
    "libsirocco",
]

REQUIRED_NATIVE_IMPORT_MODULES = [
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
    "sage.libs.sirocco",
    "sage.libs.symmetrica.symmetrica",
    "sage.numerical.backends.glpk_backend",
    "sage.numerical.backends.glpk_exact_backend",
    "sage.numerical.backends.glpk_graph_backend",
    "sage.rings.polynomial.pbori.pbori",
]


def catalog() -> dict[str, list[str]]:
    return {
        "required_meson_options": REQUIRED_MESON_OPTIONS,
        "required_native_extension_prefixes": REQUIRED_NATIVE_EXTENSION_PREFIXES,
        "required_native_library_prefixes": REQUIRED_NATIVE_LIBRARY_PREFIXES,
        "required_native_import_modules": REQUIRED_NATIVE_IMPORT_MODULES,
    }


def main() -> int:
    json.dump(catalog(), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
