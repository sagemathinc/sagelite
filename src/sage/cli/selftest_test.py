import sys
import types

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


def test_installed_requirements_rejects_missing_runtime(monkeypatch):
    monkeypatch.setattr(
        selftest.importlib_metadata,
        "distribution",
        lambda name: FakeDistribution(["sagelite-pari-data >=10.9,<10.10"]),
    )

    def missing_version(name):
        raise selftest.importlib_metadata.PackageNotFoundError(name)

    monkeypatch.setattr(selftest.importlib_metadata, "version", missing_version)

    with pytest.raises(RuntimeError, match="sagelite-pari-data is not installed"):
        selftest._check_installed_requirements()


def test_run_check_reports_signal_style_failures(capsys):
    class FakeSignalError(BaseException):
        pass

    def raise_signal_error():
        raise FakeSignalError("segfault")

    assert selftest._run_check("signal probe", raise_signal_error) is False

    output = capsys.readouterr()
    assert "checking signal probe ... FAIL" in output.out
    assert "FakeSignalError: segfault" in output.err


@pytest.mark.parametrize("exception", [KeyboardInterrupt, SystemExit])
def test_run_check_preserves_process_exit_exceptions(exception):
    def raise_exception():
        raise exception()

    with pytest.raises(exception):
        selftest._run_check("exit probe", raise_exception)


class FakeFeatureResult:
    def __init__(self, present, reason=""):
        self.present = present
        self.reason = reason

    def __bool__(self):
        return self.present


class FakeFeature:
    def __init__(self, present, reason=""):
        self.present = present
        self.reason = reason

    def is_present(self):
        return FakeFeatureResult(self.present, self.reason)


def test_companion_feature_skips_missing_companion(monkeypatch):
    def missing_module(name):
        raise ImportError(name)

    monkeypatch.setattr(selftest.importlib, "import_module", missing_module)

    assert (
        selftest._check_companion_feature(
            "sagelite_missing", lambda: FakeFeature(True), "missing runtime"
        )
        == "not installed"
    )


def test_companion_feature_rejects_installed_but_missing_feature(monkeypatch):
    monkeypatch.setattr(selftest.importlib, "import_module", lambda name: object())

    with pytest.raises(RuntimeError, match="not executable"):
        selftest._check_companion_feature(
            "sagelite_broken",
            lambda: FakeFeature(False, "not executable"),
            "broken runtime",
        )


def test_companion_feature_accepts_present_feature(monkeypatch):
    monkeypatch.setattr(selftest.importlib, "import_module", lambda name: object())

    assert (
        selftest._check_companion_feature(
            "sagelite_present", lambda: FakeFeature(True), "present runtime"
        )
        == "present runtime available"
    )


def test_glucose_runtime_checks_both_companion_executables(monkeypatch):
    checked = []

    class FakeGlucose:
        def __init__(self, program):
            checked.append(program)

        def is_present(self):
            return FakeFeatureResult(True)

    fake_sat = types.ModuleType("sage.features.sat")
    fake_sat.Glucose = FakeGlucose
    monkeypatch.setitem(sys.modules, "sage.features.sat", fake_sat)
    monkeypatch.setattr(
        selftest.importlib,
        "import_module",
        lambda name: object() if name == "sagelite_glucose" else None,
    )

    assert selftest._check_glucose_runtime() == "Glucose executable runtime available"
    assert checked == ["glucose", "glucose-syrup"]


def test_glucose_runtime_rejects_missing_companion_executable(monkeypatch):
    class FakeGlucose:
        def __init__(self, program):
            self.program = program

        def is_present(self):
            return FakeFeatureResult(self.program == "glucose", "missing syrup")

    fake_sat = types.ModuleType("sage.features.sat")
    fake_sat.Glucose = FakeGlucose
    monkeypatch.setitem(sys.modules, "sage.features.sat", fake_sat)
    monkeypatch.setattr(
        selftest.importlib,
        "import_module",
        lambda name: object() if name == "sagelite_glucose" else None,
    )

    with pytest.raises(RuntimeError, match="glucose-syrup"):
        selftest._check_glucose_runtime()


def test_cddlib_runtime_uses_feature_absolute_filename(monkeypatch):
    class FakeCddExecutable:
        def __init__(self, program):
            self.program = program

        def is_present(self):
            return FakeFeatureResult(True)

        def absolute_filename(self):
            return f"/tmp/{self.program}"

    fake_cddlib = types.ModuleType("sage.features.cddlib")
    fake_cddlib.CddExecutable = FakeCddExecutable
    monkeypatch.setitem(sys.modules, "sage.features.cddlib", fake_cddlib)
    monkeypatch.setattr(
        selftest.importlib,
        "import_module",
        lambda name: object() if name == "sagelite_cddlib" else None,
    )

    assert (
        selftest._check_cddlib_runtime()
        == "cddexec=/tmp/cddexec, cddexec_gmp=/tmp/cddexec_gmp"
    )
