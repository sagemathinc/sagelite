from __future__ import annotations

import email.parser
import importlib.util
import json
import os
import sys
import tomllib
from pathlib import Path

import pytest
from packaging.requirements import Requirement
from packaging.version import Version


ROOT = Path(__file__).resolve().parents[1]


def _load_native_catalog():
    path = ROOT / "tools" / "sagelite_native_wheel_catalog.py"
    spec = importlib.util.spec_from_file_location("sagelite_native_wheel_catalog", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


NATIVE_WHEEL_CATALOG = _load_native_catalog()


def test_native_wheel_catalog_exports_stable_json(capsys):
    assert NATIVE_WHEEL_CATALOG.main() == 0
    payload = json.loads(capsys.readouterr().out)

    assert payload == {
        "required_meson_options": RELEASE_REQUIRED_MESON_OPTIONS,
        "required_native_extension_prefixes": RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES,
        "required_native_library_prefixes": RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES,
        "required_native_import_modules": RELEASE_REQUIRED_NATIVE_IMPORT_MODULES,
        "required_native_smoke_import_modules": (
            RELEASE_REQUIRED_NATIVE_SMOKE_IMPORT_MODULES
        ),
    }
    assert "coxeter3" in payload["required_meson_options"]
    assert "sage/libs/coxeter3/coxeter." in (
        payload["required_native_extension_prefixes"]
    )
    assert "sage/libs/ntl/error." in payload["required_native_extension_prefixes"]
    assert "libcoxeter3" in payload["required_native_library_prefixes"]
    assert "libntl" in payload["required_native_library_prefixes"]
    assert "sage.libs.coxeter3.coxeter" in payload["required_native_import_modules"]
    assert "sage.libs.ntl.error" in payload["required_native_import_modules"]
    assert "sage.libs.coxeter3.coxeter" in (
        payload["required_native_smoke_import_modules"]
    )
    assert "sage.graphs.graph_decompositions.tdlib" in (
        payload["required_native_import_modules"]
    )
    assert "sage.graphs.graph_decompositions.tdlib" not in (
        payload["required_native_smoke_import_modules"]
    )


RUNTIME_PACKAGE_DATA = {
    "sagelite-4ti2-runtime": {
        "sagelite_four_ti_2": ["data/bin/*"],
    },
    "sagelite-benzene-runtime": {
        "sagelite_benzene": ["data/bin/*"],
    },
    "sagelite-buckygen-runtime": {
        "sagelite_buckygen": ["data/bin/*"],
    },
    "sagelite-cddlib-runtime": {
        "sagelite_cddlib": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-csdp-runtime": {
        "sagelite_csdp": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-d3js-runtime": {
        "sagelite_d3js_runtime": ["data/d3js/**/*"],
    },
    "sagelite-dvipng-runtime": {
        "sagelite_dvipng": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-ecl-runtime": {
        "sagelite_ecl": [
            "data/bin/*",
            "data/include/ecl/**/*",
            "data/lib/*",
            "data/lib/ecl*/**/*",
        ],
    },
    "sagelite-ecm-runtime": {
        "sagelite_ecm": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-flatter-runtime": {
        "sagelite_flatter": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-frobby-runtime": {
        "sagelite_frobby": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-fricas-runtime": {
        "sagelite_fricas": [
            "data/bin/*",
            "data/lib/fricas/**/*",
            "data/share/fricas/**/*",
        ],
    },
    "sagelite-fplll-data": {
        "sagelite_fplll_data": ["data/strategies/*.json"],
    },
    "sagelite-gap-runtime": {
        "sagelite_gap_runtime": ["data/bin/*", "data/gap*/**/*"],
    },
    "sagelite-gap-package-atlasrep": {
        "sagelite_gap_package_atlasrep": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-ctbllib": {
        "sagelite_gap_package_ctbllib": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-design": {
        "sagelite_gap_package_design": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-gapdoc": {
        "sagelite_gap_package_gapdoc": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-grape": {
        "sagelite_gap_package_grape": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-guava": {
        "sagelite_gap_package_guava": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-hap": {
        "sagelite_gap_package_hap": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-polenta": {
        "sagelite_gap_package_polenta": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-polycyclic": {
        "sagelite_gap_package_polycyclic": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-primgrp": {
        "sagelite_gap_package_primgrp": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-qpa": {
        "sagelite_gap_package_qpa": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-quagroup": {
        "sagelite_gap_package_quagroup": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-repsn": {
        "sagelite_gap_package_repsn": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-smallgrp": {
        "sagelite_gap_package_smallgrp": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-tomlib": {
        "sagelite_gap_package_tomlib": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-transgrp": {
        "sagelite_gap_package_transgrp": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap3-runtime": {
        "sagelite_gap3": ["data/gap3/**/*"],
    },
    "sagelite-gfan-runtime": {
        "sagelite_gfan": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-giac-runtime": {
        "sagelite_giac": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-glucose-runtime": {
        "sagelite_glucose": ["data/bin/*"],
    },
    "sagelite-graphviz-runtime": {
        "sagelite_graphviz": [
            "data/bin/*",
            "data/lib/*",
            "data/lib/graphviz/*",
        ],
    },
    "sagelite-imagemagick-runtime": {
        "sagelite_imagemagick": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-info-runtime": {
        "sagelite_info": [
            "data/bin/*",
            "data/lib/*",
            "data/share/info/**/*",
        ],
    },
    "sagelite-jmol-runtime": {
        "sagelite_jmol_runtime": ["data/jmol/**/*"],
    },
    "sagelite-kenzo-runtime": {
        "sagelite_kenzo": ["data/kenzo.fas"],
    },
    "sagelite-kissat-runtime": {
        "sagelite_kissat": ["data/bin/*"],
    },
    "sagelite-latte-runtime": {
        "sagelite_latte": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-lcalc-runtime": {
        "sagelite_lcalc": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-lie-runtime": {
        "sagelite_lie": ["data/bin/*", "data/LiE/**/*"],
    },
    "sagelite-lrslib-runtime": {
        "sagelite_lrslib": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-maxima-runtime": {
        "sagelite_maxima": [
            "data/bin/*",
            "data/lib/**/*",
            "data/share/**/*",
        ],
    },
    "sagelite-mathjax-runtime": {
        "sagelite_mathjax_runtime": ["data/mathjax/**/*"],
    },
    "sagelite-meataxe-runtime": {
        "sagelite_meataxe": ["data/meataxe/*"],
    },
    "sagelite-mwrank-runtime": {
        "sagelite_mwrank": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-msolve-runtime": {
        "sagelite_msolve": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-nauty-runtime": {
        "sagelite_nauty": ["data/bin/*"],
    },
    "sagelite-palp-runtime": {
        "sagelite_palp": ["data/bin/*"],
    },
    "sagelite-pdf2svg-runtime": {
        "sagelite_pdf2svg": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-planarity-runtime": {
        "sagelite_planarity": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-plantri-runtime": {
        "sagelite_plantri": ["data/bin/*"],
    },
    "sagelite-poppler-runtime": {
        "sagelite_poppler": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-qepcad-runtime": {
        "sagelite_qepcad": [
            "data/root/bin/qepcad",
            "data/root/etc/default.qepcadrc",
            "data/root/share/qepcad/qepcad.help",
        ],
    },
    "sagelite-rubiks-runtime": {
        "sagelite_rubiks": ["data/bin/*"],
    },
    "sagelite-singular-runtime": {
        "sagelite_singular_runtime": [
            "data/bin/*",
            "data/lib/*",
            "data/singular/**/*",
        ],
    },
    "sagelite-sirocco-runtime": {
        "sagelite_sirocco": ["data/include/*", "data/lib/*"],
    },
    "sagelite-sympow-runtime": {
        "sagelite_sympow": [
            "data/bin/*",
            "data/datafiles/**/*",
            "data/lib/*",
        ],
    },
    "sagelite-tachyon-runtime": {
        "sagelite_tachyon": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-threejs-runtime": {
        "sagelite_threejs_runtime": ["data/threejs-sage/**/*"],
    },
    "sagelite-tides-runtime": {
        "sagelite_tides": ["data/include/*", "data/lib/*"],
    },
    "sagelite-topcom-runtime": {
        "sagelite_topcom": ["data/bin/*", "data/lib/*"],
    },
}

SOURCE_BUNDLED_DATA_PACKAGE_DATA = {
    "sagelite-database-cremona-mini": {
        "sagelite_database_cremona_mini": [
            "data/cremona/cremona_mini.db",
        ],
    },
    "sagelite-database-ellcurves": {
        "sagelite_database_ellcurves": [
            "data/ellcurves/rank*",
        ],
    },
    "sagelite-database-graphs": {
        "sagelite_database_graphs": [
            "data/graphs/brouwer_srg_database.json",
            "data/graphs/graphs.db",
            "data/graphs/isgci_sage.xml",
            "data/graphs/smallgraphs.txt",
        ],
    },
    "sagelite-database-jones-numfield": {
        "sagelite_database_jones_numfield": [
            "data/jones/jones.sobj",
        ],
    },
    "sagelite-database-kohel": {
        "sagelite_database_kohel": [
            "data/kohel/**/*",
        ],
    },
    "sagelite-database-mutation-class": {
        "sagelite_database_mutation_class": [
            "data/cluster_algebra_quiver/mutation_classes_*.dig6",
        ],
    },
    "sagelite-database-odlyzko-zeta": {
        "sagelite_database_odlyzko_zeta": [
            "data/odlyzko/zeros.sobj",
        ],
    },
    "sagelite-database-polytopes": {
        "sagelite_database_polytopes": [
            "data/reflexive_polytopes/**/*",
        ],
    },
    "sagelite-database-stein-watkins-mini": {
        "sagelite_database_stein_watkins_mini": [
            "data/stein_watkins/a.000.bz2",
            "data/stein_watkins/a.001.bz2",
            "data/stein_watkins/p.00.bz2",
        ],
    },
    "sagelite-database-symbolic-data": {
        "sagelite_database_symbolic_data": [
            "data/symbolic_data/COPYING",
            "data/symbolic_data/Data/**/*",
        ],
    },
}

BUILD_COPIED_DATA_PACKAGE_DATA = {
    "sagelite-cunningham-tables": {
        "sagelite_cunningham_tables": [
            "data/cunningham_tables/cunningham_prime_factors.sobj",
        ],
    },
    "sagelite-database-cremona-ellcurve": {
        "sagelite_database_cremona_ellcurve": [
            "data/cremona/cremona.db",
        ],
    },
    "sagelite-database-polytopes-4d": {
        "sagelite_database_polytopes_4d": [
            "data/reflexive_polytopes/Hodge4d/**/*",
        ],
    },
    "sagelite-database-sloane": {
        "sagelite_database_sloane": [
            "data/sloane/sloane-oeis.bz2",
            "data/sloane/sloane-names.bz2",
        ],
    },
    "sagelite-database-stein-watkins": {
        "sagelite_database_stein_watkins": [
            "data/stein_watkins/**/*",
        ],
    },
    "sagelite-pari-data": {
        "sagelite_pari_data": [
            "data/pari/galdata/**/*",
            "data/pari/elldata/**/*",
            "data/pari/seadata/**/*",
            "data/pari/galpol/**/*",
            "data/pari/nftables/**/*",
            "data/pari/buzzard/**/*",
            "data/pari/dokchitser/**/*",
            "data/pari/simon/**/*",
        ],
    },
}

REPAIR_WORKFLOW_BUILT_RUNTIME_PACKAGES = {
    "sagelite-4ti2-runtime",
    "sagelite-benzene-runtime",
    "sagelite-buckygen-runtime",
    "sagelite-cddlib-runtime",
    "sagelite-csdp-runtime",
    "sagelite-dvipng-runtime",
    "sagelite-ecm-runtime",
    "sagelite-flatter-runtime",
    "sagelite-fplll-data",
    "sagelite-frobby-runtime",
    "sagelite-gap-runtime",
    "sagelite-gfan-runtime",
    "sagelite-giac-runtime",
    "sagelite-glucose-runtime",
    "sagelite-info-runtime",
    "sagelite-kissat-runtime",
    "sagelite-latte-runtime",
    "sagelite-lcalc-runtime",
    "sagelite-lie-runtime",
    "sagelite-lrslib-runtime",
    "sagelite-maxima-runtime",
    "sagelite-meataxe-runtime",
    "sagelite-msolve-runtime",
    "sagelite-mwrank-runtime",
    "sagelite-nauty-runtime",
    "sagelite-palp-runtime",
    "sagelite-pdf2svg-runtime",
    "sagelite-planarity-runtime",
    "sagelite-plantri-runtime",
    "sagelite-qepcad-runtime",
    "sagelite-rubiks-runtime",
    "sagelite-singular-runtime",
    "sagelite-sympow-runtime",
    "sagelite-tachyon-runtime",
    "sagelite-tides-runtime",
    "sagelite-topcom-runtime",
}

REPAIR_WORKFLOW_EXTERNAL_RUNTIME_PACKAGES = {
    "sagelite-d3js-runtime",
    "sagelite-ecl-runtime",
    "sagelite-gap3-runtime",
    "sagelite-fricas-runtime",
    "sagelite-gap-package-atlasrep",
    "sagelite-gap-package-ctbllib",
    "sagelite-gap-package-design",
    "sagelite-gap-package-gapdoc",
    "sagelite-gap-package-grape",
    "sagelite-gap-package-guava",
    "sagelite-gap-package-hap",
    "sagelite-gap-package-polenta",
    "sagelite-gap-package-polycyclic",
    "sagelite-gap-package-primgrp",
    "sagelite-gap-package-qpa",
    "sagelite-gap-package-quagroup",
    "sagelite-gap-package-repsn",
    "sagelite-gap-package-smallgrp",
    "sagelite-gap-package-tomlib",
    "sagelite-gap-package-transgrp",
    "sagelite-jmol-runtime",
    "sagelite-kenzo-runtime",
    "sagelite-graphviz-runtime",
    "sagelite-imagemagick-runtime",
    "sagelite-lie-runtime",
    "sagelite-mathjax-runtime",
    "sagelite-poppler-runtime",
    "sagelite-sirocco-runtime",
    "sagelite-threejs-runtime",
}

COMPANION_WORKFLOW_BUILT_RUNTIME_PACKAGES = {
    "sagelite-4ti2-runtime",
    "sagelite-benzene-runtime",
    "sagelite-buckygen-runtime",
    "sagelite-cddlib-runtime",
    "sagelite-csdp-runtime",
    "sagelite-d3js-runtime",
    "sagelite-dvipng-runtime",
    "sagelite-ecl-runtime",
    "sagelite-ecm-runtime",
    "sagelite-flatter-runtime",
    "sagelite-fplll-data",
    "sagelite-frobby-runtime",
    "sagelite-fricas-runtime",
    "sagelite-gap-runtime",
    "sagelite-gap-package-atlasrep",
    "sagelite-gap-package-ctbllib",
    "sagelite-gap-package-design",
    "sagelite-gap-package-gapdoc",
    "sagelite-gap-package-grape",
    "sagelite-gap-package-guava",
    "sagelite-gap-package-hap",
    "sagelite-gap-package-polenta",
    "sagelite-gap-package-polycyclic",
    "sagelite-gap-package-primgrp",
    "sagelite-gap-package-qpa",
    "sagelite-gap-package-quagroup",
    "sagelite-gap-package-repsn",
    "sagelite-gap-package-smallgrp",
    "sagelite-gap-package-tomlib",
    "sagelite-gap-package-transgrp",
    "sagelite-gfan-runtime",
    "sagelite-giac-runtime",
    "sagelite-glucose-runtime",
    "sagelite-graphviz-runtime",
    "sagelite-imagemagick-runtime",
    "sagelite-info-runtime",
    "sagelite-kenzo-runtime",
    "sagelite-kissat-runtime",
    "sagelite-latte-runtime",
    "sagelite-lcalc-runtime",
    "sagelite-lrslib-runtime",
    "sagelite-mathjax-runtime",
    "sagelite-maxima-runtime",
    "sagelite-meataxe-runtime",
    "sagelite-mwrank-runtime",
    "sagelite-msolve-runtime",
    "sagelite-nauty-runtime",
    "sagelite-palp-runtime",
    "sagelite-pari-data",
    "sagelite-pdf2svg-runtime",
    "sagelite-planarity-runtime",
    "sagelite-plantri-runtime",
    "sagelite-poppler-runtime",
    "sagelite-qepcad-runtime",
    "sagelite-rubiks-runtime",
    "sagelite-singular-runtime",
    "sagelite-sirocco-runtime",
    "sagelite-sympow-runtime",
    "sagelite-tachyon-runtime",
    "sagelite-threejs-runtime",
    "sagelite-tides-runtime",
    "sagelite-topcom-runtime",
}

RELEASE_WORKFLOW_SEPARATED_RUNTIME_PACKAGES = {
    "sagelite-4ti2-runtime": "four-ti-2-runtime-dist",
    "sagelite-benzene-runtime": "benzene-runtime-dist",
    "sagelite-buckygen-runtime": "buckygen-runtime-dist",
    "sagelite-cddlib-runtime": "cddlib-runtime-dist",
    "sagelite-csdp-runtime": "csdp-runtime-dist",
    "sagelite-dvipng-runtime": "dvipng-runtime-dist",
    "sagelite-ecm-runtime": "ecm-runtime-dist",
    "sagelite-flatter-runtime": "flatter-runtime-dist",
    "sagelite-frobby-runtime": "frobby-runtime-dist",
    "sagelite-gap3-runtime": "gap3-runtime-dist",
    "sagelite-gap-runtime": "gap-runtime-dist",
    "sagelite-gfan-runtime": "gfan-runtime-dist",
    "sagelite-giac-runtime": "giac-runtime-dist",
    "sagelite-glucose-runtime": "glucose-runtime-dist",
    "sagelite-graphviz-runtime": "graphviz-runtime-dist",
    "sagelite-info-runtime": "info-runtime-dist",
    "sagelite-kissat-runtime": "kissat-runtime-dist",
    "sagelite-latte-runtime": "latte-runtime-dist",
    "sagelite-lcalc-runtime": "lcalc-runtime-dist",
    "sagelite-lie-runtime": "lie-runtime-dist",
    "sagelite-lrslib-runtime": "lrslib-runtime-dist",
    "sagelite-maxima-runtime": "maxima-runtime-dist",
    "sagelite-meataxe-runtime": "meataxe-runtime-dist",
    "sagelite-msolve-runtime": "msolve-runtime-dist",
    "sagelite-mwrank-runtime": "mwrank-runtime-dist",
    "sagelite-nauty-runtime": "nauty-runtime-dist",
    "sagelite-palp-runtime": "palp-runtime-dist",
    "sagelite-pdf2svg-runtime": "pdf2svg-runtime-dist",
    "sagelite-planarity-runtime": "planarity-runtime-dist",
    "sagelite-plantri-runtime": "plantri-runtime-dist",
    "sagelite-poppler-runtime": "poppler-runtime-dist",
    "sagelite-qepcad-runtime": "qepcad-runtime-dist",
    "sagelite-rubiks-runtime": "rubiks-runtime-dist",
    "sagelite-singular-runtime": "singular-runtime-dist",
    "sagelite-sympow-runtime": "sympow-runtime-dist",
    "sagelite-tachyon-runtime": "tachyon-runtime-dist",
    "sagelite-tides-runtime": "tides-runtime-dist",
    "sagelite-topcom-runtime": "topcom-runtime-dist",
}

COMPANION_WORKFLOW_DATA_PACKAGES = {
    "sagelite-cunningham-tables",
    "sagelite-database-cremona-ellcurve",
    "sagelite-database-cremona-mini",
    "sagelite-database-ellcurves",
    "sagelite-database-graphs",
    "sagelite-database-jones-numfield",
    "sagelite-database-kohel",
    "sagelite-database-mutation-class",
    "sagelite-database-odlyzko-zeta",
    "sagelite-database-polytopes",
    "sagelite-database-polytopes-4d",
    "sagelite-database-sloane",
    "sagelite-database-stein-watkins",
    "sagelite-database-stein-watkins-mini",
    "sagelite-database-symbolic-data",
}

BASE_SAGELITE_DATA_DEPENDENCIES = {
    "sagelite-cunningham-tables >=10.9,<10.10",
    "sagelite-d3js-runtime >=10.9,<10.10",
    "sagelite-threejs-runtime >=10.9,<10.10",
    "sagelite-database-cremona-mini >=10.9.post1,<10.10",
    "sagelite-database-ellcurves >=10.9,<10.10",
    "sagelite-database-graphs >=10.9,<10.10",
    "sagelite-database-jones-numfield >=10.9,<10.10",
    "sagelite-database-kohel >=10.9,<10.10",
    "sagelite-database-mutation-class >=10.9,<10.10",
    "sagelite-database-odlyzko-zeta >=10.9,<10.10",
    "sagelite-database-polytopes >=10.9,<10.10",
    "sagelite-database-stein-watkins-mini >=10.9,<10.10",
    "sagelite-database-symbolic-data >=10.9,<10.10",
    "sagelite-mathjax-runtime >=10.9,<10.10",
    "sagelite-pari-data >=10.9,<10.10",
}

DATA_COMPANION_EXTRA_ALIASES = {
    "cremona_ellcurve": "sagelite-database-cremona-ellcurve >=10.9,<10.10",
    "database_polytopes": "sagelite-database-polytopes >=10.9,<10.10",
    "database_polytopes_4d": "sagelite-database-polytopes-4d >=10.9,<10.10",
    "jones_numfield": "sagelite-database-jones-numfield >=10.9,<10.10",
    "mutation_class": "sagelite-database-mutation-class >=10.9,<10.10",
    "odlyzko_zeta": "sagelite-database-odlyzko-zeta >=10.9,<10.10",
    "pari_data": "sagelite-pari-data >=10.9,<10.10",
    "polytopes_4d": "sagelite-database-polytopes-4d >=10.9,<10.10",
    "stein_watkins": "sagelite-database-stein-watkins >=10.9,<10.10",
    "stein_watkins_mini": "sagelite-database-stein-watkins-mini >=10.9,<10.10",
    "symbolic_data": "sagelite-database-symbolic-data >=10.9,<10.10",
}

BASE_SAGELITE_STANDARD_RUNTIME_DEPENDENCIES = {
    "sagelite-4ti2-runtime >=10.9,<10.10",
    "sagelite-benzene-runtime >=10.9,<10.10",
    "sagelite-buckygen-runtime >=10.9,<10.10",
    "sagelite-cddlib-runtime >=10.9,<10.10",
    "sagelite-dvipng-runtime >=10.9,<10.10",
    "sagelite-ecm-runtime >=10.9,<10.10",
    "sagelite-flatter-runtime >=10.9,<10.10",
    "sagelite-frobby-runtime >=10.9,<10.10",
    "sagelite-gfan-runtime >=10.9,<10.10",
    "sagelite-graphviz-runtime >=10.9.post1,<10.10",
    "sagelite-latte-runtime >=10.9,<10.10",
    "sagelite-lcalc-runtime >=10.9,<10.10",
    "sagelite-mwrank-runtime >=10.9,<10.10",
    "sagelite-palp-runtime >=10.9,<10.10",
    "sagelite-pdf2svg-runtime >=10.9,<10.10",
    "sagelite-poppler-runtime >=10.9,<10.10",
    "sagelite-singular-runtime >=10.9.post1,<10.10",
    "sagelite-sirocco-runtime >=10.9,<10.10",
    "sagelite-tides-runtime >=10.9,<10.10",
    "sagelite-topcom-runtime >=10.9,<10.10",
}

BASE_SAGELITE_STANDARD_PYPI_RUNTIME_DEPENDENCIES = {
    "cvxopt >=1.3.3",
    "dot2tex >=2.11.3",
    "imageio-ffmpeg >=0.6.0",
    "igraph",
    "jupyter-jsmol >=2022.1.0",
    "khoca >=1.4",
    'lrcalc ~=2.1; sys_platform != "win32"',
    "Mathics3 >=10.0.1; python_version < '3.14'",
    "packaging",
    "phitigra >=0.2.6",
    'primecountpy >=0.2.1; sys_platform != "win32"',
    "pypandoc-binary >=1.17",
    "pycosat >=0.6.3",
    (
        "pycryptosat; python_version < '3.13' and "
        "(sys_platform == 'darwin' or "
        "(sys_platform == 'linux' and platform_machine == 'x86_64'))"
    ),
    'pynormaliz >=2.18; sys_platform != "win32"',
    "regina >=7.4.1",
    "symengine >= 0.6.1",
}

OPTIONAL_CVXPY_SOLVER_RUNTIME_DEPENDENCIES = {
    "cvxpy": "cvxpy >=1.6.7",
    "cylp": "cylp >=0.92.3",
    "ortools": "ortools >=9.11",
    "pyscipopt": "pyscipopt >=5.1.1",
}

PUBLISHABLE_STATIC_RUNTIME_PACKAGES = {
    "sagelite-d3js-runtime",
    "sagelite-mathjax-runtime",
    "sagelite-threejs-runtime",
}

RELEASE_REQUIRED_MESON_OPTIONS = (
    NATIVE_WHEEL_CATALOG.REQUIRED_MESON_OPTIONS
)
RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES = (
    NATIVE_WHEEL_CATALOG.REQUIRED_NATIVE_EXTENSION_PREFIXES
)
RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES = (
    NATIVE_WHEEL_CATALOG.REQUIRED_NATIVE_LIBRARY_PREFIXES
)
RELEASE_REQUIRED_NATIVE_IMPORT_MODULES = (
    NATIVE_WHEEL_CATALOG.REQUIRED_NATIVE_IMPORT_MODULES
)
RELEASE_REQUIRED_NATIVE_SMOKE_IMPORT_MODULES = (
    NATIVE_WHEEL_CATALOG.REQUIRED_NATIVE_SMOKE_IMPORT_MODULES
)


GAP_PACKAGE_EXTRA_REQUIREMENTS = {
    "atlasrep": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-atlasrep >=10.9,<10.10",
    ],
    "ctbllib": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-ctbllib >=10.9,<10.10",
    ],
    "design": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-design >=10.9,<10.10",
    ],
    "gapdoc": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-gapdoc >=10.9,<10.10",
    ],
    "grape": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-grape >=10.9,<10.10",
    ],
    "guava": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-guava >=10.9,<10.10",
    ],
    "hap": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-hap >=10.9,<10.10",
    ],
    "polenta": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-polenta >=10.9,<10.10",
    ],
    "polycyclic": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-polycyclic >=10.9,<10.10",
    ],
    "primgrp": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-primgrp >=10.9,<10.10",
    ],
    "qpa": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-qpa >=10.9,<10.10",
    ],
    "quagroup": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-quagroup >=10.9,<10.10",
    ],
    "repsn": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-repsn >=10.9,<10.10",
    ],
    "smallgrp": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-smallgrp >=10.9,<10.10",
    ],
    "tomlib": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-tomlib >=10.9,<10.10",
    ],
    "transgrp": [
        "sagelite-gap-runtime >=10.9.post2,<10.10",
        "sagelite-gap-package-transgrp >=10.9,<10.10",
    ],
}

