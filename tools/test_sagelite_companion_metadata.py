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
    "sagelite-ecm-runtime": {
        "sagelite_ecm": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-gap-runtime": {
        "sagelite_gap_runtime": ["data/bin/*", "data/gap*/**/*"],
    },
    "sagelite-gap3-runtime": {
        "sagelite_gap3": ["data/gap3/**/*"],
    },
    "sagelite-gfan-runtime": {
        "sagelite_gfan": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-glucose-runtime": {
        "sagelite_glucose": ["data/bin/*"],
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
    "sagelite-planarity-runtime": {
        "sagelite_planarity": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-plantri-runtime": {
        "sagelite_plantri": ["data/bin/*"],
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
        "sagelite_tachyon": ["data/bin/*"],
    },
    "sagelite-threejs-runtime": {
        "sagelite_threejs_runtime": ["data/threejs-sage/**/*"],
    },
    "sagelite-topcom-runtime": {
        "sagelite_topcom": ["data/bin/*", "data/lib/*"],
    },
}

REPAIR_WORKFLOW_BUILT_RUNTIME_PACKAGES = {
    "sagelite-4ti2-runtime",
    "sagelite-benzene-runtime",
    "sagelite-buckygen-runtime",
    "sagelite-cddlib-runtime",
    "sagelite-csdp-runtime",
    "sagelite-ecm-runtime",
    "sagelite-gap-runtime",
    "sagelite-gfan-runtime",
    "sagelite-glucose-runtime",
    "sagelite-kissat-runtime",
    "sagelite-latte-runtime",
    "sagelite-lrslib-runtime",
    "sagelite-maxima-runtime",
    "sagelite-meataxe-runtime",
    "sagelite-msolve-runtime",
    "sagelite-mwrank-runtime",
    "sagelite-nauty-runtime",
    "sagelite-palp-runtime",
    "sagelite-planarity-runtime",
    "sagelite-plantri-runtime",
    "sagelite-rubiks-runtime",
    "sagelite-singular-runtime",
    "sagelite-sympow-runtime",
    "sagelite-tachyon-runtime",
    "sagelite-topcom-runtime",
}

REPAIR_WORKFLOW_EXTERNAL_RUNTIME_PACKAGES = {
    "sagelite-d3js-runtime",
    "sagelite-gap3-runtime",
    "sagelite-jmol-runtime",
    "sagelite-kenzo-runtime",
    "sagelite-lie-runtime",
    "sagelite-mathjax-runtime",
    "sagelite-threejs-runtime",
}

COMPANION_WORKFLOW_BUILT_RUNTIME_PACKAGES = {
    "sagelite-4ti2-runtime",
    "sagelite-cddlib-runtime",
    "sagelite-csdp-runtime",
    "sagelite-ecm-runtime",
    "sagelite-gap-runtime",
    "sagelite-gfan-runtime",
    "sagelite-glucose-runtime",
    "sagelite-kenzo-runtime",
    "sagelite-kissat-runtime",
    "sagelite-maxima-runtime",
    "sagelite-meataxe-runtime",
    "sagelite-mwrank-runtime",
    "sagelite-nauty-runtime",
    "sagelite-palp-runtime",
    "sagelite-pari-data",
    "sagelite-planarity-runtime",
    "sagelite-plantri-runtime",
    "sagelite-rubiks-runtime",
    "sagelite-singular-runtime",
    "sagelite-sympow-runtime",
    "sagelite-tachyon-runtime",
    "sagelite-topcom-runtime",
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


def test_linux_repair_builds_pari_data_companion_wheel():
    repair_script = ROOT / ".github" / "workflows" / "repair-wheel-linux.sh"
    repair_text = repair_script.read_text()

    assert "companion-packages/sagelite-pari-data" in repair_text
    assert "build_pari_data_companion" in repair_text
    assert "SAGELITE_PARI_DATA_DIR" in repair_text


def test_d3js_runtime_registers_static_data_path():
    pyproject = _pyproject("sagelite-d3js-runtime")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "d3js": "sagelite_d3js_runtime:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["package-data"]["sagelite_d3js_runtime"] == [
        "data/d3js/**/*",
    ]


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


def test_buckygen_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-buckygen-runtime >=10.9,<10.10"

    assert extras["buckygen"] == [requirement]
    assert requirement in extras["runtime"]
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


def test_sympow_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-sympow-runtime >=10.9,<10.10"

    assert extras["sympow"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_d3js_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-d3js-runtime >=10.9,<10.10"

    assert extras["d3js"] == [requirement]
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


def test_planarity_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-planarity-runtime >=10.9,<10.10"

    assert extras["planarity"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


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

    assert pyproject["tool"]["setuptools"]["include-package-data"] is True
    assert pyproject["tool"]["setuptools"]["package-data"]["sagelite_maxima"] == [
        "data/bin/*",
        "data/lib/**/*",
        "data/share/**/*",
    ]


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
        "reflexive_polytopes_4d": "sagelite_database_polytopes_4d:sage_data_path",
    }
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
    assert requirement not in extras["databases"]
    assert requirement not in extras["full"]


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
