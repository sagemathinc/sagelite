from __future__ import annotations

import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


RUNTIME_PACKAGE_DATA = {
    "sagelite-4ti2-runtime": {
        "sagelite_four_ti_2": ["data/bin/*"],
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
    "sagelite-jmol-runtime": {
        "sagelite_jmol_runtime": ["data/jmol/**/*"],
    },
    "sagelite-kenzo-runtime": {
        "sagelite_kenzo": ["data/kenzo.fas"],
    },
    "sagelite-latte-runtime": {
        "sagelite_latte": ["data/bin/*", "data/lib/*"],
    },
    "sagelite-lie-runtime": {
        "sagelite_lie": ["data/bin/*", "data/LiE/**/*"],
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
    "sagelite-nauty-runtime": {
        "sagelite_nauty": ["data/bin/*"],
    },
    "sagelite-palp-runtime": {
        "sagelite_palp": ["data/bin/*"],
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
    "sagelite-threejs-runtime": {
        "sagelite_threejs_runtime": ["data/threejs-sage/**/*"],
    },
    "sagelite-topcom-runtime": {
        "sagelite_topcom": ["data/bin/*", "data/lib/*"],
    },
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


def test_d3js_runtime_registers_static_data_path():
    pyproject = _pyproject("sagelite-d3js-runtime")

    assert pyproject["project"]["entry-points"]["sagemath.data_paths"] == {
        "d3js": "sagelite_d3js_runtime:sage_data_path",
    }
    assert pyproject["tool"]["setuptools"]["package-data"]["sagelite_d3js_runtime"] == [
        "data/d3js/**/*",
    ]


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


def test_mathjax_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-mathjax-runtime >=10.9,<10.10"

    assert extras["mathjax"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]


def test_lie_runtime_declares_console_script():
    pyproject = _pyproject("sagelite-lie-runtime")

    assert pyproject["project"]["scripts"] == {
        "lie": "sagelite_lie.runtime:lie",
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