DEFAULT_GAP_PACKAGE_COMPANION_DEPENDENCIES: set[str] = set()


def _pyproject(name: str) -> dict:
    with (ROOT / "companion-packages" / name / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)


def _maxima_runtime_setup_helpers() -> dict:
    setup_py = ROOT / "companion-packages" / "sagelite-maxima-runtime" / "setup.py"
    source = setup_py.read_text()
    start = source.index("def _dynamic_symbols")
    end = source.index("\ndef _copy_maxima_info_indexes")
    namespace = {"os": os, "Path": Path, "REPO_ROOT": ROOT, "subprocess": None}
    exec(source[start:end], namespace)
    return namespace


def _load_gap_runtime_module():
    runtime_path = (
        ROOT
        / "companion-packages"
        / "sagelite-gap-runtime"
        / "src"
        / "sagelite_gap_runtime"
        / "runtime.py"
    )
    spec = importlib.util.spec_from_file_location(
        "test_sagelite_gap_runtime", runtime_path
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _companion_versions() -> dict[str, Version]:
    versions = {}
    for pyproject_toml in (ROOT / "companion-packages").glob(
        "sagelite-*/pyproject.toml"
    ):
        pyproject = tomllib.loads(pyproject_toml.read_text())
        versions[pyproject["project"]["name"]] = Version(
            pyproject["project"]["version"]
        )
    return versions


def _requirement_minimum_version(requirement: Requirement) -> Version | None:
    lower_bounds = [
        Version(specifier.version)
        for specifier in requirement.specifier
        if specifier.operator in {">=", ">", "~="}
    ]
    return max(lower_bounds) if lower_bounds else None


def test_sagelite_dependency_floors_match_companion_package_versions():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    companion_versions = _companion_versions()
    requirements = list(pyproject["project"]["dependencies"])
    for extra_requirements in pyproject["project"]["optional-dependencies"].values():
        requirements.extend(extra_requirements)

    for requirement_text in requirements:
        requirement = Requirement(requirement_text)
        companion_version = companion_versions.get(requirement.name)
        if companion_version is None:
            continue

        minimum_version = _requirement_minimum_version(requirement)
        assert minimum_version is not None
        assert minimum_version >= companion_version, requirement_text


def test_generated_companion_egg_info_matches_pyproject_when_present():
    for pyproject_toml in (ROOT / "companion-packages").glob(
        "sagelite-*/pyproject.toml"
    ):
        pyproject = tomllib.loads(pyproject_toml.read_text())
        project = pyproject["project"]

        for pkg_info in pyproject_toml.parent.glob("src/*.egg-info/PKG-INFO"):
            metadata = email.parser.Parser().parsestr(pkg_info.read_text())

            assert metadata["Name"] == project["name"], pkg_info
            assert metadata["Version"] == project["version"], pkg_info


def test_sagelite_default_dependencies_include_public_index_doctest_companions():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    dependencies = set(pyproject["project"]["dependencies"])

    assert "sagelite-database-cremona-mini >=10.9.post1,<10.10" in dependencies
    assert "database-cubic-hecke ==2022.4.4" in dependencies
    assert "database-knotinfo >=2026.3.1" in dependencies
    assert "sagelite-database-cremona-ellcurve >=10.9,<10.10" not in dependencies
    assert "sagelite-ecl-runtime >=10.9,<10.10" not in dependencies
    assert "sagelite-maxima-runtime >=10.9.post13,<10.10" not in dependencies


def test_runtime_companion_wheels_declare_copied_package_data():
    for package, package_data in RUNTIME_PACKAGE_DATA.items():
        pyproject = _pyproject(package)
        setuptools = pyproject["tool"]["setuptools"]

        assert setuptools["include-package-data"] is True
        assert setuptools["package-data"] == package_data


def test_maxima_runtime_wheel_excludes_python_bytecode():
    pyproject = _pyproject("sagelite-maxima-runtime")
    setuptools = pyproject["tool"]["setuptools"]

    assert setuptools["exclude-package-data"]["*"] == [
        "__pycache__/*",
        "*.pyc",
        "*.pyo",
    ]


def test_source_bundled_data_companion_wheels_ship_declared_payloads():
    for package, package_data in SOURCE_BUNDLED_DATA_PACKAGE_DATA.items():
        pyproject = _pyproject(package)
        setuptools = pyproject["tool"]["setuptools"]

        assert setuptools["include-package-data"] is True
        assert setuptools["package-data"] == package_data

        package_root = ROOT / "companion-packages" / package / "src"
        for module, patterns in package_data.items():
            module_root = package_root / module
            for pattern in patterns:
                assert any(path.is_file() for path in module_root.glob(pattern)), (
                    f"{package} declares {module}:{pattern} but no payload files "
                    "are present in the source tree"
                )


def test_build_copied_data_companion_wheels_declare_packaged_payloads():
    for package, package_data in BUILD_COPIED_DATA_PACKAGE_DATA.items():
        pyproject = _pyproject(package)
        setuptools = pyproject["tool"]["setuptools"]

        assert setuptools["include-package-data"] is True
        assert setuptools["package-data"] == package_data


def test_companion_wheels_with_package_data_are_classified():
    classified = (
        set(RUNTIME_PACKAGE_DATA)
        | set(SOURCE_BUNDLED_DATA_PACKAGE_DATA)
        | set(BUILD_COPIED_DATA_PACKAGE_DATA)
    )
    declared = set()
    for pyproject_toml in (ROOT / "companion-packages").glob(
        "sagelite-*/pyproject.toml"
    ):
        pyproject = tomllib.loads(pyproject_toml.read_text())
        if pyproject.get("tool", {}).get("setuptools", {}).get("package-data"):
            declared.add(pyproject["project"]["name"])

    assert declared == classified


def test_linux_repair_builds_expected_runtime_companion_wheels():
    repair_script = ROOT / ".github" / "workflows" / "repair-wheel-linux.sh"
    repair_text = repair_script.read_text()

    for package in REPAIR_WORKFLOW_BUILT_RUNTIME_PACKAGES:
        assert f"companion-packages/{package}" in repair_text

    covered = (
        REPAIR_WORKFLOW_BUILT_RUNTIME_PACKAGES
        | REPAIR_WORKFLOW_EXTERNAL_RUNTIME_PACKAGES
    )
    assert set(RUNTIME_PACKAGE_DATA) == covered


def test_companion_workflow_builds_expected_runtime_companion_wheels():
    workflow = ROOT / ".github" / "workflows" / "companion-packages.yml"
    workflow_text = workflow.read_text()

    for package in COMPANION_WORKFLOW_BUILT_RUNTIME_PACKAGES:
        assert f"path: companion-packages/{package}" in workflow_text


def test_companion_workflow_builds_expected_data_companion_wheels():
    workflow = ROOT / ".github" / "workflows" / "companion-packages.yml"
    workflow_text = workflow.read_text()

    for package in COMPANION_WORKFLOW_DATA_PACKAGES:
        assert f"path: companion-packages/{package}" in workflow_text


def test_base_sagelite_installs_standard_data_companion_wheels():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    dependencies = set(pyproject["project"]["dependencies"])

    assert BASE_SAGELITE_DATA_DEPENDENCIES <= dependencies


def test_data_companion_wheels_are_exposed_by_upstream_style_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]

    for extra, requirement in DATA_COMPANION_EXTRA_ALIASES.items():
        assert extras[extra] == [requirement]


