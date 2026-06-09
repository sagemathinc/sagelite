import importlib.util
import sys
from pathlib import Path

import pytest

import sage.env
from sage.features import _trivial_unique_representation_cache


ROOT = Path(__file__).resolve().parents[3]
SOURCE_MODULE = ROOT / "src" / "sage" / "features" / "meataxe.py"


def _load_source_meataxe_module():
    if not SOURCE_MODULE.exists():
        from sage.features import meataxe

        return meataxe

    fullname = "sage.features.meataxe"
    sys.modules.pop(fullname, None)
    spec = importlib.util.spec_from_file_location(fullname, SOURCE_MODULE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[fullname] = module
    spec.loader.exec_module(module)
    return module


meataxe = _load_source_meataxe_module()


@pytest.fixture(autouse=True)
def clean_feature_cache():
    _trivial_unique_representation_cache.clear()
    yield
    _trivial_unique_representation_cache.clear()


def _write_meataxe_tables(tmp_path, *names):
    table_dir = tmp_path / "meataxe"
    table_dir.mkdir()
    for name in names:
        (table_dir / name).write_text("meataxe table\n")
    return table_dir


def test_meataxe_tables_feature_accepts_companion_table_directory(monkeypatch, tmp_path):
    table_dir = _write_meataxe_tables(
        tmp_path, "p002.zzz", "p009.zzz", "p025.zzz", "p125.zzz", "p251.zzz"
    )

    monkeypatch.setattr(sage.env, "MTXLIB", str(table_dir))

    presence = meataxe.MeatAxeTables().is_present()

    assert presence


def test_meataxe_tables_feature_rejects_incomplete_table_directory(
    monkeypatch, tmp_path
):
    table_dir = _write_meataxe_tables(tmp_path, "p009.zzz")

    monkeypatch.setattr(sage.env, "MTXLIB", str(table_dir))

    presence = meataxe.MeatAxeTables().is_present()

    assert not presence
    assert "p125.zzz" in presence.reason
