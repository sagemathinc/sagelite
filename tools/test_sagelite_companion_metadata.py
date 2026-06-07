from __future__ import annotations

import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _pyproject(name: str) -> dict:
    with (ROOT / "companion-packages" / name / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)


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


def test_sympow_runtime_is_exposed_by_sagelite_extras():
    with (ROOT / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    extras = pyproject["project"]["optional-dependencies"]
    requirement = "sagelite-sympow-runtime >=10.9,<10.10"

    assert extras["sympow"] == [requirement]
    assert requirement in extras["runtime"]
    assert requirement in extras["full"]