def test_base_sagelite_installs_standard_runtime_companion_wheels():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    dependencies = set(pyproject["project"]["dependencies"])

    assert BASE_SAGELITE_STANDARD_RUNTIME_DEPENDENCIES <= dependencies


def test_base_sagelite_companion_dependencies_are_contract_classified():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    dependencies = {
        requirement
        for requirement in pyproject["project"]["dependencies"]
        if requirement.startswith("sagelite-")
    }
    classified = (
        BASE_SAGELITE_DATA_DEPENDENCIES
        | BASE_SAGELITE_STANDARD_RUNTIME_DEPENDENCIES
        | DEFAULT_GAP_PACKAGE_COMPANION_DEPENDENCIES
    )

    assert dependencies == classified


def test_base_sagelite_installs_standard_pypi_runtime_wheels():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    dependencies = set(pyproject["project"]["dependencies"])
    extras = pyproject["project"]["optional-dependencies"]

    assert BASE_SAGELITE_STANDARD_PYPI_RUNTIME_DEPENDENCIES <= dependencies
    assert BASE_SAGELITE_STANDARD_PYPI_RUNTIME_DEPENDENCIES <= set(extras["runtime"])
    assert BASE_SAGELITE_STANDARD_PYPI_RUNTIME_DEPENDENCIES <= set(extras["full"])


def test_cvxpy_solver_runtime_wheels_are_exposed_by_feature_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]

    for feature, requirement in OPTIONAL_CVXPY_SOLVER_RUNTIME_DEPENDENCIES.items():
        assert extras[feature] == [requirement]
        assert requirement in extras["extra"]
        assert requirement in extras["runtime"]
        assert requirement in extras["full"]


def test_base_sagelite_companion_dependencies_are_build_covered():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    workflow_text = (
        (ROOT / ".github" / "workflows" / "companion-packages.yml").read_text()
        + (ROOT / ".github" / "workflows" / "repair-wheel-linux.sh").read_text()
    )
    dependencies = {
        requirement.split()[0]
        for requirement in pyproject["project"]["dependencies"]
        if requirement.startswith("sagelite-")
    }

    for package in dependencies:
        assert (ROOT / "companion-packages" / package).is_dir()
        assert f"companion-packages/{package}" in workflow_text


def test_gap_package_wheels_are_exposed_by_upstream_package_name_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]

    for package, requirements in GAP_PACKAGE_EXTRA_REQUIREMENTS.items():
        assert extras[package] == requirements
        assert extras[f"gap-{package}"] == requirements
        assert extras[f"gap_package_{package}"] == requirements


def test_packaged_gap_companions_are_declared_as_sage_features():
    source = (ROOT / "src" / "sage" / "features" / "gap.py").read_text()

    for package in GAP_PACKAGE_EXTRA_REQUIREMENTS:
        assert f'GapPackage("{package}", spkg=' in source


def test_packaged_gap_companions_are_exercised_by_selftest():
    selftest = (ROOT / "src" / "sage" / "cli" / "selftest.py").read_text()

    assert "GAP_PACKAGE_COMPANIONS = [" in selftest
    assert "def _check_gap_package_runtime(" in selftest

    for package in GAP_PACKAGE_EXTRA_REQUIREMENTS:
        module_name = f"sagelite_gap_package_{package}"
        if package == "gapdoc":
            assert '"GAPDoc package runtime", _check_gapdoc_runtime' in selftest
        else:
            assert f'("{package}", "{module_name}",' in selftest


def test_lrslib_runtime_is_exposed_by_lrs_extra():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-lrslib-runtime >=10.9,<10.10"

    assert extras["lrs"] == [requirement]
    assert extras["lrslib"] == [requirement]


def test_base_sagelite_data_companion_wheels_are_publishable():
    workflow = ROOT / ".github" / "workflows" / "companion-packages.yml"
    workflow_text = workflow.read_text()

    for requirement in BASE_SAGELITE_DATA_DEPENDENCIES:
        package = requirement.split()[0]
        start = workflow_text.index(f"- name: {package}")
        end = workflow_text.find("\n          - name:", start + 1)
        block = workflow_text[start : end if end != -1 else len(workflow_text)]

        assert f"path: companion-packages/{package}" in block
        assert "publish: true" in block


def test_default_gap_package_companion_wheels_are_publishable():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    dependencies = set(pyproject["project"]["dependencies"])
    workflow = ROOT / ".github" / "workflows" / "companion-packages.yml"
    workflow_text = workflow.read_text()

    assert DEFAULT_GAP_PACKAGE_COMPANION_DEPENDENCIES <= dependencies

    for requirement in DEFAULT_GAP_PACKAGE_COMPANION_DEPENDENCIES:
        package = requirement.split()[0]
        start = workflow_text.index(f"- name: {package}")
        end = workflow_text.find("\n          - name:", start + 1)
        block = workflow_text[start : end if end != -1 else len(workflow_text)]

        assert f"path: companion-packages/{package}" in block
        assert "publish: true" in block


def test_base_sagelite_standard_runtime_companion_wheels_are_publishable():
    workflow = ROOT / ".github" / "workflows" / "companion-packages.yml"
    workflow_text = workflow.read_text()
    release_runtime_packages = set(RELEASE_WORKFLOW_SEPARATED_RUNTIME_PACKAGES)

    for requirement in BASE_SAGELITE_STANDARD_RUNTIME_DEPENDENCIES:
        package = requirement.split()[0]
        if f"- name: {package}" not in workflow_text:
            assert package in release_runtime_packages
            continue

        start = workflow_text.index(f"- name: {package}")
        end = workflow_text.find("\n          - name:", start + 1)
        block = workflow_text[start : end if end != -1 else len(workflow_text)]

        assert f"path: companion-packages/{package}" in block
        if "publish: true" not in block:
            assert package in release_runtime_packages


def test_selftest_exercises_standard_feature_runtime_companions():
    selftest = (ROOT / "src" / "sage" / "cli" / "selftest.py").read_text()
    expected = {
        "sagelite-benzene-runtime": (
            "sagelite_benzene",
            "benzene graph generator runtime",
            "_check_benzene_runtime",
        ),
        "sagelite-buckygen-runtime": (
            "sagelite_buckygen",
            "buckygen graph generator runtime",
            "_check_buckygen_runtime",
        ),
        "sagelite-csdp-runtime": (
            "sagelite_csdp",
            "CSDP executable runtime",
            "_check_csdp_runtime",
        ),
        "sagelite-fricas-runtime": (
            "sagelite_fricas",
            "FriCAS executable runtime",
            "_check_fricas_runtime",
        ),
        "sagelite-frobby-runtime": (
            "sagelite_frobby",
            "Frobby executable runtime",
            "_check_frobby_runtime",
        ),
        "sagelite-gap3-runtime": (
            "sagelite_gap3",
            "GAP3 executable runtime",
            "_check_gap3_runtime",
        ),
        "sagelite-giac-runtime": (
            "sagelite_giac",
            "Giac executable runtime",
            "_check_giac_runtime",
        ),
        "sagelite-glucose-runtime": (
            "sagelite_glucose",
            "Glucose executable runtime",
            "_check_glucose_runtime",
        ),
        "sagelite-info-runtime": (
            "sagelite_info",
            "GNU Info executable runtime",
            "_check_info_runtime",
        ),
        "sagelite-kenzo-runtime": (
            "sagelite_kenzo",
            "Kenzo ECL runtime",
            "_check_kenzo_runtime",
        ),
        "sagelite-kissat-runtime": (
            "sagelite_kissat",
            "Kissat executable runtime",
            "_check_kissat_runtime",
        ),
        "sagelite-latte-runtime": (
            "sagelite_latte",
            "LattE executable runtime",
            "_check_latte_runtime",
        ),
        "sagelite-lcalc-runtime": (
            "sagelite_lcalc",
            "lcalc executable runtime",
            "_check_lcalc_runtime",
        ),
        "sagelite-lrslib-runtime": (
            "sagelite_lrslib",
            "lrslib executable runtime",
            "_check_lrslib_runtime",
        ),
        "sagelite-msolve-runtime": (
            "sagelite_msolve",
            "msolve executable runtime",
            "_check_msolve_runtime",
        ),
        "sagelite-planarity-runtime": (
            "sagelite_planarity",
            "planarity executable runtime",
            "_check_planarity_runtime",
        ),
        "sagelite-plantri-runtime": (
            "sagelite_plantri",
            "plantri graph generator runtime",
            "_check_plantri_runtime",
        ),
        "sagelite-qepcad-runtime": (
            "sagelite_qepcad",
            "QEPCAD executable runtime",
            "_check_qepcad_runtime",
        ),
        "sagelite-tides-runtime": (
            "sagelite_tides",
            "TIDES compile-time runtime",
            "_check_tides_runtime",
        ),
        "sagelite-topcom-runtime": (
            "sagelite_topcom",
            "TOPCOM executable runtime",
            "_check_topcom_runtime",
        ),
    }

    for package, (module_name, label, check_name) in expected.items():
        assert f'"{module_name}"' in selftest
        assert f'def {check_name}()' in selftest
        assert f'("{label}", {check_name})' in selftest


def test_static_runtime_companion_wheels_are_publishable():
    workflow = ROOT / ".github" / "workflows" / "companion-packages.yml"
    workflow_text = workflow.read_text()

    for package in PUBLISHABLE_STATIC_RUNTIME_PACKAGES:
        start = workflow_text.index(f"- name: {package}")
        end = workflow_text.find("\n          - name:", start + 1)
        block = workflow_text[start : end if end != -1 else len(workflow_text)]

        assert f"path: companion-packages/{package}" in block
        assert "publish: true" in block


def test_release_workflow_separates_expected_runtime_companion_wheels():
    workflow = ROOT / ".github" / "workflows" / "release.yml"
    workflow_text = workflow.read_text()

    for package, dist_dir in RELEASE_WORKFLOW_SEPARATED_RUNTIME_PACKAGES.items():
        wheel_glob = package.replace("-", "_")

        assert f'mkdir -p {dist_dir}' in workflow_text
        assert f'-name "{wheel_glob}-*.whl"' in workflow_text
        assert f'path: ./{dist_dir}/*.whl' in workflow_text
        assert f'path: {dist_dir}' in workflow_text
        assert f'packages-dir: {dist_dir}/' in workflow_text


def test_release_workflow_smoke_test_installs_sagelite_with_local_companions():
    workflow = ROOT / ".github" / "workflows" / "release.yml"
    workflow_text = workflow.read_text()

    start = workflow_text.index("- name: Smoke test wheel in a fresh virtualenv")
    end = workflow_text.index("- uses: actions/upload-artifact@v4", start)
    block = workflow_text[start:end]

    assert "wheels=(wheelhouse/*.whl)" in block
    assert 'wheels+=("$companion_dist"/*.whl)' in block
    assert 'pip install "${wheels[@]}"' in block
    assert "pip install wheelhouse/*.whl" not in block


def test_release_workflow_verifies_current_maxima_runtime_version():
    workflow = ROOT / ".github" / "workflows" / "release.yml"
    workflow_text = workflow.read_text()
    version = _pyproject("sagelite-maxima-runtime")["project"]["version"]

    assert (
        f"sagelite_maxima_runtime-{version}-py3-none-manylinux_2_28_x86_64.whl"
        in workflow_text
    )
    assert (
        f"sagelite_maxima_runtime-{version}-py3-none-manylinux_2_28_aarch64.whl"
        in workflow_text
    )


def test_release_workflow_requires_standard_native_meson_options():
    workflow = ROOT / ".github" / "workflows" / "release.yml"
    workflow_text = workflow.read_text()

    for option in RELEASE_REQUIRED_MESON_OPTIONS:
        assert f"setup-args=-D{option}=enabled" in workflow_text


def test_sagelite_source_build_defaults_optional_native_meson_options_to_auto():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    setup_args = set(pyproject["tool"]["meson-python"]["args"]["setup"])

    assert "-Dbuild-docs=false" in setup_args
    for option in RELEASE_REQUIRED_MESON_OPTIONS:
        assert f"-D{option}=auto" in setup_args


def test_release_workflow_verifies_standard_native_extensions():
    workflow = ROOT / ".github" / "workflows" / "release.yml"
    workflow_text = workflow.read_text()

    assert "tools/sagelite_native_wheel_catalog.py" in workflow_text
    assert 'catalog["required_native_extension_prefixes"]' in workflow_text
    assert "Missing required native extensions" in workflow_text
    assert "sage/libs/coxeter3/coxeter." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/libs/braiding." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/libs/homfly." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/graphs/bliss." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/graphs/cliquer." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/graphs/planarity." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/libs/ntl/error." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/rings/polynomial/pbori/pbori." in (
        RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    )


def test_release_workflow_verifies_standard_native_libraries():
    workflow = ROOT / ".github" / "workflows" / "release.yml"
    workflow_text = workflow.read_text()

    assert "Missing required bundled native libraries" in workflow_text
    assert 'catalog["required_native_library_prefixes"]' in workflow_text
    assert "libbrial" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libbrial_groebner" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libbraiding" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libcoxeter3" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libec-" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libec" not in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libhomfly" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libbliss" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libcliquer" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libplanarity" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES


