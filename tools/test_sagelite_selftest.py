from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _load_selftest():
    path = ROOT / "src" / "sage" / "cli" / "selftest.py"
    spec = importlib.util.spec_from_file_location("sage_cli_selftest", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_selftest_rejects_private_cypari_pari_runtime(monkeypatch, tmp_path):
    selftest = _load_selftest()
    package_dir = tmp_path / "site-packages" / "cypari2"
    package_dir.mkdir(parents=True)
    origin = package_dir / "__init__.py"
    origin.write_text("", encoding="utf-8")
    private_libs = tmp_path / "site-packages" / "cypari2.libs"
    private_libs.mkdir()
    (private_libs / "libpari-3a78ce10.so.2.17.2").write_text(
        "private pari runtime\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        selftest.importlib.util,
        "find_spec",
        lambda name: importlib.machinery.ModuleSpec(name, loader=None, origin=origin),
    )

    with pytest.raises(RuntimeError, match="private PARI runtime"):
        selftest._check_single_pari_runtime()


def test_selftest_accepts_cypari_without_private_pari_runtime(
    monkeypatch, tmp_path
):
    selftest = _load_selftest()
    package_dir = tmp_path / "site-packages" / "cypari2"
    package_dir.mkdir(parents=True)
    origin = package_dir / "__init__.py"
    origin.write_text("", encoding="utf-8")

    monkeypatch.setattr(
        selftest.importlib.util,
        "find_spec",
        lambda name: importlib.machinery.ModuleSpec(name, loader=None, origin=origin),
    )

    assert (
        selftest._check_single_pari_runtime()
        == "cypari2 does not carry a private PARI runtime"
    )


def test_selftest_stops_after_pari_runtime_packaging_failure(monkeypatch):
    selftest = _load_selftest()
    calls = []

    def run_check(name, check):
        calls.append(name)
        return name != "PARI runtime packaging"

    monkeypatch.setattr(selftest, "_run_check", run_check)

    assert selftest.main() == 1
    assert calls == ["installed package requirements", "PARI runtime packaging"]
