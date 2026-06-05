import importlib.util
import sys
from pathlib import Path

import pytest

import sage

_CONFIG_PATH = Path(__file__).resolve().parents[2] / "build" / "sage-distro" / "src" / "sage" / "config.py"
if not hasattr(sage, "config") and _CONFIG_PATH.exists():
    _spec = importlib.util.spec_from_file_location("sage.config", _CONFIG_PATH)
    _module = importlib.util.module_from_spec(_spec)
    sys.modules["sage.config"] = _module
    _spec.loader.exec_module(_module)
    sage.config = _module

from sage import env


@pytest.fixture(autouse=True)
def clean_runtime_environment():
    keys = ["GAP_ROOT_PATHS", "MAXIMA", "MAXIMA_FAS", "MAXIMA_PREFIX", "SAGE_ECMBIN"]
    before = {key: env.os.environ.get(key) for key in keys}
    yield
    for key, value in before.items():
        if value is None:
            env.os.environ.pop(key, None)
        else:
            env.os.environ[key] = value


def _gap_root(tmp_path: Path, name: str) -> Path:
    root = tmp_path / name
    (root / "lib").mkdir(parents=True)
    (root / "lib" / "init.g").write_text("# GAP init\n")
    return root


def _maxima_runtime(tmp_path: Path, name: str) -> tuple[Path, Path, Path]:
    root = tmp_path / name
    prefix = root / "share" / "maxima" / "5.47.0"
    fas = root / "lib" / "ecl" / "maxima.fas"
    command = root / "bin" / "maxima"
    prefix.mkdir(parents=True)
    fas.parent.mkdir(parents=True)
    command.parent.mkdir(parents=True)
    fas.write_text("maxima fas\n")
    command.write_text("#!/bin/sh\n")
    command.chmod(0o755)
    return prefix, fas, command


def _ecm_runtime(tmp_path: Path, name: str) -> Path:
    command = tmp_path / name / "bin" / "ecm"
    command.parent.mkdir(parents=True)
    command.write_text("#!/bin/sh\n")
    command.chmod(0o755)
    return command


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


def test_maxima_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    prefix, fas, command = _maxima_runtime(tmp_path, "companion")

    monkeypatch.delenv("MAXIMA", raising=False)
    monkeypatch.delenv("MAXIMA_PREFIX", raising=False)
    monkeypatch.delenv("MAXIMA_FAS", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "MAXIMA",
        str(tmp_path / "stale-bin" / "maxima"),
        raising=False,
    )
    monkeypatch.setattr(env.sage.config, "MAXIMA_PREFIX", str(tmp_path / "stale"), raising=False)
    monkeypatch.setattr(env.sage.config, "MAXIMA_FAS", str(tmp_path / "stale.fas"), raising=False)

    def runtime_value(module_name, attr_name):
        values = {
            ("sagelite_maxima.runtime", "maxima_command"): command,
            ("sagelite_maxima.runtime", "maxima_prefix"): prefix,
            ("sagelite_maxima.runtime", "maxima_fas"): fas,
        }
        return values.get((module_name, attr_name))

    monkeypatch.setattr(env, "_optional_runtime_value", runtime_value)

    env._bootstrap_sagelite_maxima_runtime()

    assert env.os.environ["MAXIMA"] == str(command)
    assert env.os.environ["MAXIMA_PREFIX"] == str(prefix)
    assert env.os.environ["MAXIMA_FAS"] == str(fas)


def test_maxima_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    prefix, fas, command = _maxima_runtime(tmp_path, "companion")
    existing_command = tmp_path / "existing-bin" / "maxima"
    existing = tmp_path / "configured"
    existing_fas = tmp_path / "configured" / "maxima.fas"
    existing_command.parent.mkdir()
    existing_command.write_text("#!/bin/sh\n")
    existing_command.chmod(0o755)
    existing_fas.parent.mkdir()
    existing_fas.write_text("existing maxima fas\n")

    monkeypatch.setenv("MAXIMA", str(existing_command))
    monkeypatch.setenv("MAXIMA_PREFIX", str(existing))
    monkeypatch.setenv("MAXIMA_FAS", str(existing_fas))
    monkeypatch.setattr(env.sage.config, "MAXIMA", "", raising=False)
    monkeypatch.setattr(env.sage.config, "MAXIMA_PREFIX", "", raising=False)
    monkeypatch.setattr(env.sage.config, "MAXIMA_FAS", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(
            {
                "maxima_command": command,
                "maxima_prefix": prefix,
                "maxima_fas": fas,
            }[attr_name]
        ),
    )

    env._bootstrap_sagelite_maxima_runtime()

    assert env.os.environ["MAXIMA"] == str(existing_command)
    assert env.os.environ["MAXIMA_PREFIX"] == str(existing)
    assert env.os.environ["MAXIMA_FAS"] == str(existing_fas)


def test_ecm_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    command = _ecm_runtime(tmp_path, "companion")

    monkeypatch.delenv("SAGE_ECMBIN", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "SAGE_ECMBIN",
        str(tmp_path / "stale-bin" / "ecm"),
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: command
        if (module_name, attr_name) == ("sagelite_ecm.runtime", "ecm_command")
        else None,
    )

    env._bootstrap_sagelite_ecm_runtime()

    assert env.os.environ["SAGE_ECMBIN"] == str(command)


def test_ecm_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    command = _ecm_runtime(tmp_path, "companion")
    existing_command = _ecm_runtime(tmp_path, "existing")

    monkeypatch.setenv("SAGE_ECMBIN", str(existing_command))
    monkeypatch.setattr(env.sage.config, "SAGE_ECMBIN", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: command,
    )

    env._bootstrap_sagelite_ecm_runtime()

    assert env.os.environ["SAGE_ECMBIN"] == str(existing_command)