def test_pari_data_wheel_declares_copied_runtime_data():
    pyproject = _pyproject("sagelite-pari-data")
    package_init = (
        ROOT
        / "companion-packages"
        / "sagelite-pari-data"
        / "src"
        / "sagelite_pari_data"
        / "__init__.py"
    ).read_text()

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "pari": "sagelite_pari_data:sage_data_path",
    }
    assert "def sage_data_path()" in package_init
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert (
        pyproject["tool"]["setuptools"]["package-data"]
        == BUILD_COPIED_DATA_PACKAGE_DATA["sagelite-pari-data"]
    )

    for script_dir in ("buzzard", "dokchitser", "simon"):
        assert (ROOT / "src" / "sage" / "ext_data" / "pari" / script_dir).is_dir()


def test_pari_data_wheel_runtime_helper_points_at_bundled_data():
    sys.path.insert(
        0, str(ROOT / "companion-packages" / "sagelite-pari-data" / "src")
    )
    try:
        from sagelite_pari_data.runtime import pari_data_dir
    finally:
        sys.path.pop(0)

    assert Path(pari_data_dir()).parts[-2:] == ("data", "pari")


def test_pari_data_wheel_is_exposed_by_sagelite_data_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-pari-data >=10.9,<10.10"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["pari-data"] == [requirement]
    assert extras["pari-seadata-small"] == [requirement]
    assert extras["pari_seadata_small"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_pari_data_wheel_payload_is_reflected_in_external_host_requires():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    host_requires = pyproject["external"]["host-requires"]

    assert "pkg:generic/pari-elldata" in host_requires
    assert "pkg:generic/pari-galdata" in host_requires
    assert "pkg:generic/pari-galpol" in host_requires
    assert "pkg:generic/pari-nftables" in host_requires
    assert "pkg:generic/pari-seadata" in host_requires
    assert "pkg:generic/pari-seadata-small" in host_requires


def test_pari_data_workflows_build_complete_payload():
    companion_workflow = ROOT / ".github" / "workflows" / "companion-packages.yml"
    companion_text = companion_workflow.read_text()
    smoke_test = ROOT / ".github" / "workflows" / "smoke-test-sagelite-companion.py"
    smoke_test_text = smoke_test.read_text()
    release_workflow = ROOT / ".github" / "workflows" / "release.yml"
    release_text = release_workflow.read_text()

    assert "SAGELITE_PARI_NFTABLES_TARBALL" in companion_text
    assert "download pari_nftables" in companion_text
    assert 'os.path.join(data_dir, "nftables")' in smoke_test_text

    for spkg in (
        "pari_elldata",
        "pari_galdata",
        "pari_galpol",
        "pari_nftables",
        "pari_seadata",
    ):
        assert spkg in release_text


def test_tides_runtime_wheel_declares_copied_runtime_files():
    pyproject = _pyproject("sagelite-tides-runtime")

    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"]["sagelite_tides"] == [
        "data/include/*",
        "data/lib/*",
    ]


def test_tides_runtime_wheel_helper_points_at_bundled_files():
    sys.path.insert(
        0, str(ROOT / "companion-packages" / "sagelite-tides-runtime" / "src")
    )
    try:
        from sagelite_tides.runtime import include_dir, library_path
    finally:
        sys.path.pop(0)

    assert Path(include_dir()).parts[-2:] == ("data", "include")
    assert Path(library_path()).parts[-3:] == ("data", "lib", "libTIDES.a")


def test_tides_runtime_wheel_is_exposed_by_sagelite_runtime_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-tides-runtime >=10.9,<10.10"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["tides"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_sirocco_runtime_wheel_helper_points_at_bundled_files():
    sys.path.insert(
        0, str(ROOT / "companion-packages" / "sagelite-sirocco-runtime" / "src")
    )
    try:
        from sagelite_sirocco.runtime import include_dir, library_dir, library_path
    finally:
        sys.path.pop(0)

    assert Path(include_dir()).parts[-2:] == ("data", "include")
    assert Path(library_dir()).parts[-2:] == ("data", "lib")
    assert Path(library_path()).parts[-3:-1] == ("data", "lib")
    assert Path(library_path()).name.startswith("libsirocco")


def test_sirocco_runtime_wheel_is_exposed_by_sagelite_runtime_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-sirocco-runtime >=10.9,<10.10"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["sirocco"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_fplll_data_wheel_declares_copied_strategy_files():
    pyproject = _pyproject("sagelite-fplll-data")

    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"]["sagelite_fplll_data"] == [
        "data/strategies/*.json",
    ]


def test_fplll_data_wheel_helper_points_at_bundled_default_strategy():
    sys.path.insert(
        0, str(ROOT / "companion-packages" / "sagelite-fplll-data" / "src")
    )
    try:
        from sagelite_fplll_data.runtime import default_strategy, strategies_dir
    finally:
        sys.path.pop(0)

    assert Path(strategies_dir()).parts[-2:] == ("data", "strategies")
    assert Path(default_strategy()).parts[-3:] == (
        "data",
        "strategies",
        "default.json",
    )


def test_fplll_data_wheel_is_exposed_by_sagelite_dependencies_and_runtime_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    requirement = "sagelite-fplll-data >=10.9,<10.10"
    assert requirement not in pyproject["project"]["dependencies"]

    extras = pyproject["project"]["optional-dependencies"]
    assert extras["fplll-data"] == [requirement]
    assert extras["fplll_data"] == [requirement]
    assert requirement in extras["all-needed-extras"]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_info_runtime_wheel_declares_copied_runtime_files():
    pyproject = _pyproject("sagelite-info-runtime")

    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"]["sagelite_info"] == [
        "data/bin/*",
        "data/lib/*",
        "data/share/info/**/*",
    ]


def test_info_runtime_wheel_helper_points_at_bundled_files():
    sys.path.insert(
        0, str(ROOT / "companion-packages" / "sagelite-info-runtime" / "src")
    )
    try:
        from sagelite_info.runtime import executable_path, info_dir
    finally:
        sys.path.pop(0)

    assert Path(executable_path()).parts[-3:] == ("data", "bin", "info")
    assert Path(info_dir()).parts[-3:] == ("data", "share", "info")


def test_info_runtime_wheel_is_exposed_by_sagelite_runtime_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-info-runtime >=10.9,<10.10"

    assert extras["info"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_info_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-info-runtime")

    assert pyproject["project"]["scripts"] == {
        "info": "sagelite_info.runtime:info",
    }


def test_ecl_runtime_wheel_is_exposed_by_sagelite_runtime_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-ecl-runtime >=10.9,<10.10"

    assert extras["ecl"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_ecl_runtime_declares_console_scripts():
    pyproject = _pyproject("sagelite-ecl-runtime")

    assert pyproject["project"]["scripts"] == {
        "ecl": "sagelite_ecl.runtime:ecl",
        "ecl-config": "sagelite_ecl.runtime:ecl_config",
    }


def test_linux_repair_builds_pari_data_companion_wheel():
    repair_script = ROOT / ".github" / "workflows" / "repair-wheel-linux.sh"
    repair_text = repair_script.read_text()

    assert "companion-packages/sagelite-pari-data" in repair_text
    assert "build_pari_data_companion" in repair_text
    assert "SAGELITE_PARI_DATA_DIR" in repair_text


def test_linux_repair_builds_lie_runtime_companion_wheel():
    repair_script = ROOT / ".github" / "workflows" / "repair-wheel-linux.sh"
    repair_text = repair_script.read_text()

    assert "companion-packages/sagelite-lie-runtime" in repair_text
    assert "build_lie_runtime_companion" in repair_text
    assert "SAGELITE_LIE_BINDIR" in repair_text
    assert "SAGELITE_LIE_INFO_DIR" in repair_text


def test_linux_repair_builds_tides_runtime_companion_wheel():
    repair_script = ROOT / ".github" / "workflows" / "repair-wheel-linux.sh"
    repair_text = repair_script.read_text()

    assert "companion-packages/sagelite-tides-runtime" in repair_text
    assert "build_tides_runtime_companion" in repair_text
    assert "SAGELITE_TIDES_PREFIX" in repair_text


def test_companion_workflow_installs_available_pari_data_payloads():
    workflow = ROOT / ".github" / "workflows" / "companion-packages.yml"
    workflow_text = workflow.read_text()

    assert (
        "apt_packages: pari-elldata pari-galdata pari-galpol pari-seadata"
        in workflow_text
    )


def test_d3js_runtime_registers_static_data_path():
    pyproject = _pyproject("sagelite-d3js-runtime")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "d3js": "sagelite_d3js_runtime:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["package-data"]["sagelite_d3js_runtime"] == [
        "data/d3js/**/*",
    ]


def test_mathjax_runtime_registers_static_data_path():
    pyproject = _pyproject("sagelite-mathjax-runtime")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "mathjax": "sagelite_mathjax_runtime:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_mathjax_runtime"
    ] == [
        "data/mathjax/**/*",
    ]


def test_threejs_runtime_registers_static_data_path():
    pyproject = _pyproject("sagelite-threejs-runtime")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "threejs_sage": "sagelite_threejs_runtime:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_threejs_runtime"
    ] == [
        "data/threejs-sage/**/*",
    ]


def test_jmol_runtime_registers_static_data_path_and_script():
    pyproject = _pyproject("sagelite-jmol-runtime")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "jmol": "sagelite_jmol_runtime:sage_data_path",
    }
    assert pyproject["project"]["scripts"] == {
        "jmol": "sagelite_jmol_runtime.runtime:jmol",
    }
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_jmol_runtime"
    ] == [
        "data/jmol/**/*",
    ]


def test_jmol_runtime_helpers_point_at_bundled_files():
    sys.path.insert(
        0, str(ROOT / "companion-packages" / "sagelite-jmol-runtime" / "src")
    )
    try:
        import sagelite_jmol_runtime
        from sagelite_jmol_runtime import runtime
    finally:
        sys.path.pop(0)

    assert Path(sagelite_jmol_runtime.sage_data_path()).parts[-1:] == ("data",)
    assert Path(sagelite_jmol_runtime.jmol_path()).parts[-2:] == ("data", "jmol")
    assert Path(sagelite_jmol_runtime.jmol_data_jar_path()).parts[-3:] == (
        "data",
        "jmol",
        "JmolData.jar",
    )
    assert Path(runtime.jmol_dir()).parts[-2:] == ("data", "jmol")
    assert Path(runtime.jmol_jar_path()).parts[-3:] == ("data", "jmol", "Jmol.jar")
    assert Path(runtime.jmol_data_jar_path()).parts[-3:] == (
        "data",
        "jmol",
        "JmolData.jar",
    )


def test_cremona_ellcurve_database_registers_data_path():
    pyproject = _pyproject("sagelite-database-cremona-ellcurve")
    setup_py = (
        ROOT
        / "companion-packages"
        / "sagelite-database-cremona-ellcurve"
        / "setup.py"
    ).read_text()
    package_init = (
        ROOT
        / "companion-packages"
        / "sagelite-database-cremona-ellcurve"
        / "src"
        / "sagelite_database_cremona_ellcurve"
        / "__init__.py"
    ).read_text()

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "cremona": "sagelite_database_cremona_ellcurve:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_cremona_ellcurve"
    ] == [
        "data/cremona/cremona.db",
    ]
    assert "SAGELITE_CREMONA_ELLCURVE_DB" in setup_py
    assert "local\" / \"share\" / \"cremona" in setup_py
    assert '"sdist": sdist' in setup_py
    assert "def cremona_ellcurve_path()" in package_init


def test_cremona_ellcurve_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-cremona-ellcurve >=10.9,<10.10"

    assert requirement not in pyproject["project"]["dependencies"]
    assert extras["cremona-ellcurve"] == [requirement]
    assert requirement not in extras["databases"]
    assert requirement not in extras["full"]


def test_cremona_mini_database_registers_data_path():
    pyproject = _pyproject("sagelite-database-cremona-mini")
    setup_py = (
        ROOT / "companion-packages" / "sagelite-database-cremona-mini" / "setup.py"
    ).read_text()
    package_init = (
        ROOT
        / "companion-packages"
        / "sagelite-database-cremona-mini"
        / "src"
        / "sagelite_database_cremona_mini"
        / "__init__.py"
    ).read_text()

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "cremona": "sagelite_database_cremona_mini:cremona_data_path",
        "cremona_mini": "sagelite_database_cremona_mini:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_cremona_mini"
    ] == [
        "data/cremona/cremona_mini.db",
    ]
    assert "SAGELITE_CREMONA_MINI_DB" in setup_py
    assert "local\" / \"share\" / \"cremona" in setup_py
    assert "PACKAGE_DATA_FILE" in setup_py
    assert "def cremona_data_path()" in package_init


def test_cremona_mini_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-cremona-mini >=10.9.post1,<10.10"

    assert extras["cremona"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_kohel_database_wheel_declares_and_copies_polynomial_data():
    pyproject = _pyproject("sagelite-database-kohel")
    setup_py = (
        ROOT / "companion-packages" / "sagelite-database-kohel" / "setup.py"
    ).read_text()

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "kohel": "sagelite_database_kohel:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_kohel"
    ] == [
        "data/kohel/**/*",
    ]
    assert "SAGELITE_KOHEL_DATA_DIR" in setup_py
    assert "local\" / \"share\" / \"kohel" in setup_py
    assert "PolMod" in setup_py
    assert "PolHeeg" in setup_py
    assert "BUNDLED_SOURCE" in setup_py


def test_kohel_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-kohel >=10.9,<10.10"

    assert extras["kohel"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_ellcurves_database_wheel_declares_and_copies_rank_data():
    pyproject = _pyproject("sagelite-database-ellcurves")
    setup_py = (
        ROOT / "companion-packages" / "sagelite-database-ellcurves" / "setup.py"
    ).read_text()

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "ellcurves": "sagelite_database_ellcurves:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_ellcurves"
    ] == [
        "data/ellcurves/rank*",
    ]
    assert "SAGELITE_ELLCURVES_DATA_DIR" in setup_py
    assert "local\" / \"share\" / \"ellcurves" in setup_py
    assert "PACKAGE_DATA_DIR" in setup_py


def test_graphs_database_wheel_declares_packaged_data():
    pyproject = _pyproject("sagelite-database-graphs")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "graphs": "sagelite_database_graphs:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_graphs"
    ] == [
        "data/graphs/brouwer_srg_database.json",
        "data/graphs/graphs.db",
        "data/graphs/isgci_sage.xml",
        "data/graphs/smallgraphs.txt",
    ]


def test_graphs_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-graphs >=10.9,<10.10"

    assert extras["graphs"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_jones_numfield_database_registers_data_path():
    pyproject = _pyproject("sagelite-database-jones-numfield")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "jones": "sagelite_database_jones_numfield:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_jones_numfield"
    ] == [
        "data/jones/jones.sobj",
    ]


def test_jones_numfield_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-jones-numfield >=10.9,<10.10"

    assert extras["jones-numfield"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_reflexive_polytopes_database_wheel_declares_packaged_data():
    pyproject = _pyproject("sagelite-database-polytopes")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "reflexive_polytopes": "sagelite_database_polytopes:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_polytopes"
    ] == [
        "data/reflexive_polytopes/**/*",
    ]


def test_reflexive_polytopes_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-polytopes >=10.9,<10.10"

    assert extras["polytopes"] == [requirement]
    assert extras["database-polytopes"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_sloane_database_registers_data_path():
    pyproject = _pyproject("sagelite-database-sloane")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "sloane": "sagelite_database_sloane:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_sloane"
    ] == [
        "data/sloane/sloane-oeis.bz2",
        "data/sloane/sloane-names.bz2",
    ]


def test_sloane_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-sloane >=10.9,<10.10"

    assert extras["sloane"] == [requirement]
    assert extras["sloane-database"] == [requirement]
    assert extras["database-sloane"] == [requirement]
    assert requirement not in extras["databases"]
    assert requirement not in extras["full"]


def test_mutation_class_database_registers_data_path():
    pyproject = _pyproject("sagelite-database-mutation-class")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "cluster_algebra_quiver": "sagelite_database_mutation_class:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_mutation_class"
    ] == [
        "data/cluster_algebra_quiver/mutation_classes_*.dig6",
    ]


