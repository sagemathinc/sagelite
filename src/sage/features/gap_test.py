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
