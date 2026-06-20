import os
import sys
import types

from sage.features.gap import GapPackage


class _FakeGapPath:
    def __init__(self, path):
        self._path = path

    def sage(self):
        return self._path


class _FakeGapDirectory:
    def __init__(self, path):
        self._path = os.fspath(path)

    def Filename(self, name):
        return _FakeGapPath(os.path.join(self._path, name))


class _FakeLibgap:
    def __init__(self, program_dirs):
        self._program_dirs = program_dirs

    def eval(self, command):
        assert command == 'LoadPackage("guava")'
        return True

    def DirectoriesPackagePrograms(self, package):
        assert package == "guava"
        return [_FakeGapDirectory(path) for path in self._program_dirs]


def _install_fake_libgap(monkeypatch, libgap):
    module = types.ModuleType("sage.libs.gap.libgap")
    module.libgap = libgap
    monkeypatch.setitem(sys.modules, "sage.libs.gap.libgap", module)


def _install_fake_guava_companion(monkeypatch, roots):
    package = types.ModuleType("sagelite_gap_package_guava")
    runtime = types.ModuleType("sagelite_gap_package_guava.runtime")
    runtime.gap_root_paths = lambda: roots
    monkeypatch.setitem(sys.modules, "sagelite_gap_package_guava", package)
    monkeypatch.setitem(sys.modules, "sagelite_gap_package_guava.runtime", runtime)


def test_guava_feature_requires_executable_wtdist(monkeypatch, tmp_path):
    package_bin = tmp_path / "guava" / "bin"
    package_bin.mkdir(parents=True)
    wtdist = package_bin / "wtdist"
    wtdist.write_text("#!/bin/sh\n", encoding="utf-8")
    wtdist.chmod(0o755)

    _install_fake_libgap(monkeypatch, _FakeLibgap([package_bin]))

    result = GapPackage("guava", spkg="gap_packages")._is_present()

    assert bool(result)


def test_guava_feature_is_absent_without_executable_wtdist(monkeypatch, tmp_path):
    package_bin = tmp_path / "guava" / "bin"
    package_bin.mkdir(parents=True)
    (package_bin / "wtdist").write_text("#!/bin/sh\n", encoding="utf-8")

    _install_fake_libgap(monkeypatch, _FakeLibgap([package_bin]))

    result = GapPackage("guava", spkg="gap_packages")._is_present()

    assert not bool(result)
    assert "wtdist" in result.reason


def test_guava_feature_rejects_incomplete_sagelite_companion(
    monkeypatch, tmp_path
):
    package_bin = tmp_path / "host" / "pkg" / "guava" / "bin"
    package_bin.mkdir(parents=True)
    wtdist = package_bin / "wtdist"
    wtdist.write_text("#!/bin/sh\n", encoding="utf-8")
    wtdist.chmod(0o755)

    _install_fake_libgap(monkeypatch, _FakeLibgap([package_bin]))
    _install_fake_guava_companion(monkeypatch, "")

    result = GapPackage("guava", spkg="gap_packages")._is_present()

    assert not bool(result)
    assert "does not expose a complete GAP package root" in result.reason


def test_guava_feature_rejects_host_wtdist_when_sagelite_companion_installed(
    monkeypatch, tmp_path
):
    companion_root = tmp_path / "companion" / "gaproot"
    host_bin = tmp_path / "host" / "pkg" / "guava" / "bin"
    host_bin.mkdir(parents=True)
    wtdist = host_bin / "wtdist"
    wtdist.write_text("#!/bin/sh\n", encoding="utf-8")
    wtdist.chmod(0o755)

    _install_fake_libgap(monkeypatch, _FakeLibgap([host_bin]))
    _install_fake_guava_companion(monkeypatch, str(companion_root))

    result = GapPackage("guava", spkg="gap_packages")._is_present()

    assert not bool(result)
    assert "outside the installed sagelite companion roots" in result.reason


def test_guava_feature_accepts_companion_wtdist_when_sagelite_companion_installed(
    monkeypatch, tmp_path
):
    companion_root = tmp_path / "companion" / "gaproot"
    package_bin = companion_root / "pkg" / "guava" / "bin"
    package_bin.mkdir(parents=True)
    wtdist = package_bin / "wtdist"
    wtdist.write_text("#!/bin/sh\n", encoding="utf-8")
    wtdist.chmod(0o755)

    _install_fake_libgap(monkeypatch, _FakeLibgap([package_bin]))
    _install_fake_guava_companion(monkeypatch, str(companion_root))

    result = GapPackage("guava", spkg="gap_packages")._is_present()

    assert bool(result)
