from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _load_vendor():
    path = ROOT / ".github" / "workflows" / "vendor-cypari-wheel.py"
    spec = importlib.util.spec_from_file_location("vendor_cypari_wheel", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_vendor_cypari_rejects_private_pari_runtime(tmp_path):
    vendor = _load_vendor()
    src = tmp_path / "site"
    (src / "cypari2").mkdir(parents=True)
    (src / "cypari2" / "__init__.py").write_text("", encoding="utf-8")
    (src / "cypari2.libs").mkdir()
    (src / "cypari2.libs" / "libpari-3a78ce10.so.2.17.2").write_text(
        "private pari runtime\n",
        encoding="utf-8",
    )

    with pytest.raises(SystemExit, match="private PARI runtime"):
        vendor.copy_cypari_runtime(src, tmp_path / "wheel")


def test_vendor_cypari_keeps_non_pari_private_libraries(tmp_path):
    vendor = _load_vendor()
    src = tmp_path / "site"
    dest = tmp_path / "wheel"
    (src / "cypari2").mkdir(parents=True)
    (src / "cypari2" / "__init__.py").write_text("", encoding="utf-8")
    (src / "cypari2.libs").mkdir()
    (src / "cypari2.libs" / "libhelper.so").write_text(
        "private helper runtime\n",
        encoding="utf-8",
    )

    vendor.copy_cypari_runtime(src, dest)

    assert (dest / "cypari2" / "__init__.py").is_file()
    assert (dest / "cypari2.libs" / "libhelper.so").is_file()
