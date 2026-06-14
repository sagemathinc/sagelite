import pytest

from sage.cli import selftest


class FakeDistribution:
    def __init__(self, requires):
        self.requires = requires


def test_installed_requirements_accepts_matching_versions(monkeypatch):
    monkeypatch.setattr(
        selftest.importlib_metadata,
        "distribution",
        lambda name: FakeDistribution(
            [
                "sagelite-maxima-runtime >=10.9.post7,<10.10",
                'optional-package >=1; extra == "optional"',
            ]
        ),
    )
    monkeypatch.setattr(
        selftest.importlib_metadata,
        "version",
        lambda name: {"sagelite-maxima-runtime": "10.9.post7"}[name],
    )

    assert (
        selftest._check_installed_requirements()
        == "installed requirement versions satisfy metadata"
    )


def test_installed_requirements_rejects_stale_companion_version(monkeypatch):
    monkeypatch.setattr(
        selftest.importlib_metadata,
        "distribution",
        lambda name: FakeDistribution(
            ["sagelite-maxima-runtime >=10.9.post7,<10.10"]
        ),
    )
    monkeypatch.setattr(
        selftest.importlib_metadata,
        "version",
        lambda name: {"sagelite-maxima-runtime": "10.9.post5"}[name],
    )

    with pytest.raises(RuntimeError, match="sagelite-maxima-runtime 10.9.post5"):
        selftest._check_installed_requirements()


def test_installed_requirements_ignores_missing_runtime(monkeypatch):
    monkeypatch.setattr(
        selftest.importlib_metadata,
        "distribution",
        lambda name: FakeDistribution(["sagelite-pari-data >=10.9,<10.10"]),
    )

    def missing_version(name):
        raise selftest.importlib_metadata.PackageNotFoundError(name)

    monkeypatch.setattr(selftest.importlib_metadata, "version", missing_version)

    assert (
        selftest._check_installed_requirements()
        == "installed requirement versions satisfy metadata"
    )
