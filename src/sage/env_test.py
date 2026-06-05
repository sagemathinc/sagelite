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

from sage import env


def _gap_root(tmp_path: Path, name: str) -> Path:
    root = tmp_path / name
    (root / "lib").mkdir(parents=True)
    (root / "lib" / "init.g").write_text("# GAP init\n")
    return root


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


def test_gap_root_paths_prefers_environment(monkeypatch, tmp_path):
    configured = _gap_root(tmp_path, "configured")
    companion = _gap_root(tmp_path, "companion")

    monkeypatch.setenv("GAP_ROOT_PATHS", str(configured))
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", "", raising=False)
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(companion),
    )

    assert env._gap_root_paths().split(";") == [str(configured), str(companion)]


def test_gap_root_paths_uses_companion_runtime(monkeypatch, tmp_path):
    companion = _gap_root(tmp_path, "companion")
    stale_config = tmp_path / "stale-build-root"

    monkeypatch.delenv("GAP_ROOT_PATHS", raising=False)
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", str(stale_config), raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(companion),
    )
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))

    assert env._gap_root_paths() == str(companion)


def test_gap_root_paths_ignores_broken_companion(monkeypatch, tmp_path):
    baked = _gap_root(tmp_path, "configured")
    broken = tmp_path / "broken-companion"

    monkeypatch.delenv("GAP_ROOT_PATHS", raising=False)
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", str(baked), raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(broken),
    )
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))

    assert env._gap_root_paths() == str(baked)
