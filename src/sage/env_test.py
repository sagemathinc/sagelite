import importlib.util
from pathlib import Path
import sys

import sage

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "build" / "sage-distro" / "src" / "sage" / "config.py"
if not hasattr(sage, "config") and _CONFIG_PATH.exists():
    _spec = importlib.util.spec_from_file_location("sage.config", _CONFIG_PATH)
    _module = importlib.util.module_from_spec(_spec)
    sys.modules["sage.config"] = _module
    _spec.loader.exec_module(_module)
    sage.config = _module

import sage.env as env


class _EntryPoint:
    def __init__(self, value):
        self._value = value

    def load(self):
        return self._value


def test_sage_data_paths_discovers_registered_entry_points(monkeypatch, tmp_path):
    root = tmp_path / "companion-data"
    (root / "cremona").mkdir(parents=True)

    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(lambda: root)],
    )
    monkeypatch.setattr(env, "SAGE_DATA_PATH", None)

    assert str(root / "cremona") in env.sage_data_paths("cremona")


def test_sage_data_paths_accepts_multiple_registered_directories(monkeypatch, tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()

    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(lambda: [first, second])],
    )

    assert env._registered_sage_data_paths() == {str(first), str(second)}


def test_sage_data_paths_ignores_broken_entry_points(monkeypatch, tmp_path):
    existing = tmp_path / "existing"
    existing.mkdir()

    def broken():
        raise RuntimeError("boom")

    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(broken), _EntryPoint(existing)],
    )

    assert env._registered_sage_data_paths() == {str(existing)}