def test_mutation_class_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-mutation-class >=10.9,<10.10"

    assert extras["mutation-class"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_odlyzko_zeta_database_wheel_declares_packaged_data():
    pyproject = _pyproject("sagelite-database-odlyzko-zeta")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "odlyzko": "sagelite_database_odlyzko_zeta:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_odlyzko_zeta"
    ] == [
        "data/odlyzko/zeros.sobj",
    ]


def test_odlyzko_zeta_database_can_build_zeros_sobj_without_importing_sage():
    setup_py = (
        ROOT / "companion-packages" / "sagelite-database-odlyzko-zeta" / "setup.py"
    )
    setup_text = setup_py.read_text()

    assert "import pickle" in setup_text
    assert "import zlib" in setup_text
    assert "pickle.dumps(zeros, protocol=2)" in setup_text
    assert "from sage.all import save" not in setup_text


def test_odlyzko_zeta_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-odlyzko-zeta >=10.9,<10.10"

    assert extras["odlyzko-zeta"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_symbolic_data_database_wheel_declares_packaged_data():
    pyproject = _pyproject("sagelite-database-symbolic-data")
    setup_py = (
        ROOT / "companion-packages" / "sagelite-database-symbolic-data" / "setup.py"
    ).read_text()

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "symbolic_data": "sagelite_database_symbolic_data:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_symbolic_data"
    ] == [
        "data/symbolic_data/COPYING",
        "data/symbolic_data/Data/**/*",
    ]
    assert "SAGELITE_SYMBOLIC_DATA_DIR" in setup_py
    assert "local\" / \"share\" / \"symbolic_data" in setup_py
    assert "Data\" / \"XMLResources" in setup_py


