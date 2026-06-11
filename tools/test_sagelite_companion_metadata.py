from __future__ import annotations

import tomllib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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
    "sagelite-gap-runtime": {
        "sagelite_gap_runtime": ["data/bin/*", "data/gap*/**/*"],
    },
    "sagelite-gap-package-grape": {
        "sagelite_gap_package_grape": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-guava": {
        "sagelite_gap_package_guava": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-polycyclic": {
        "sagelite_gap_package_polycyclic": ["data/gaproot/pkg/**/*"],
    },
    "sagelite-gap-package-smallgrp": {
        "sagelite_gap_package_smallgrp": ["data/gaproot/pkg/**/*"],
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
        "sagelite_singular_runtime": ["data/singular/**/*"],
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

REPAIR_WORKFLOW_BUILT_RUNTIME_PACKAGES = {
    "sagelite-4ti2-runtime",
    "sagelite-benzene-runtime",
    "sagelite-buckygen-runtime",
    "sagelite-cddlib-runtime",
    "sagelite-csdp-runtime",
    "sagelite-dvipng-runtime",
    "sagelite-ecm-runtime",
    "sagelite-flatter-runtime",
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
    "sagelite-gap3-runtime",
    "sagelite-fricas-runtime",
    "sagelite-gap-package-grape",
    "sagelite-gap-package-guava",
    "sagelite-gap-package-polycyclic",
    "sagelite-gap-package-smallgrp",
    "sagelite-jmol-runtime",
    "sagelite-kenzo-runtime",
    "sagelite-lie-runtime",
    "sagelite-mathjax-runtime",
    "sagelite-poppler-runtime",
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
    "sagelite-ecm-runtime",
    "sagelite-flatter-runtime",
    "sagelite-frobby-runtime",
    "sagelite-fricas-runtime",
    "sagelite-gap-runtime",
    "sagelite-gap-package-grape",
    "sagelite-gap-package-guava",
    "sagelite-gap-package-polycyclic",
    "sagelite-gap-package-smallgrp",
    "sagelite-gfan-runtime",
    "sagelite-giac-runtime",
    "sagelite-glucose-runtime",
    "sagelite-info-runtime",
    "sagelite-kenzo-runtime",
    "sagelite-kissat-runtime",
    "sagelite-latte-runtime",
    "sagelite-lcalc-runtime",
    "sagelite-lrslib-runtime",
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
    "sagelite-sympow-runtime",
    "sagelite-tachyon-runtime",
    "sagelite-tides-runtime",
    "sagelite-topcom-runtime",
}

RELEASE_WORKFLOW_SEPARATED_RUNTIME_PACKAGES = {
    "sagelite-4ti2-runtime": "four-ti-2-runtime-dist",
    "sagelite-benzene-runtime": "benzene-runtime-dist",
    "sagelite-buckygen-runtime": "buckygen-runtime-dist",
    "sagelite-cddlib-runtime": "cddlib-runtime-dist",
    "sagelite-csdp-runtime": "csdp-runtime-dist",
    "sagelite-ecm-runtime": "ecm-runtime-dist",
    "sagelite-flatter-runtime": "flatter-runtime-dist",
    "sagelite-frobby-runtime": "frobby-runtime-dist",
    "sagelite-gap-runtime": "gap-runtime-dist",
    "sagelite-gfan-runtime": "gfan-runtime-dist",
    "sagelite-giac-runtime": "giac-runtime-dist",
    "sagelite-glucose-runtime": "glucose-runtime-dist",
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


def _pyproject(name: str) -> dict:
    with (ROOT / "companion-packages" / name / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)


def test_runtime_companion_wheels_declare_copied_package_data():
    for package, package_data in RUNTIME_PACKAGE_DATA.items():
        pyproject = _pyproject(package)
        setuptools = pyproject["tool"]["setuptools"]

        assert setuptools["include-package-data"] is True
        assert setuptools["package-data"] == package_data


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


def test_pari_data_wheel_declares_copied_runtime_data():
    pyproject = _pyproject("sagelite-pari-data")

    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"]["sagelite_pari_data"] == [
        "data/pari/galdata/**/*",
        "data/pari/elldata/**/*",
        "data/pari/seadata/**/*",
        "data/pari/galpol/**/*",
        "data/pari/nftables/**/*",
    ]


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

    assert extras["pari-data"] == [requirement]
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

    assert extras["tides"] == [requirement]
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
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_info_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-info-runtime")

    assert pyproject["project"]["scripts"] == {
        "info": "sagelite_info.runtime:info",
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

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "cremona": "sagelite_database_cremona_ellcurve:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_cremona_ellcurve"
    ] == [
        "data/cremona/cremona.db",
    ]


def test_cremona_ellcurve_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-cremona-ellcurve >=10.9,<10.10"

    assert extras["cremona-ellcurve"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_cremona_mini_database_registers_data_path():
    pyproject = _pyproject("sagelite-database-cremona-mini")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "cremona_mini": "sagelite_database_cremona_mini:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_database_cremona_mini"
    ] == [
        "data/cremona/cremona_mini.db",
    ]


def test_cremona_mini_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-database-cremona-mini >=10.9,<10.10"

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
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


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


def test_cubic_hecke_pypi_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "database-cubic-hecke ==2022.4.4"

    assert extras["cubic-hecke"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_knotinfo_pypi_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "database-knotinfo >=2026.3.1"

    assert extras["knotinfo"] == [requirement]
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_matroid_pypi_database_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "matroid-database ==0.3"

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

    assert extras["pycryptosat"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["full"]


def test_khoca_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "khoca >=1.4"

    assert extras["khoca"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["full"]


def test_dot2tex_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "dot2tex >=2.11.3"

    assert extras["dot2tex"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["full"]


def test_phitigra_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "phitigra >=0.2.3"

    assert extras["phitigra"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["full"]


def test_regina_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "regina >=7.4.1"

    assert extras["regina"] == [requirement]
    assert requirement in extras["extra"]
    assert requirement in extras["full"]


def test_imageio_ffmpeg_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "imageio-ffmpeg >=0.6.0"

    assert extras["ffmpeg"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_pypandoc_binary_pypi_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "pypandoc-binary >=1.17"

    assert extras["pandoc"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_buckygen_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-buckygen-runtime >=10.9,<10.10"

    assert extras["buckygen"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


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
    assert grape in extras["runtime"]
    assert grape in extras["full"]


def test_gap_guava_package_registers_gap_root_path():
    pyproject = _pyproject("sagelite-gap-package-guava")

    assert pyproject["project"]["entry-points"]["sagemath.gap_root_paths"] == {
        "guava": "sagelite_gap_package_guava.runtime:gap_root_paths",
    }
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_gap_package_guava"
    ] == [
        "data/gaproot/pkg/**/*",
    ]


def test_gap_guava_package_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    guava = "sagelite-gap-package-guava >=10.9,<10.10"

    assert extras["gap-guava"] == [gap_runtime, guava]
    assert extras["gap_package_guava"] == [gap_runtime, guava]
    assert guava in extras["runtime"]
    assert guava in extras["full"]


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
    assert polycyclic in extras["runtime"]
    assert polycyclic in extras["full"]


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
    assert smallgrp in extras["runtime"]
    assert smallgrp in extras["full"]


def test_gap_packages_extra_matches_available_gap_package_companions():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    gap_runtime = "sagelite-gap-runtime >=10.9.post2,<10.10"
    available_gap_packages = [
        "sagelite-gap-package-grape >=10.9,<10.10",
        "sagelite-gap-package-guava >=10.9,<10.10",
        "sagelite-gap-package-polycyclic >=10.9,<10.10",
        "sagelite-gap-package-smallgrp >=10.9,<10.10",
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
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


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
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


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
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_cddlib_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-cddlib-runtime >=10.9,<10.10"

    assert extras["cddlib"] == [requirement]
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
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


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
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_glucose_runtime_declares_console_scripts():
    pyproject = _pyproject("sagelite-glucose-runtime")

    assert pyproject["project"]["scripts"] == {
        "glucose": "sagelite_glucose.runtime:glucose",
        "glucose-syrup": "sagelite_glucose.runtime:glucose_syrup",
    }


def test_kissat_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-kissat-runtime >=10.9,<10.10"

    assert extras["kissat"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


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
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


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
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


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
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_mathjax_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-mathjax-runtime >=10.9,<10.10"

    assert extras["mathjax"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_msolve_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-msolve-runtime >=10.9,<10.10"

    assert extras["msolve"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


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

    assert pyproject["project"]["version"] == "10.9.post1"
    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"]["sagelite_maxima"] == [
        "data/bin/*",
        "data/lib/**/*",
        "data/share/**/*",
    ]


def test_maxima_runtime_patches_copied_ecl_images():
    setup_py = ROOT / "companion-packages" / "sagelite-maxima-runtime" / "setup.py"
    setup_text = setup_py.read_text()

    assert 'original.startswith("libecl")' in setup_text
    assert "_patch_ecl_fas(fas_target)" in setup_text
    assert 'for ecl_fas in ecl_target.glob("*.fas")' in setup_text
    assert "_patch_ecl_fas(ecl_fas)" in setup_text


def test_maxima_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-maxima-runtime >=10.9.post1,<10.10"

    assert extras["maxima"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_singular_runtime_wheel_declares_copied_runtime_data():
    pyproject = _pyproject("sagelite-singular-runtime")

    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"][
        "sagelite_singular_runtime"
    ] == [
        "data/singular/**/*",
    ]


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
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


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
    assert requirement in extras["databases"]
    assert requirement in extras["full"]


def test_stein_watkins_mini_database_registers_data_path():
    pyproject = _pyproject("sagelite-database-stein-watkins-mini")

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
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


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
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


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

    assert extras["plantri"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_plantri_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-plantri-runtime")

    assert pyproject["project"]["scripts"] == {
        "plantri": "sagelite_plantri.runtime:plantri",
    }