def test_symbolic_data_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-symbolic-data >=10.9,<10.10"

    assert extras["symbolic-data"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_conway_polynomials_pypi_database_is_core_sagelite_dependency():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    requirement = "conway-polynomials >=0.8"

    assert requirement in pyproject["project"]["dependencies"]
    assert pyproject["project"]["optional-dependencies"]["conway-polynomials"] == [
        requirement
    ]
    assert pyproject["project"]["optional-dependencies"]["conway_polynomials"] == [
        requirement
    ]
    assert requirement in pyproject["project"]["optional-dependencies"]["databases"]
    assert requirement in pyproject["project"]["optional-dependencies"]["full"]


def test_lrcalc_pypi_library_is_core_sagelite_dependency():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    requirement = 'lrcalc ~=2.1; sys_platform != "win32"'
    extras = pyproject["project"]["optional-dependencies"]

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["lrcalc"] == [requirement]
    assert extras["lrcalc-python"] == [requirement]
    assert extras["lrcalc_python"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_pyparsing_pypi_library_is_core_sagelite_dependency():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    requirement = "pyparsing >=3.2.3"

    assert requirement in pyproject["project"]["dependencies"]
    assert pyproject["project"]["optional-dependencies"]["pyparsing"] == [
        requirement
    ]


def test_elliptic_curves_standard_database_extra_installs_split_wheels():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirements = [
        "sagelite-database-cremona-mini >=10.9.post1,<10.10",
        "sagelite-database-ellcurves >=10.9,<10.10",
    ]

    assert extras["elliptic-curves"] == requirements
    assert extras["elliptic_curves"] == requirements


def test_cubic_hecke_pypi_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "database-cubic-hecke ==2022.4.4"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["cubic-hecke"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_knotinfo_pypi_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "database-knotinfo >=2026.3.1"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["knotinfo"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_matroid_pypi_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "matroid-database ==0.3"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["matroids"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_pycryptosat_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = (
        "pycryptosat; python_version < '3.13' and "
        "(sys_platform == 'darwin' or "
        "(sys_platform == 'linux' and platform_machine == 'x86_64'))"
    )

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["pycryptosat"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_pynormaliz_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = 'pynormaliz >=2.18; sys_platform != "win32"'

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["pynormaliz"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_khoca_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "khoca >=1.4"
    py_requirement = "py >=1.11,<2"

    assert requirement in pyproject["project"]["dependencies"]
    assert py_requirement in pyproject["project"]["dependencies"]
    assert extras["khoca"] == [requirement, py_requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]
    assert py_requirement in extras["extra"]
    assert py_requirement in extras["runtime"]
    assert py_requirement in extras["full"]


def test_mathics_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "Mathics3 >=10.0.1; python_version < '3.14'"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["mathics"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_dot2tex_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "dot2tex >=2.11.3"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["dot2tex"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_phitigra_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "phitigra >=0.2.6"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["phitigra"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_regina_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "regina >=7.4.1"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["regina"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_symengine_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "symengine >= 0.6.1"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["symengine"] == [requirement]
    assert extras["symengine_py"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_imageio_ffmpeg_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "imageio-ffmpeg >=0.6.0"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["ffmpeg"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_igraph_pypi_runtime_is_core_sagelite_dependency():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "igraph"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["igraph"] == [requirement]
    assert extras["python_igraph"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_graphviz_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-graphviz-runtime >=10.9.post1,<10.10"

    assert extras["graphviz"] == [requirement]
    assert extras["dot"] == [requirement]
    assert extras["neato"] == [requirement]
    assert extras["twopi"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_pypandoc_binary_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "pypandoc-binary >=1.17"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["pandoc"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_jupyter_jsmol_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "jupyter-jsmol >=2022.1.0"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["jupyter-jsmol"] == [requirement]
    assert extras["jupyter_jsmol"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_upstream_feature_name_aliases_are_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]

    aliases = {
        "cunningham_tables": "cunningham-tables",
        "database_cremona_ellcurve": "database-cremona-ellcurve",
        "database_cubic_hecke": "database-cubic-hecke",
        "database_graphs": "database-graphs",
        "database_jones_numfield": "database-jones-numfield",
        "database_knotinfo": "database-knotinfo",
        "database_kohel": "database-kohel",
        "database_mutation_class": "database-mutation-class",
        "database_odlyzko_zeta": "database-odlyzko-zeta",
        "database_sloane": "database-sloane",
        "database_stein_watkins": "database-stein-watkins",
        "database_stein_watkins_mini": "database-stein-watkins-mini",
        "database_symbolic_data": "database-symbolic-data",
        "jupyter_jsmol": "jupyter-jsmol",
        "latte_int": "latte",
        "lrcalc_python": "lrcalc",
        "matroid_database": "matroid-database",
        "polytopes_db": "polytopes-db",
        "polytopes_db_4d": "polytopes-db-4d",
        "python_igraph": "igraph",
        "rpy2": "R",
        "sloane_database": "sloane-database",
        "symengine_py": "symengine",
    }
    for alias, canonical in aliases.items():
        assert extras[alias] == extras[canonical]

    for alias in ("pycosat", "sage_numerical_backends_coin"):
        assert extras[alias][0] in extras["extra"]
        assert extras[alias][0] in extras["full"]


def test_buckygen_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-buckygen-runtime >=10.9,<10.10"

    assert extras["buckygen"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_gap_runtime_requires_gap4_roots_and_keeps_package_roots(
    monkeypatch, tmp_path
):
    setup_text = (
        ROOT / "companion-packages" / "sagelite-gap-runtime" / "setup.py"
    ).read_text()
    runtime = _load_gap_runtime_module()
    repair_text = (ROOT / ".github" / "workflows" / "repair-wheel-linux.sh").read_text()
    gap_builder = repair_text[
        repair_text.index("build_gap_runtime_companion()") :
        repair_text.index("\nbuild_gap3_runtime_companion()")
    ]

    core_root = tmp_path / "data" / "gap0"
    gap3_root = tmp_path / "data" / "gap1"
    package_root = tmp_path / "data" / "gap2"
    (core_root / "lib").mkdir(parents=True)
    for name in ("init.g", "system.g", "package.gi"):
        (core_root / "lib" / name).write_text("gap4 marker\n", encoding="utf-8")
    (gap3_root / "lib").mkdir(parents=True)
    (gap3_root / "lib" / "init.g").write_text("gap3 marker\n", encoding="utf-8")
    _gap_package(package_root, "example")

    monkeypatch.setattr(runtime, "files", lambda package: tmp_path)

    assert runtime.gap_root_paths() == f"{core_root};{package_root}"
    assert '"system.g"' in setup_text
    assert '"package.gi"' in setup_text
    assert "GAP 4 roots" in setup_text
    assert "lib/system.g" in gap_builder
    assert "lib/package.gi" in gap_builder
    assert "*/pkg/*/PackageInfo.g" not in gap_builder


def test_gap_grape_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-grape")

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "grape": "sagelite_gap_package_grape.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_grape"
    ] == [
        "data/gaproot/pkg/**/*",
    ]


def test_gap_grape_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    grape = "sagelite-gap-package-grape >=10.9,<10.10"

    assert extras["gap-grape"] == [gap_runtime, grape]
    assert extras["gap_package_grape"] == [gap_runtime, grape]
    assert grape not in extras["runtime"]
    assert grape not in extras["full"]


def test_gap_atlasrep_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-atlasrep")

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "atlasrep": "sagelite_gap_package_atlasrep.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_atlasrep"
    ] == [
        "data/gaproot/pkg/**/*",
    ]


def test_gap_atlasrep_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    atlasrep = "sagelite-gap-package-atlasrep >=10.9,<10.10"

    assert extras["gap-atlasrep"] == [gap_runtime, atlasrep]
    assert extras["gap_package_atlasrep"] == [gap_runtime, atlasrep]
    assert atlasrep not in extras["runtime"]
    assert atlasrep not in extras["full"]


def test_gap_ctbllib_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-ctbllib")

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "ctbllib": "sagelite_gap_package_ctbllib.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_ctbllib"
    ] == [
        "data/gaproot/pkg/**/*",
    ]


def test_gap_ctbllib_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    ctbllib = "sagelite-gap-package-ctbllib >=10.9,<10.10"

    assert extras["gap-ctbllib"] == [gap_runtime, ctbllib]
    assert extras["gap_package_ctbllib"] == [gap_runtime, ctbllib]
    assert ctbllib not in extras["runtime"]
    assert ctbllib not in extras["full"]


def test_gap_design_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-design")

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "design": "sagelite_gap_package_design.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_design"
    ] == [
        "data/gaproot/pkg/**/*",
    ]


def test_gap_design_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    design = "sagelite-gap-package-design >=10.9,<10.10"

    assert extras["gap-design"] == [gap_runtime, design]
    assert extras["gap_package_design"] == [gap_runtime, design]
    assert design not in extras["runtime"]
    assert design not in extras["full"]


def test_gap_gapdoc_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-gapdoc")

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "gapdoc": "sagelite_gap_package_gapdoc.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_gapdoc"
    ] == [
        "data/gaproot/pkg/**/*",
    ]


def test_gap_gapdoc_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    gapdoc = "sagelite-gap-package-gapdoc >=10.9,<10.10"

    assert extras["gap-gapdoc"] == [gap_runtime, gapdoc]
    assert extras["gap_package_gapdoc"] == [gap_runtime, gapdoc]
    assert gapdoc not in extras["runtime"]
    assert gapdoc not in extras["full"]


def test_gap_guava_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-guava")
    setup_py = (
        ROOT / "companion-packages" / "sagelite-gap-package-guava" / "setup.py"
    ).read_text()
    runtime_py = (
        ROOT
        / "companion-packages"
        / "sagelite-gap-package-guava"
        / "src"
        / "sagelite_gap_package_guava"
        / "runtime.py"
    ).read_text()

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "guava": "sagelite_gap_package_guava.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_guava"
    ] == [
        "data/gaproot/pkg/**/*",
    ]
    assert "GUAVA_PROGRAM_NAMES = (\"wtdist\",)" in setup_py
    assert "SAGELITE_GAP_GUAVA_PROGRAM_DIR" in setup_py
    assert "_copy_guava_programs(source, target)" in setup_py
    assert 'joinpath("bin", "wtdist")' in runtime_py


def _load_guava_runtime_module():
    runtime_path = (
        ROOT
        / "companion-packages"
        / "sagelite-gap-package-guava"
        / "src"
        / "sagelite_gap_package_guava"
        / "runtime.py"
    )
    spec = importlib.util.spec_from_file_location(
        "test_sagelite_gap_package_guava_runtime",
        runtime_path,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _gap_package(root: Path, name: str) -> Path:
    package = root / "pkg" / name
    package.mkdir(parents=True)
    (package / "PackageInfo.g").write_text("PackageInfo := rec();\n", encoding="utf-8")
    return package


def test_gap_guava_runtime_requires_complete_package_payload(monkeypatch, tmp_path):
    runtime = _load_guava_runtime_module()
    gaproot = tmp_path / "data" / "gaproot"
    guava = _gap_package(gaproot, "guava-3.17")
    _gap_package(gaproot, "sonata-2.9")
    wtdist = guava / "bin" / "wtdist"
    wtdist.parent.mkdir()
    wtdist.write_text("#!/bin/sh\n", encoding="utf-8")
    wtdist.chmod(0o755)

    monkeypatch.setattr(runtime, "files", lambda package: tmp_path)

    assert runtime.gap_root_paths() == str(gaproot)


@pytest.mark.parametrize("missing", ["guava", "sonata", "wtdist", "executable"])
def test_gap_guava_runtime_rejects_incomplete_package_payload(
    monkeypatch, tmp_path, missing
):
    runtime = _load_guava_runtime_module()
    gaproot = tmp_path / "data" / "gaproot"
    if missing != "guava":
        guava = _gap_package(gaproot, "guava-3.17")
    if missing != "sonata":
        _gap_package(gaproot, "sonata-2.9")
    if missing not in {"guava", "wtdist"}:
        wtdist = guava / "bin" / "wtdist"
        wtdist.parent.mkdir()
        wtdist.write_text("#!/bin/sh\n", encoding="utf-8")
        if missing != "executable":
            wtdist.chmod(0o755)

    monkeypatch.setattr(runtime, "files", lambda package: tmp_path)

    assert runtime.gap_root_paths() == ""


def test_gap_guava_smoke_test_requires_wtdist_program():
    smoke_test = ROOT / ".github" / "workflows" / "smoke-test-sagelite-companion.py"
    smoke_text = smoke_test.read_text()

    assert 'os.path.join(guava_dirs[0], "bin", "wtdist")' in smoke_text
    assert "os.X_OK" in smoke_text
    assert 'libgap.LoadPackage("guava")' in smoke_text
    assert 'libgap.DirectoriesPackagePrograms("guava")' in smoke_text
    assert "weight_distribution(" in smoke_text
    assert 'algorithm="leon"' in smoke_text
    assert "skipping Sage GUAVA smoke: sage.all is not installed" in smoke_text


def test_gap_guava_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    guava = "sagelite-gap-package-guava >=10.9,<10.10"

    assert extras["gap-guava"] == [gap_runtime, guava]
    assert extras["gap_package_guava"] == [gap_runtime, guava]
    assert guava not in extras["runtime"]
    assert guava not in extras["full"]


def test_gap_polycyclic_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-polycyclic")

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "polycyclic": "sagelite_gap_package_polycyclic.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_polycyclic"
    ] == [
        "data/gaproot/pkg/**/*",
    ]


def test_gap_polycyclic_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    polycyclic = "sagelite-gap-package-polycyclic >=10.9,<10.10"

    assert extras["gap-polycyclic"] == [gap_runtime, polycyclic]
    assert extras["gap_package_polycyclic"] == [gap_runtime, polycyclic]
    assert polycyclic not in extras["runtime"]
    assert polycyclic not in extras["full"]


def test_gap_primgrp_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-primgrp")

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "primgrp": "sagelite_gap_package_primgrp.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_primgrp"
    ] == [
        "data/gaproot/pkg/**/*",
    ]


def test_gap_primgrp_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    primgrp = "sagelite-gap-package-primgrp >=10.9,<10.10"

    assert extras["gap-primgrp"] == [gap_runtime, primgrp]
    assert extras["gap_package_primgrp"] == [gap_runtime, primgrp]
    assert primgrp not in extras["runtime"]
    assert primgrp not in extras["full"]


def test_gap_repsn_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-repsn")

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "repsn": "sagelite_gap_package_repsn.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_repsn"
    ] == [
        "data/gaproot/pkg/**/*",
    ]


def test_gap_repsn_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    repsn = "sagelite-gap-package-repsn >=10.9,<10.10"

    assert extras["gap-repsn"] == [gap_runtime, repsn]
    assert extras["gap_package_repsn"] == [gap_runtime, repsn]
    assert repsn not in extras["runtime"]
    assert repsn not in extras["full"]


def test_gap_smallgrp_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-smallgrp")

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "smallgrp": "sagelite_gap_package_smallgrp.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_smallgrp"
    ] == [
        "data/gaproot/pkg/**/*",
    ]


def test_gap_smallgrp_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    smallgrp = "sagelite-gap-package-smallgrp >=10.9,<10.10"

    assert extras["gap-smallgrp"] == [gap_runtime, smallgrp]
    assert extras["gap_package_smallgrp"] == [gap_runtime, smallgrp]
    assert smallgrp not in extras["runtime"]
    assert smallgrp not in extras["full"]


def test_gap_tomlib_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-tomlib")

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "tomlib": "sagelite_gap_package_tomlib.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_tomlib"
    ] == [
        "data/gaproot/pkg/**/*",
    ]


def test_gap_tomlib_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    tomlib = "sagelite-gap-package-tomlib >=10.9,<10.10"

    assert extras["gap-tomlib"] == [gap_runtime, tomlib]
    assert extras["gap_package_tomlib"] == [gap_runtime, tomlib]
    assert tomlib not in extras["runtime"]
    assert tomlib not in extras["full"]


def test_gap_transgrp_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-transgrp")

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "transgrp": "sagelite_gap_package_transgrp.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_transgrp"
    ] == [
        "data/gaproot/pkg/**/*",
    ]


def test_gap_transgrp_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    transgrp = "sagelite-gap-package-transgrp >=10.9,<10.10"

    assert extras["gap-transgrp"] == [gap_runtime, transgrp]
    assert extras["gap_package_transgrp"] == [gap_runtime, transgrp]
    assert transgrp not in extras["runtime"]
    assert transgrp not in extras["full"]


def test_gap_packages_extra_matches_available_gap_package_companions():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    available_gap_packages = [
        "sagelite-gap-package-atlasrep >=10.9,<10.10",
        "sagelite-gap-package-ctbllib >=10.9,<10.10",
        "sagelite-gap-package-design >=10.9,<10.10",
        "sagelite-gap-package-gapdoc >=10.9,<10.10",
        "sagelite-gap-package-grape >=10.9,<10.10",
        "sagelite-gap-package-guava >=10.9,<10.10",
        "sagelite-gap-package-hap >=10.9,<10.10",
        "sagelite-gap-package-polenta >=10.9,<10.10",
        "sagelite-gap-package-polycyclic >=10.9,<10.10",
        "sagelite-gap-package-primgrp >=10.9,<10.10",
        "sagelite-gap-package-qpa >=10.9,<10.10",
        "sagelite-gap-package-quagroup >=10.9,<10.10",
        "sagelite-gap-package-repsn >=10.9,<10.10",
        "sagelite-gap-package-smallgrp >=10.9,<10.10",
        "sagelite-gap-package-tomlib >=10.9,<10.10",
        "sagelite-gap-package-transgrp >=10.9,<10.10",
    ]

    assert extras["gap_packages"] == [gap_runtime, *available_gap_packages]


def test_cunningham_tables_registers_data_path():
    pyproject = _pyproject("sagelite-cunningham-tables")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "cunningham_tables": "sagelite_cunningham_tables:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_cunningham_tables"
    ] == [
        "data/cunningham_tables/cunningham_prime_factors.sobj",
    ]


def test_cunningham_tables_accept_precomputed_sage_object_payload():
    setup_py = ROOT / "companion-packages" / "sagelite-cunningham-tables" / "setup.py"
    setup_text = setup_py.read_text()
    repair_text = (ROOT / ".github/workflows/repair-wheel-linux.sh").read_text()

    assert "SAGELITE_CUNNINGHAM_FACTORS_SOBJ" in setup_text
    assert "_find_precomputed_sobj" in setup_text
    assert "cunningham_prime_factors.sobj" in repair_text
    assert "SAGELITE_CUNNINGHAM_FACTORS_SOBJ=$factors_sobj" in repair_text


def test_cunningham_tables_are_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-cunningham-tables >=10.9,<10.10"

    assert extras["cunningham-tables"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_benzene_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-benzene-runtime >=10.9,<10.10"

    assert extras["benzene"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_benzene_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-benzene-runtime")

    assert pyproject["project"]["scripts"] == {
        "benzene": "sagelite_benzene.runtime:benzene",
    }


def test_buckygen_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-buckygen-runtime")

    assert pyproject["project"]["scripts"] == {
        "buckygen": "sagelite_buckygen.runtime:buckygen",
    }


def test_frobby_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-frobby-runtime >=10.9,<10.10"

    assert extras["frobby"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_flatter_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-flatter-runtime >=10.9,<10.10"

    assert extras["flatter"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_flatter_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-flatter-runtime")

    assert pyproject["project"]["scripts"] == {
        "flatter": "sagelite_flatter.runtime:flatter",
    }


def test_flatter_runtime_repair_builds_pinned_source_fallback():
    repair = (ROOT / ".github/workflows/repair-wheel-linux.sh").read_text()

    assert "git clone https://github.com/keeganryan/flatter.git" in repair
    assert "d2b8026f29b4a69e987b15d4b240f8a5053275d3" in repair
    assert 'CMAKE_PREFIX_PATH="$prefix${CMAKE_PREFIX_PATH:+:$CMAKE_PREFIX_PATH}"' in repair
    assert 'SAGELITE_FLATTER_BINDIR="$flatter_bindir"' in repair
    assert 'LD_LIBRARY_PATH="$flatter_runtime_prefix/lib:$prefix/lib' in repair


def test_frobby_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-frobby-runtime")

    assert pyproject["project"]["scripts"] == {
        "frobby": "sagelite_frobby.runtime:frobby",
    }


def test_fricas_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-fricas-runtime >=10.9,<10.10"

    assert extras["fricas"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_fricas_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-fricas-runtime")

    assert pyproject["project"]["scripts"] == {
        "fricas": "sagelite_fricas.runtime:fricas",
    }


def test_fricas_runtime_rewrites_prefix_for_relocation():
    setup_py = (
        ROOT / "companion-packages" / "sagelite-fricas-runtime" / "setup.py"
    ).read_text()

    assert "FRICAS_PREFIX" in setup_py
    assert "exec_prefix=" in setup_py
    assert "fricas-real" in setup_py


def test_sympow_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-sympow-runtime >=10.9,<10.10"

    assert extras["sympow"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_sympow_runtime_builds_datafiles_aware_wrapper():
    setup_py = (
        ROOT / "companion-packages" / "sagelite-sympow-runtime" / "setup.py"
    ).read_text()

    assert "sympow-real" in setup_py
    assert "LD_LIBRARY_PATH" in setup_py
    assert "data_target" in setup_py
    assert "cd \"$HERE/..\" || exit 127" in setup_py


def test_d3js_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-d3js-runtime >=10.9,<10.10"

    assert extras["d3js"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_jmol_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-jmol-runtime >=10.9,<10.10"

    assert extras["jmol"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_cddlib_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-cddlib-runtime >=10.9,<10.10"

    assert extras["cddlib"] == [requirement]
    assert extras["cddexec"] == [requirement]
    assert extras["cddexec_gmp"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_cddlib_runtime_declares_console_scripts():
    pyproject = _pyproject("sagelite-cddlib-runtime")

    assert pyproject["project"]["scripts"] == {
        "cddexec": "sagelite_cddlib.runtime:cddexec",
        "cddexec_gmp": "sagelite_cddlib.runtime:cddexec_gmp",
        "redcheck_gmp": "sagelite_cddlib.runtime:redcheck_gmp",
        "scdd": "sagelite_cddlib.runtime:scdd",
        "scdd_gmp": "sagelite_cddlib.runtime:scdd_gmp",
    }


def test_csdp_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-csdp-runtime >=10.9,<10.10"

    assert extras["csdp"] == [requirement]
    assert extras["theta"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_csdp_runtime_declares_console_scripts():
    pyproject = _pyproject("sagelite-csdp-runtime")

    assert pyproject["project"]["scripts"] == {
        "theta": "sagelite_csdp.runtime:theta",
    }


def test_glucose_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-glucose-runtime >=10.9,<10.10"

    assert extras["glucose"] == [requirement]
    assert extras["glucose-syrup"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_glucose_runtime_declares_console_scripts():
    pyproject = _pyproject("sagelite-glucose-runtime")

    assert pyproject["project"]["scripts"] == {
        "glucose": "sagelite_glucose.runtime:glucose",
        "glucose-syrup": "sagelite_glucose.runtime:glucose_syrup",
    }


def test_graphviz_runtime_declares_console_scripts():
    pyproject = _pyproject("sagelite-graphviz-runtime")

    assert pyproject["project"]["scripts"] == {
        "dot": "sagelite_graphviz.runtime:dot",
        "neato": "sagelite_graphviz.runtime:neato",
        "twopi": "sagelite_graphviz.runtime:twopi",
    }


def test_imagemagick_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-imagemagick-runtime >=10.9,<10.10"

    assert extras["imagemagick"] == [requirement]
    assert extras["magick"] == [requirement]
    assert extras["convert"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_imagemagick_runtime_declares_console_scripts():
    pyproject = _pyproject("sagelite-imagemagick-runtime")

    assert pyproject["project"]["scripts"] == {
        "convert": "sagelite_imagemagick.runtime:convert",
        "magick": "sagelite_imagemagick.runtime:magick",
    }


def test_kissat_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-kissat-runtime >=10.9,<10.10"

    assert extras["kissat"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_kissat_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-kissat-runtime")

    assert pyproject["project"]["scripts"] == {
        "kissat": "sagelite_kissat.runtime:kissat",
    }


def test_dvipng_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-dvipng-runtime >=10.9,<10.10"

    assert extras["dvipng"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_dvipng_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-dvipng-runtime")

    assert pyproject["project"]["scripts"] == {
        "dvipng": "sagelite_dvipng.runtime:dvipng",
    }


def test_planarity_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-planarity-runtime >=10.9,<10.10"

    assert extras["planarity"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_pdf2svg_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-pdf2svg-runtime >=10.9,<10.10"

    assert extras["pdf2svg"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_poppler_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-poppler-runtime >=10.9,<10.10"

    assert extras["poppler"] == [requirement]
    assert extras["pdftocairo"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_pdf2svg_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-pdf2svg-runtime")

    assert pyproject["project"]["scripts"] == {
        "pdf2svg": "sagelite_pdf2svg.runtime:pdf2svg",
    }


def test_poppler_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-poppler-runtime")

    assert pyproject["project"]["scripts"] == {
        "pdftocairo": "sagelite_poppler.runtime:pdftocairo",
    }


def test_planarity_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-planarity-runtime")

    assert pyproject["project"]["scripts"] == {
        "planarity": "sagelite_planarity.runtime:planarity",
    }


def test_lie_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-lie-runtime >=10.9,<10.10"

    assert extras["lie"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_latte_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-latte-runtime >=10.9,<10.10"

    assert extras["latte"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_lcalc_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-lcalc-runtime >=10.9,<10.10"

    assert extras["lcalc"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_lrslib_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-lrslib-runtime >=10.9,<10.10"

    assert extras["lrslib"] == [requirement]
    assert extras["lrs"] == [requirement]
    assert extras["lrsnash"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_mathjax_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-mathjax-runtime >=10.9,<10.10"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["mathjax"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_threejs_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-threejs-runtime >=10.9,<10.10"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["threejs"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_msolve_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-msolve-runtime >=10.9,<10.10"

    assert extras["msolve"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_msolve_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-msolve-runtime")

    assert pyproject["project"]["scripts"] == {
        "msolve": "sagelite_msolve.runtime:msolve",
    }


def test_lie_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-lie-runtime")

    assert pyproject["project"]["scripts"] == {
        "lie": "sagelite_lie.runtime:lie",
    }


def test_lie_runtime_builds_relocatable_wrapper():
    setup_text = (
        ROOT / "companion-packages" / "sagelite-lie-runtime" / "setup.py"
    ).read_text()

    assert "def _write_lie_command" in setup_text
    assert 'LD="${LIE_INFO_DIR:-$PREFIX/LiE}"' in setup_text
    assert 'exec "$LD/Lie.exe" initfile "$LD" "$@"' in setup_text
    assert 'info_target / "Lie.exe"' in setup_text
    assert 'shutil.copy2(command, bin_target / "lie")' not in setup_text


def test_lrslib_runtime_declares_console_scripts():
    pyproject = _pyproject("sagelite-lrslib-runtime")

    assert pyproject["project"]["scripts"] == {
        "lrs": "sagelite_lrslib.runtime:lrs",
        "lrsnash": "sagelite_lrslib.runtime:lrsnash",
    }


def test_lcalc_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-lcalc-runtime")

    assert pyproject["project"]["scripts"] == {
        "lcalc": "sagelite_lcalc.runtime:lcalc",
    }


def test_latte_runtime_wheel_declares_copied_runtime_data():
    pyproject = _pyproject("sagelite-latte-runtime")

    assert pyproject["project"]["scripts"] == {
        "count": "sagelite_latte.runtime:count",
        "integrate": "sagelite_latte.runtime:integrate",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"]["sagelite_latte"] == [
        "data/bin/*",
        "data/lib/*",
    ]


def test_maxima_runtime_wheel_declares_copied_runtime_data():
    pyproject = _pyproject("sagelite-maxima-runtime")
    package_init = (
        ROOT
        / "companion-packages"
        / "sagelite-maxima-runtime"
        / "src"
        / "sagelite_maxima"
        / "__init__.py"
    ).read_text()
    runtime_py = (
        ROOT
        / "companion-packages"
        / "sagelite-maxima-runtime"
        / "src"
        / "sagelite_maxima"
        / "runtime.py"
    ).read_text()

    assert pyproject["project"]["version"] == "10.9.post13"
    assert pyproject["project"]["dependencies"] == [
        "sagelite-ecl-runtime >=10.9,<10.10",
    ]
    assert pyproject["project"]["scripts"] == {
        "maxima": "sagelite_maxima.runtime:maxima",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"]["sagelite_maxima"] == [
        "data/bin/*",
        "data/lib/**/*",
        "data/share/**/*",
    ]
    assert "def maxima_library_path()" in runtime_py
    assert "def runtime_library_dir()" in runtime_py
    assert "def maxima()" in runtime_py
    assert '"maxima_library_path"' in runtime_py
    assert '"runtime_library_dir"' in runtime_py
    assert "maxima_library_path" in package_init
    assert "runtime_library_dir" in package_init


def test_maxima_library_mode_prefers_versioned_companion_tree():
    maxima_lib_py = ROOT / "src" / "sage" / "interfaces" / "maxima_lib.py"
    maxima_lib_text = maxima_lib_py.read_text()

    assert "def _maxima_library_prefix_is_usable" in maxima_lib_text
    assert '"maxima_library_path"' in maxima_lib_text
    assert maxima_lib_text.index('"maxima_library_path"') < maxima_lib_text.index(
        '"maxima_prefix"'
    )


def test_maxima_runtime_patches_copied_ecl_images():
    setup_py = ROOT / "companion-packages" / "sagelite-maxima-runtime" / "setup.py"
    setup_text = setup_py.read_text()

    assert "def _install_roots_for_maxima_prefix" in setup_text
    assert "def _validate_maxima_prefix" in setup_text
    assert "_validate_maxima_prefix(maxima_prefix)" in setup_text
    assert "requires Maxima >= 5.47.0" in setup_text
    assert "src/maxima-package.lisp" in setup_text
    assert "def _validate_copied_ecl_images" in setup_text
    assert "_find_maxima_fas(maxima_prefix)" in setup_text
    assert "_find_ecl_dir(maxima_prefix)" in setup_text
    assert "_validate_copied_ecl_images(ecl_target, runtime_target)" in setup_text
    assert 'original.startswith("libecl")' in setup_text
    assert "SAGELITE_MAXIMA_ECL_SONAME is not set" in setup_text
    assert "SAGELITE_MAXIMA_ALLOW_SYSTEM_ECL" in setup_text
    assert "_patch_ecl_fas(fas_target)" in setup_text
    assert 'for ecl_fas in ecl_target.glob("*.fas")' in setup_text
    assert "_patch_ecl_fas(ecl_fas)" in setup_text
    assert "def _is_ecl_runtime_symbol" in setup_text
    assert "def _system_ecl_libraries" in setup_text
    assert "def _validation_targets" in setup_text
    assert "SAGELITE_MAXIMA_ECL_LIBRARY" in setup_text
    assert "system ECL runtime" in setup_text
    assert '"FE"' in setup_text
    assert "--remove-rpath" in setup_text
    assert "--set-rpath" in setup_text
    assert '"$ORIGIN/../runtime"' in setup_text
    assert '"libgc.so"' in setup_text
    assert '"libffi.so"' in setup_text


def test_maxima_runtime_strips_rpath_for_system_ecl_images(
    monkeypatch, tmp_path
):
    helpers = _maxima_runtime_setup_helpers()
    image = tmp_path / "maxima.fas"
    commands = []

    class Patchelf:
        @staticmethod
        def run(args, **kwargs):
            commands.append(args)
            assert kwargs["check"] is True
            if args[:2] == ["patchelf", "--print-needed"]:
                assert kwargs["capture_output"] is True
                assert kwargs["text"] is True

                class Result:
                    stdout = "libecl.so.24.5\nlibc.so.6\n"

                return Result()
            return None

    monkeypatch.setenv("SAGELITE_MAXIMA_ALLOW_SYSTEM_ECL", "1")
    monkeypatch.delenv("SAGELITE_MAXIMA_ECL_SONAME", raising=False)
    monkeypatch.setitem(helpers, "subprocess", Patchelf)

    helpers["_patch_ecl_fas"](image)

    assert ["patchelf", "--remove-rpath", os.fspath(image)] in commands
    assert not any("--replace-needed" in command for command in commands)


def test_maxima_runtime_sets_relative_rpath_without_ecl_needed(tmp_path):
    helpers = _maxima_runtime_setup_helpers()
    image = tmp_path / "sockets.fas"
    commands = []

    class Patchelf:
        @staticmethod
        def run(args, **kwargs):
            commands.append(args)
            assert kwargs["check"] is True
            if args[:2] == ["patchelf", "--print-needed"]:
                assert kwargs["capture_output"] is True
                assert kwargs["text"] is True

                class Result:
                    stdout = "libc.so.6\n"

                return Result()
            return None

    helpers["subprocess"] = Patchelf

    helpers["_patch_ecl_fas"](image)

    assert commands == [
        ["patchelf", "--print-needed", os.fspath(image)],
        ["patchelf", "--set-rpath", "$ORIGIN/../runtime", os.fspath(image)],
    ]


def test_maxima_runtime_rewrites_ecl_needed_and_sets_relative_rpath(
    monkeypatch, tmp_path
):
    helpers = _maxima_runtime_setup_helpers()
    image = tmp_path / "sockets.fas"
    commands = []

    class Patchelf:
        @staticmethod
        def run(args, **kwargs):
            commands.append(args)
            assert kwargs["check"] is True
            if args[:2] == ["patchelf", "--print-needed"]:
                assert kwargs["capture_output"] is True
                assert kwargs["text"] is True

                class Result:
                    stdout = "libecl.so.24.5\nlibgc.so.1\nlibc.so.6\n"

                return Result()
            return None

    monkeypatch.setenv("SAGELITE_MAXIMA_ECL_SONAME", "libecl-sagelite.so.24.5.10")
    helpers["subprocess"] = Patchelf

    helpers["_patch_ecl_fas"](image)

    assert [
        "patchelf",
        "--replace-needed",
        "libecl.so.24.5",
        "libecl-sagelite.so.24.5.10",
        os.fspath(image),
    ] in commands
    assert ["patchelf", "--set-rpath", "$ORIGIN/../runtime", os.fspath(image)] in commands


def test_maxima_runtime_validation_rejects_missing_fe_symbols(monkeypatch, tmp_path):
    helpers = _maxima_runtime_setup_helpers()
    ecl_dir = tmp_path / "lib" / "ecl-24.5.10"
    runtime_dir = tmp_path / "lib" / "runtime"
    image = ecl_dir / "maxima.fas"
    libecl = runtime_dir / "libecl.so.24.5"
    target_libecl = tmp_path / "sagelite.libs" / "libecl-sagelite.so.24.5.10"
    image.parent.mkdir(parents=True)
    libecl.parent.mkdir(parents=True)
    target_libecl.parent.mkdir(parents=True)
    image.write_text("compiled maxima image\n")
    libecl.write_text("ecl runtime\n")
    target_libecl.write_text("target ecl runtime\n")
    monkeypatch.setenv("SAGELITE_MAXIMA_ECL_LIBRARY", str(target_libecl))

    def dynamic_symbols(path, *args):
        if path == libecl and "--defined-only" in args:
            return {"ecl_stack_pop_values"}
        if path == target_libecl and "--defined-only" in args:
            return {"FEstack_advance", "ecl_stack_pop_values"}
        if path == image and "--undefined-only" in args:
            return {"FEstack_advance", "__stack_chk_fail"}
        return set()

    monkeypatch.setitem(helpers, "_dynamic_symbols", dynamic_symbols)

    with pytest.raises(RuntimeError, match="FEstack_advance"):
        helpers["_validate_copied_ecl_images"](ecl_dir, runtime_dir)


def test_maxima_runtime_validation_requires_target_ecl(monkeypatch, tmp_path):
    helpers = _maxima_runtime_setup_helpers()
    runtime_dir = tmp_path / "lib" / "runtime"
    copied_libecl = runtime_dir / "libecl.so.24.5"
    copied_libecl.parent.mkdir(parents=True)
    copied_libecl.write_text("copied ecl runtime\n")
    monkeypatch.delenv("SAGELITE_MAXIMA_ECL_LIBRARY", raising=False)
    monkeypatch.delenv("SAGELITE_MAXIMA_ALLOW_SYSTEM_ECL", raising=False)

    with pytest.raises(RuntimeError, match="SAGELITE_MAXIMA_ECL_LIBRARY"):
        helpers["_validation_targets"](runtime_dir)


def test_maxima_runtime_validation_checks_target_sagelite_ecl(
    monkeypatch, tmp_path
):
    helpers = _maxima_runtime_setup_helpers()
    ecl_dir = tmp_path / "lib" / "ecl-24.5.10"
    runtime_dir = tmp_path / "lib" / "runtime"
    image = ecl_dir / "maxima.fas"
    copied_libecl = runtime_dir / "libecl.so.24.5"
    target_libecl = tmp_path / "sagelite.libs" / "libecl-sagelite.so.24.5.10"
    image.parent.mkdir(parents=True)
    copied_libecl.parent.mkdir(parents=True)
    target_libecl.parent.mkdir(parents=True)
    image.write_text("compiled maxima image\n")
    copied_libecl.write_text("copied ecl runtime\n")
    target_libecl.write_text("target ecl runtime\n")
    monkeypatch.setenv("SAGELITE_MAXIMA_ECL_LIBRARY", str(target_libecl))

    def dynamic_symbols(path, *args):
        if path == copied_libecl and "--defined-only" in args:
            return {"FEstack_advance", "ecl_stack_pop_values"}
        if path == target_libecl and "--defined-only" in args:
            return {"ecl_stack_pop_values"}
        if path == image and "--undefined-only" in args:
            return {"FEstack_advance", "__stack_chk_fail"}
        return set()

    monkeypatch.setitem(helpers, "_dynamic_symbols", dynamic_symbols)

    with pytest.raises(RuntimeError, match="sagelite ECL runtime"):
        helpers["_validate_copied_ecl_images"](ecl_dir, runtime_dir)


def test_maxima_runtime_validation_accepts_repo_relative_target_ecl(
    monkeypatch, tmp_path
):
    helpers = _maxima_runtime_setup_helpers()
    ecl_dir = tmp_path / "lib" / "ecl-24.5.10"
    runtime_dir = tmp_path / "lib" / "runtime"
    image = ecl_dir / "maxima.fas"
    copied_libecl = runtime_dir / "libecl.so.24.5.10"
    target_libecl = ROOT / "pyproject.toml"
    image.parent.mkdir(parents=True)
    copied_libecl.parent.mkdir(parents=True)
    image.write_text("compiled maxima image\n")
    copied_libecl.write_text("copied ecl runtime\n")
    monkeypatch.setenv(
        "SAGELITE_MAXIMA_ECL_LIBRARY", os.fspath(target_libecl.relative_to(ROOT))
    )

    def dynamic_symbols(path, *args):
        if path in {copied_libecl, target_libecl} and "--defined-only" in args:
            return {"FEstack_advance"}
        if path == image and "--undefined-only" in args:
            return {"FEstack_advance"}
        return set()

    monkeypatch.setitem(helpers, "_dynamic_symbols", dynamic_symbols)

    helpers["_validate_copied_ecl_images"](ecl_dir, runtime_dir)


def test_maxima_runtime_validation_checks_system_ecl_builds(
    monkeypatch, tmp_path
):
    helpers = _maxima_runtime_setup_helpers()
    ecl_dir = tmp_path / "lib" / "ecl-24.5.10"
    runtime_dir = tmp_path / "lib" / "runtime"
    image = ecl_dir / "maxima.fas"
    copied_libecl = runtime_dir / "libecl.so.24.5.10"
    system_libecl = tmp_path / "usr" / "lib" / "libecl.so.24.5"
    image.parent.mkdir(parents=True)
    copied_libecl.parent.mkdir(parents=True)
    system_libecl.parent.mkdir(parents=True)
    image.write_text("compiled maxima image\n")
    copied_libecl.write_text("copied ecl runtime\n")
    system_libecl.write_text("system ecl runtime\n")
    monkeypatch.setenv("SAGELITE_MAXIMA_ALLOW_SYSTEM_ECL", "1")
    monkeypatch.delenv("SAGELITE_MAXIMA_ECL_LIBRARY", raising=False)
    monkeypatch.setitem(
        helpers, "_system_ecl_libraries", lambda: [system_libecl]
    )

    def dynamic_symbols(path, *args):
        if path == copied_libecl and "--defined-only" in args:
            return {"FEstack_advance", "ecl_stack_pop_values"}
        if path == system_libecl and "--defined-only" in args:
            return {"ecl_stack_pop_values"}
        if path == image and "--undefined-only" in args:
            return {"FEstack_advance", "__stack_chk_fail"}
        return set()

    monkeypatch.setitem(helpers, "_dynamic_symbols", dynamic_symbols)

    with pytest.raises(RuntimeError, match="system ECL runtime"):
        helpers["_validate_copied_ecl_images"](ecl_dir, runtime_dir)


def test_companion_workflow_marks_maxima_system_ecl_builds_explicit():
    workflow = ROOT / ".github" / "workflows" / "companion-packages.yml"
    workflow_text = workflow.read_text()
    matrix_start = workflow_text.index("- name: sagelite-maxima-runtime")
    matrix_end = workflow_text.index("- name: sagelite-mwrank-runtime", matrix_start)
    matrix_block = workflow_text[matrix_start:matrix_end]

    assert "apt_packages: maxima-sage maxima-sage-share ecl" in workflow_text
    assert "publish: false" in matrix_block
    assert "Package: maxima-sage maxima-sage-share ecl libecl-dev libecl24.5" in workflow_text
    assert "SAGELITE_MAXIMA_ALLOW_SYSTEM_ECL=1" in workflow_text


def test_companion_workflow_smoke_tests_maxima_library_mode_with_system_ecl():
    smoke_test = ROOT / ".github" / "workflows" / "smoke-test-sagelite-companion.py"
    smoke_test_text = smoke_test.read_text()
    maxima_start = smoke_test_text.index(
        'if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-maxima-runtime":'
    )
    maxima_end = smoke_test_text.index(
        'if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-nauty-runtime":',
        maxima_start,
    )
    maxima_block = smoke_test_text[maxima_start:maxima_end]
    ecl_start = maxima_block.index('ecl = shutil.which("ecl")')
    ecl_block = maxima_block[ecl_start:]

    assert 'env["ECLDIR"] = ecldir' in ecl_block
    assert '"(require \'maxima)"' in ecl_block
    assert 'env["LD_LIBRARY_PATH"]' not in ecl_block
    assert 'env.get("LD_LIBRARY_PATH")' not in ecl_block


def test_linux_repair_validates_maxima_against_repaired_sagelite_ecl():
    repair_script = ROOT / ".github" / "workflows" / "repair-wheel-linux.sh"
    repair_text = repair_script.read_text()

    assert 'auditwheel repair --plat "$AUDITWHEEL_PLAT"' in repair_text
    assert "verify_repaired_sagelite_wheel()" in repair_text
    assert "sage/libs/ecl." in repair_text
    assert "expected exactly one bundled ECL runtime" in repair_text
    verify_call = repair_text.index("\nverify_repaired_sagelite_wheel\n")
    maxima_call = repair_text.index("\nbuild_maxima_runtime_companion\n")
    assert verify_call < maxima_call
    assert (
        repair_text.index('auditwheel repair --plat "$AUDITWHEEL_PLAT"')
        < verify_call
    )
    assert 'sagelite_ecl_library="$tmpdir/$ecl_soname"' in repair_text
    assert "with zipfile.ZipFile(wheel_path) as wheel:" in repair_text
    assert "SAGELITE_MAXIMA_ECL_LIBRARY=\"$sagelite_ecl_library\"" in repair_text
    assert "'*/share/maxima*/*/src'" not in repair_text
    assert "'*/share/maxima/*/src/maxima-package.lisp'" in repair_text
    assert "'*/share/maxima-sage/*/src/maxima-package.lisp'" in repair_text
    assert "sed 's#/src/maxima-package\\.lisp$##'" in repair_text


def test_linux_repair_validates_required_optional_native_extensions():
    repair_script = ROOT / ".github" / "workflows" / "repair-wheel-linux.sh"
    repair_text = repair_script.read_text()

    assert "sagelite_native_wheel_catalog.py" in repair_text
    assert 'catalog["required_native_extension_prefixes"]' in repair_text
    assert "expected required optional native extensions" in repair_text
    assert "sage/libs/coxeter3/coxeter." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/libs/braiding." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/libs/homfly." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/graphs/bliss." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/graphs/cliquer." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/graphs/planarity." in RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    assert "sage/rings/polynomial/pbori/pbori." in (
        RELEASE_REQUIRED_NATIVE_EXTENSION_PREFIXES
    )

    assert "expected auditwheel-bundled runtime library" in repair_text
    assert 'catalog["required_native_library_prefixes"]' in repair_text
    assert "libbrial" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libbrial_groebner" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libbraiding" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libcoxeter3" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libec-" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libec" not in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libhomfly" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libbliss" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libcliquer" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libntl" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES
    assert "libplanarity" in RELEASE_REQUIRED_NATIVE_LIBRARY_PREFIXES

    assert "required_native_smoke_import_modules" in repair_text
    assert "expected repaired sagelite native modules to import" in repair_text
    assert "--target \"$repaired_site\"" in repair_text
    assert "sage.libs.coxeter3.coxeter" in RELEASE_REQUIRED_NATIVE_IMPORT_MODULES
    assert "sage.libs.braiding" in RELEASE_REQUIRED_NATIVE_IMPORT_MODULES
    assert "sage.libs.homfly" in RELEASE_REQUIRED_NATIVE_IMPORT_MODULES
    assert "sage.graphs.bliss" in RELEASE_REQUIRED_NATIVE_IMPORT_MODULES
    assert "sage.graphs.cliquer" in RELEASE_REQUIRED_NATIVE_IMPORT_MODULES
    assert "sage.graphs.planarity" in RELEASE_REQUIRED_NATIVE_IMPORT_MODULES
    assert "sage.libs.ntl.error" in RELEASE_REQUIRED_NATIVE_IMPORT_MODULES
    assert "sage.rings.polynomial.pbori.pbori" in (
        RELEASE_REQUIRED_NATIVE_IMPORT_MODULES
    )
    assert "sage.libs.coxeter3.coxeter" in RELEASE_REQUIRED_NATIVE_SMOKE_IMPORT_MODULES
    assert "sage.graphs.graph_decompositions.tdlib" not in (
        RELEASE_REQUIRED_NATIVE_SMOKE_IMPORT_MODULES
    )
    assert "sage.libs.eclib.newforms" not in RELEASE_REQUIRED_NATIVE_SMOKE_IMPORT_MODULES


def test_staged_wheel_index_validation_collects_runtime_summary_by_default():
    workflow = ROOT / ".github" / "workflows" / "test-sagelite-wheel-index.yml"
    workflow_text = workflow.read_text()

    assert "tools/run-installed-wheel-doctests.py" in workflow_text
    assert "--runtime-summary" in workflow_text
    assert "--manifest-compiled-limit 200" in workflow_text


def test_linux_repair_rejects_mixed_pari_runtimes():
    repair_script = ROOT / ".github" / "workflows" / "repair-wheel-linux.sh"
    repair_text = repair_script.read_text()

    assert 'PATH="$prefix/bin:$PATH"' in repair_text
    assert (
        'LD_LIBRARY_PATH="$prefix/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"'
        in repair_text
    )
    assert (
        'LIBRARY_PATH="$prefix/lib${LIBRARY_PATH:+:$LIBRARY_PATH}"'
        in repair_text
    )
    assert 'CPATH="$prefix/include${CPATH:+:$CPATH}"' in repair_text
    assert 'PKG_CONFIG_PATH="$cypari_pkg_config_path"' in repair_text
    assert 'SAGE_LOCAL="$prefix"' in repair_text
    assert "expected vendored cypari2 extension modules" in repair_text
    assert "cypari2.libs/" in repair_text
    assert "prebuilt cypari2 PARI runtime" in repair_text
    assert "expected exactly one bundled PARI runtime" in repair_text
    assert "verified repaired sagelite PARI runtime" in repair_text


def test_maxima_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-maxima-runtime >=10.9.post13,<10.10"

    assert extras["maxima"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]
    assert requirement in extras["all-needed-extras"]


def test_all_needed_extras_match_installed_validation_plan():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    validation_requirements = set(extras["all-needed-extras"])

    assert "sagelite-maxima-runtime >=10.9.post13,<10.10" in validation_requirements
    assert "sagelite-database-cremona-ellcurve >=10.9,<10.10" in validation_requirements
    assert "sagelite-database-polytopes-4d >=10.9,<10.10" in validation_requirements
    assert "sagelite-database-sloane >=10.9,<10.10" in validation_requirements
    assert "sagelite-database-stein-watkins >=10.9,<10.10" in validation_requirements
    assert "sagelite-ecl-runtime >=10.9,<10.10" in validation_requirements
    assert "sagelite-fricas-runtime >=10.9,<10.10" in validation_requirements
    assert "sagelite-gap-runtime >=10.9.post2,<10.10" in validation_requirements
    assert "sagelite-gap3-runtime >=10.9.post1,<10.10" in validation_requirements
    assert "sagelite-fplll-data >=10.9,<10.10" in validation_requirements
    assert "sagelite-imagemagick-runtime >=10.9,<10.10" in validation_requirements
    assert "sagelite-jmol-runtime >=10.9,<10.10" in validation_requirements
    assert "sagelite-kenzo-runtime >=10.9,<10.10" in validation_requirements
    assert "sagelite-msolve-runtime >=10.9,<10.10" in validation_requirements
    assert "sagelite-qepcad-runtime >=10.9,<10.10" in validation_requirements


def test_singular_runtime_wheel_declares_copied_runtime_data():
    pyproject = _pyproject("sagelite-singular-runtime")

    assert pyproject["project"]["version"] == "10.9.post1"
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_singular_runtime"
    ] == [
        "data/bin/*",
        "data/lib/*",
        "data/singular/**/*",
    ]


def test_singular_runtime_copies_factory_gftables():
    setup_py = ROOT / "companion-packages" / "sagelite-singular-runtime" / "setup.py"
    setup_text = setup_py.read_text()

    assert '"share" / "factory"' in setup_text
    assert '"gftables"' in setup_text
    assert 'target / "share" / "factory"' in setup_text


def test_release_upload_expects_current_singular_runtime_version():
    release = ROOT / ".github" / "workflows" / "release.yml"
    release_text = release.read_text()

    assert (
        "sagelite_singular_runtime-10.9.post1-py3-none-manylinux_2_28_x86_64.whl"
        in release_text
    )
    assert (
        "sagelite_singular_runtime-10.9-py3-none-manylinux_2_28_x86_64.whl"
        not in release_text
    )


def test_polytopes_4d_database_registers_reflexive_polytope_data_path():
    pyproject = _pyproject("sagelite-database-polytopes-4d")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "reflexive_polytopes": "sagelite_database_polytopes_4d:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_polytopes_4d"
    ] == [
        "data/reflexive_polytopes/Hodge4d/**/*",
    ]


def test_polytopes_4d_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-polytopes-4d >=10.9,<10.10"

    assert extras["polytopes-4d"] == [requirement]
    assert extras["database-polytopes-4d"] == [requirement]
    assert requirement not in extras["databases"]
    assert requirement not in extras["full"]


def test_stein_watkins_database_registers_data_path():
    pyproject = _pyproject("sagelite-database-stein-watkins")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "stein_watkins": "sagelite_database_stein_watkins:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_stein_watkins"
    ] == [
        "data/stein_watkins/**/*",
    ]


def test_stein_watkins_database_is_exposed_by_dedicated_sagelite_extra():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-stein-watkins >=10.9,<10.10"

    assert extras["stein-watkins"] == [requirement]
    assert requirement not in extras["databases"]
    assert requirement not in extras["full"]


def test_stein_watkins_mini_database_registers_data_path():
    pyproject = _pyproject("sagelite-database-stein-watkins-mini")
    setup_py = (
        ROOT
        / "companion-packages"
        / "sagelite-database-stein-watkins-mini"
        / "setup.py"
    ).read_text()

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "stein_watkins": "sagelite_database_stein_watkins_mini:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_stein_watkins_mini"
    ] == [
        "data/stein_watkins/a.000.bz2",
        "data/stein_watkins/a.001.bz2",
        "data/stein_watkins/p.00.bz2",
    ]
    assert "SAGELITE_STEIN_WATKINS_MINI_DIR" in setup_py
    assert "local\" / \"share\" / \"stein_watkins" in setup_py
    assert "STEIN_WATKINS_MINI_FILES" in setup_py


def test_stein_watkins_mini_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-stein-watkins-mini >=10.9,<10.10"

    assert extras["stein-watkins-mini"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_topcom_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-topcom-runtime >=10.9,<10.10"

    assert extras["topcom"] == [requirement]
    for extra in (
        "points2allfinetriang",
        "points2allfinetriangs",
        "points2alltriangs",
        "points2finetriang",
        "points2finetriangs",
        "points2placingtriang",
        "points2placingtriangs",
        "points2triang",
        "points2triangs",
    ):
        assert extras[extra] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_four_ti_2_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-4ti2-runtime >=10.9,<10.10"

    assert requirement in pyproject["project"]["dependencies"]
    assert extras["4ti2"] == [requirement]
    for extra in (
        "circuits",
        "graver",
        "groebner",
        "hilbert",
        "markov",
        "ppi",
        "qsolve",
        "rays",
        "zsolve",
    ):
        assert extras[extra] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_gfan_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-gfan-runtime >=10.9,<10.10"

    assert extras["gfan"] == [requirement]
    assert extras["gfan_bases"] == [requirement]
    assert extras["gfan_groebnercone"] == [requirement]
    assert extras["gfan_render"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def _linux_before_all_default_targets() -> set[str]:
    before_all = (ROOT / ".github/workflows/cibw-before-all-linux.sh").read_text()
    marker = 'TARGETS_PRE="${TARGETS_PRE:-'
    return set(before_all.split(marker, 1)[1].split('}"', 1)[0].split())


def _linux_release_targets() -> set[str]:
    release = (ROOT / ".github/workflows/release.yml").read_text()
    for line in release.splitlines():
        stripped = line.strip()
        if stripped.startswith("TARGETS_PRE: "):
            return set(stripped.split("TARGETS_PRE: ", 1)[1].split())
    raise AssertionError("release TARGETS_PRE not found")


def test_runtime_companion_targets_are_staged_for_linux_release_wheels():
    required_targets = {
        "benzene",
        "buckygen",
        "csdp",
        "dvipng",
        "ecl",
        "flatter",
        "fplll",
        "fricas",
        "gfan",
        "imagemagick",
        "jmol",
        "kenzo",
        "latte_int",
        "lie",
        "lrslib",
        "msolve",
        "pdf2svg",
        "plantri",
        "poppler",
        "sympow",
        "tachyon",
        "tides",
        "topcom",
    }

    assert required_targets <= _linux_before_all_default_targets()
    assert required_targets <= _linux_release_targets()


def test_system_tool_runtime_companions_are_staged_for_linux_wheels():
    before_all = (ROOT / ".github/workflows/cibw-before-all-linux.sh").read_text()
    repair = (ROOT / ".github/workflows/repair-wheel-linux.sh").read_text()

    assert "graphviz|dvipng|flatter|imagemagick|pdf2svg|poppler)" in before_all
    assert "tool_packages_debian=(ccache curl)" in before_all
    assert "tool_packages_fedora+=(texlive-dvipng)" in before_all
    assert "tool_packages_fedora+=(eigen3-devel)" in before_all
    assert "tool_packages_fedora+=(ImageMagick)" in before_all
    assert "tool_packages_fedora+=(git gcc pkgconf-pkg-config poppler-glib-devel cairo-devel glib2-devel)" in before_all
    assert "tool_packages_fedora+=(poppler-utils)" in before_all
    assert "git clone https://github.com/dawbarton/pdf2svg.git" in before_all
    assert "2371ca32926354227f58ce6cab18a7bd54136252" in before_all
    assert 'cc -O2 -o "$install_prefix/bin/pdf2svg"' in before_all
    assert "[ -x /usr/bin/dvipng ]" in repair
    assert "[ -x /usr/bin/pdf2svg ]" in repair
    assert "[ -x /usr/bin/pdftocairo ]" in repair
    assert '[ -x "$candidate/magick" ] || [ -x "$candidate/convert" ]' in repair


def test_linux_repair_builds_all_needed_extra_companion_wheels():
    repair = (ROOT / ".github/workflows/repair-wheel-linux.sh").read_text()

    required_calls = [
        "build_database_cremona_ellcurve_companion",
        "build_database_polytopes_4d_companion",
        "build_database_sloane_companion",
        "build_database_stein_watkins_companion",
        "build_ecl_runtime_companion",
        "build_fricas_runtime_companion",
        "build_imagemagick_runtime_companion",
        "build_jmol_runtime_companion",
        "build_kenzo_runtime_companion",
    ]
    for call in required_calls:
        assert f"\n{call}\n" in repair


def test_linux_repair_builds_requested_base_dependency_companion_wheels():
    repair = (ROOT / ".github/workflows/repair-wheel-linux.sh").read_text()

    required_calls = [
        "build_cunningham_tables_companion",
        "build_d3js_runtime_companion",
        "build_mathjax_runtime_companion",
        "build_threejs_runtime_companion",
        "build_sirocco_runtime_companion",
        "build_database_elliptic_curves_companions",
        "build_database_graphs_companion",
        "build_database_jones_numfield_companion",
        "build_database_kohel_companion",
        "build_database_mutation_class_companion",
        "build_database_odlyzko_zeta_companion",
        "build_database_polytopes_companion",
        "build_database_symbolic_data_companion",
    ]
    for call in required_calls:
        assert f"\n{call}\n" in repair

    required_packages = [
        "sagelite-cunningham-tables",
        "sagelite-d3js-runtime",
        "sagelite-database-cremona-mini",
        "sagelite-database-ellcurves",
        "sagelite-database-graphs",
        "sagelite-database-jones-numfield",
        "sagelite-database-kohel",
        "sagelite-database-mutation-class",
        "sagelite-database-odlyzko-zeta",
        "sagelite-database-polytopes",
        "sagelite-database-stein-watkins-mini",
        "sagelite-database-symbolic-data",
        "sagelite-mathjax-runtime",
        "sagelite-sirocco-runtime",
        "sagelite-threejs-runtime",
    ]
    for package in required_packages:
        assert package in repair

    assert (
        repair.index("\nbuild_ecl_runtime_companion\n")
        < repair.index("\nbuild_maxima_runtime_companion\n")
    )
    assert "download_sage_spkg database_cremona_ellcurve" in repair
    assert "download_sage_spkg polytopes_db_4d" in repair
    assert "download_sage_spkg database_stein_watkins" in repair
    assert "https://oeis.org/stripped.gz" in repair
    assert "https://oeis.org/names.gz" in repair
    assert 'local curl_bin="/usr/bin/curl"' in repair
    assert 'env -u LD_LIBRARY_PATH "$curl_bin" --fail --location --retry 5 --retry-delay 5' in repair
    assert "--retry-all-errors" not in repair
    assert "SAGELITE_ECL_PREFIX=$prefix" in repair
    assert "SAGELITE_FRICAS_PREFIX=$prefix" in repair
    assert "SAGELITE_JMOL_DIR=$jmol_dir" in repair
    assert "SAGELITE_KENZO_FAS=$kenzo_fas" in repair


def test_nauty_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-nauty-runtime >=10.9,<10.10"

    assert extras["nauty"] == [requirement]
    for extra in (
        "directg",
        "genbg",
        "geng",
        "genktreeg",
        "genposetg",
        "gentourng",
        "gentreeg",
    ):
        assert extras[extra] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_rubiks_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-rubiks-runtime >=10.9,<10.10"

    assert extras["rubiks"] == [requirement]
    for extra in ("cu2", "cubex", "dikcube", "mcube", "optimal", "size222"):
        assert extras[extra] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_topcom_runtime_wheel_declares_copied_runtime_data():
    pyproject = _pyproject("sagelite-topcom-runtime")

    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"]["sagelite_topcom"] == [
        "data/bin/*",
        "data/lib/*",
    ]
    assert "points2placingtriang" in pyproject["project"]["scripts"]
    assert "points2allfinetriangs" in pyproject["project"]["scripts"]


def test_tachyon_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-tachyon-runtime >=10.9,<10.10"

    assert extras["tachyon"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_tachyon_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-tachyon-runtime")

    assert pyproject["project"]["scripts"] == {
        "tachyon": "sagelite_tachyon.runtime:tachyon",
    }


def test_tachyon_runtime_builds_relocatable_wrapper():
    setup_py = (
        ROOT / "companion-packages" / "sagelite-tachyon-runtime" / "setup.py"
    ).read_text()

    assert "tachyon-real" in setup_py
    assert "LD_LIBRARY_PATH" in setup_py
    assert "lib_target" in setup_py
    assert "_runtime_libraries(source)" in setup_py


def test_plantri_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-plantri-runtime >=10.9,<10.10"

    assert requirement not in pyproject["project"]["dependencies"]
    assert extras["plantri"] == [requirement]
    assert requirement not in extras["runtime"]
    assert requirement not in extras["full"]


def test_plantri_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-plantri-runtime")

    assert pyproject["project"]["scripts"] == {
        "plantri": "sagelite_plantri.runtime:plantri",
    }
