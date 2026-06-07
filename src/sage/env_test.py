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
    keys = [
        "ECLDIR",
        "FOURTITWO_CIRCUITS",
        "FOURTITWO_GRAVER",
        "FOURTITWO_GROEBNER",
        "FOURTITWO_HILBERT",
        "FOURTITWO_MARKOV",
        "FOURTITWO_PPI",
        "FOURTITWO_QSOLVE",
        "FOURTITWO_RAYS",
        "FOURTITWO_ZSOLVE",
        "GAP_ROOT_PATHS",
        "GFAN_BINS_PREFIX",
        "JMOL_DIR",
        "KENZO_FAS",
        "LATTE_BINS_PREFIX",
        "LIE_INFO_DIR",
        "MAXIMA",
        "MAXIMA_FAS",
        "MAXIMA_LAYOUT_AUTOTOOLS",
        "MAXIMA_PREFIX",
        "MWRANK",
        "PALP_BINS_PREFIX",
        "RUBIKS_BINS_PREFIX",
        "SAGE_GAP3_COMMAND",
        "SAGE_GAP_COMMAND",
        "SAGE_ECMBIN",
        "SAGE_NAUTY_BINS_PREFIX",
        "SYMPOW",
    ]
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
    prefix = root
    fas = root / "lib" / "ecl" / "maxima.fas"
    command = root / "bin" / "maxima"
    (root / "share" / "maxima" / "5.47.0").mkdir(parents=True)
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


def _kenzo_runtime(tmp_path: Path, name: str) -> Path:
    fas = tmp_path / name / "lib" / "ecl" / "kenzo.fas"
    fas.parent.mkdir(parents=True)
    fas.write_text("kenzo fas\n")
    return fas


def _lie_runtime(tmp_path: Path, name: str) -> Path:
    info_dir = tmp_path / name / "lib" / "LiE"
    info_dir.mkdir(parents=True)
    (info_dir / "INFO.0").write_text("@version()\nLiE 2.2.2\n")
    (info_dir / "INFO.3").write_text("@diagram()\n")
    return info_dir


def _jmol_runtime(tmp_path: Path, name: str) -> Path:
    jmol_dir = tmp_path / name / "share" / "jmol"
    jmol_dir.mkdir(parents=True)
    (jmol_dir / "JmolData.jar").write_text("jmol data\n")
    return jmol_dir


def _mwrank_runtime(tmp_path: Path, name: str) -> Path:
    command = tmp_path / name / "bin" / "mwrank"
    command.parent.mkdir(parents=True)
    command.write_text("#!/bin/sh\n")
    command.chmod(0o755)
    return command


def _sympow_runtime(tmp_path: Path, name: str) -> Path:
    command = tmp_path / name / "bin" / "sympow"
    command.parent.mkdir(parents=True)
    command.write_text("#!/bin/sh\n")
    command.chmod(0o755)
    return command


def _gap_runtime_command(tmp_path: Path, name: str) -> Path:
    command = tmp_path / name / "bin" / "gap"
    command.parent.mkdir(parents=True)
    command.write_text("#!/bin/sh\n")
    command.chmod(0o755)
    return command


def _runtime_bin_prefix(tmp_path: Path, name: str, program: str) -> Path:
    prefix = tmp_path / name / "bin"
    prefix.mkdir(parents=True)
    command = prefix / program
    command.write_text("#!/bin/sh\n")
    command.chmod(0o755)
    return prefix


def _runtime_executable(tmp_path: Path, name: str, program: str) -> Path:
    command = tmp_path / name / "bin" / program
    command.parent.mkdir(parents=True, exist_ok=True)
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


def test_gap_root_paths_returns_empty_when_no_runtime_exists(monkeypatch, tmp_path):
    stale_config = tmp_path / "stale-build-root"

    monkeypatch.delenv("GAP_ROOT_PATHS", raising=False)
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", str(stale_config), raising=False)
    monkeypatch.setattr(env, "_optional_runtime_value", lambda module_name, attr_name: None)
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))

    assert env._gap_root_paths() == ""


def test_installed_command_or_fallback_ignores_stale_absolute_path(tmp_path):
    stale = tmp_path / "missing" / "ecl-config"

    assert env._installed_command_or_fallback(str(stale), "ecl-config") == "ecl-config"


def test_gap_feature_is_absent_without_runtime(monkeypatch):
    from sage.features.sagemath import sage__libs__gap

    monkeypatch.setattr(env, "GAP_ROOT_PATHS", "")

    presence = sage__libs__gap().is_present()

    assert not presence
    assert "GAP runtime files are not available" in presence.reason


def test_gap_runtime_sets_pexpect_command(monkeypatch, tmp_path):
    command = _gap_runtime_command(tmp_path, "companion")

    monkeypatch.delenv("SAGE_GAP_COMMAND", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: (
            str(command)
            if (module_name, attr_name)
            == ("sagelite_gap_runtime.runtime", "gap_command")
            else None
        ),
    )

    env._bootstrap_sagelite_gap_runtime()

    assert env.os.environ["SAGE_GAP_COMMAND"] == str(command)


def test_gap_runtime_keeps_existing_pexpect_command(monkeypatch, tmp_path):
    existing = _gap_runtime_command(tmp_path, "existing")
    companion = _gap_runtime_command(tmp_path, "companion")

    monkeypatch.setenv("SAGE_GAP_COMMAND", str(existing))
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(companion),
    )

    env._bootstrap_sagelite_gap_runtime()

    assert env.os.environ["SAGE_GAP_COMMAND"] == str(existing)


def test_gap3_runtime_sets_pexpect_command(monkeypatch, tmp_path):
    command = _runtime_executable(tmp_path, "companion", "gap.sh")

    monkeypatch.delenv("SAGE_GAP3_COMMAND", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: (
            str(command)
            if (module_name, attr_name) == ("sagelite_gap3.runtime", "gap3_command")
            else None
        ),
    )

    env._bootstrap_sagelite_gap3_runtime()

    assert env.os.environ["SAGE_GAP3_COMMAND"] == str(command)


def test_gap3_runtime_keeps_existing_pexpect_command(monkeypatch, tmp_path):
    existing = _runtime_executable(tmp_path, "existing", "gap3")
    companion = _runtime_executable(tmp_path, "companion", "gap.sh")

    monkeypatch.setenv("SAGE_GAP3_COMMAND", str(existing))
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(companion),
    )

    env._bootstrap_sagelite_gap3_runtime()

    assert env.os.environ["SAGE_GAP3_COMMAND"] == str(existing)


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
            ("sagelite_maxima.runtime", "maxima_layout_autotools"): "true",
        }
        return values.get((module_name, attr_name))

    monkeypatch.setattr(env, "_optional_runtime_value", runtime_value)

    env._bootstrap_sagelite_maxima_runtime()

    assert env.os.environ["MAXIMA"] == str(command)
    assert env.os.environ["MAXIMA_PREFIX"] == str(prefix)
    assert env.os.environ["MAXIMA_FAS"] == str(fas)
    assert env.os.environ["MAXIMA_LAYOUT_AUTOTOOLS"] == "true"


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
    monkeypatch.setenv("MAXIMA_LAYOUT_AUTOTOOLS", "true")
    monkeypatch.setenv("ECLDIR", str(existing / "lib" / "ecl"))
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


def test_kenzo_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    fas = _kenzo_runtime(tmp_path, "companion")

    monkeypatch.delenv("KENZO_FAS", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "KENZO_FAS",
        str(tmp_path / "stale-lib" / "ecl" / "kenzo.fas"),
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: fas
        if (module_name, attr_name) == ("sagelite_kenzo.runtime", "kenzo_fas")
        else None,
    )

    env._bootstrap_sagelite_kenzo_runtime()

    assert env.os.environ["KENZO_FAS"] == str(fas)


def test_kenzo_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    fas = _kenzo_runtime(tmp_path, "companion")
    existing_fas = _kenzo_runtime(tmp_path, "existing")

    monkeypatch.setenv("KENZO_FAS", str(existing_fas))
    monkeypatch.setattr(env.sage.config, "KENZO_FAS", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: fas,
    )

    env._bootstrap_sagelite_kenzo_runtime()

    assert env.os.environ["KENZO_FAS"] == str(existing_fas)


def test_lie_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    info_dir = _lie_runtime(tmp_path, "companion")

    monkeypatch.delenv("LIE_INFO_DIR", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "LIE_INFO_DIR",
        str(tmp_path / "stale-lib" / "LiE"),
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: info_dir
        if (module_name, attr_name) == ("sagelite_lie.runtime", "info_dir")
        else None,
    )

    env._bootstrap_sagelite_lie_runtime()

    assert env.os.environ["LIE_INFO_DIR"] == str(info_dir)


def test_lie_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    info_dir = _lie_runtime(tmp_path, "companion")
    existing_info_dir = _lie_runtime(tmp_path, "existing")

    monkeypatch.setenv("LIE_INFO_DIR", str(existing_info_dir))
    monkeypatch.setattr(env.sage.config, "LIE_INFO_DIR", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: info_dir,
    )

    env._bootstrap_sagelite_lie_runtime()

    assert env.os.environ["LIE_INFO_DIR"] == str(existing_info_dir)


def test_jmol_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    jmol_dir = _jmol_runtime(tmp_path, "companion")

    monkeypatch.delenv("JMOL_DIR", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "JMOL_DIR",
        str(tmp_path / "stale-share" / "jmol"),
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: jmol_dir
        if (module_name, attr_name) == ("sagelite_jmol_runtime", "jmol_path")
        else None,
    )

    env._bootstrap_sagelite_jmol_runtime()

    assert env.os.environ["JMOL_DIR"] == str(jmol_dir)


def test_jmol_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    jmol_dir = _jmol_runtime(tmp_path, "companion")
    existing_jmol_dir = _jmol_runtime(tmp_path, "existing")

    monkeypatch.setenv("JMOL_DIR", str(existing_jmol_dir))
    monkeypatch.setattr(env.sage.config, "JMOL_DIR", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: jmol_dir,
    )

    env._bootstrap_sagelite_jmol_runtime()

    assert env.os.environ["JMOL_DIR"] == str(existing_jmol_dir)


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


def test_mwrank_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    command = _mwrank_runtime(tmp_path, "companion")

    monkeypatch.delenv("MWRANK", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "MWRANK",
        str(tmp_path / "stale-bin" / "mwrank"),
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: command
        if (module_name, attr_name) == ("sagelite_mwrank.runtime", "mwrank_command")
        else None,
    )

    env._bootstrap_sagelite_mwrank_runtime()

    assert env.os.environ["MWRANK"] == str(command)


def test_mwrank_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    command = _mwrank_runtime(tmp_path, "companion")
    existing_command = _mwrank_runtime(tmp_path, "existing")

    monkeypatch.setenv("MWRANK", str(existing_command))
    monkeypatch.setattr(env.sage.config, "MWRANK", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: command,
    )

    env._bootstrap_sagelite_mwrank_runtime()

    assert env.os.environ["MWRANK"] == str(existing_command)


def test_sympow_runtime_uses_companion_when_command_is_missing(monkeypatch, tmp_path):
    command = _sympow_runtime(tmp_path, "companion")

    monkeypatch.delenv("SYMPOW", raising=False)
    monkeypatch.setattr(env.shutil, "which", lambda name: None)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: command
        if (module_name, attr_name) == ("sagelite_sympow.runtime", "sympow_command")
        else None,
    )

    env._bootstrap_sagelite_sympow_runtime()

    assert env.os.environ["SYMPOW"] == str(command)


def test_sympow_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    command = _sympow_runtime(tmp_path, "companion")
    existing_command = _sympow_runtime(tmp_path, "existing")

    monkeypatch.setenv("SYMPOW", str(existing_command))
    monkeypatch.setattr(env.shutil, "which", lambda name: None)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: command,
    )

    env._bootstrap_sagelite_sympow_runtime()

    assert env.os.environ["SYMPOW"] == str(existing_command)


def test_sympow_runtime_keeps_system_command(monkeypatch, tmp_path):
    command = _sympow_runtime(tmp_path, "companion")
    system_command = _sympow_runtime(tmp_path, "system")

    monkeypatch.delenv("SYMPOW", raising=False)
    monkeypatch.setattr(env.shutil, "which", lambda name: str(system_command))
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: command,
    )

    env._bootstrap_sagelite_sympow_runtime()

    assert "SYMPOW" not in env.os.environ


def test_gfan_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    prefix = _runtime_bin_prefix(tmp_path, "companion", "gfan")

    monkeypatch.delenv("GFAN_BINS_PREFIX", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "GFAN_BINS_PREFIX",
        str(tmp_path / "stale-bin") + env.os.sep,
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(prefix) + env.os.sep
        if (module_name, attr_name) == ("sagelite_gfan.runtime", "bin_prefix")
        else None,
    )

    env._bootstrap_sagelite_gfan_runtime()

    assert env.os.environ["GFAN_BINS_PREFIX"] == str(prefix) + env.os.sep


def test_gfan_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    prefix = _runtime_bin_prefix(tmp_path, "companion", "gfan")
    existing = _runtime_bin_prefix(tmp_path, "existing", "gfan")

    monkeypatch.setenv("GFAN_BINS_PREFIX", str(existing) + env.os.sep)
    monkeypatch.setattr(env.sage.config, "GFAN_BINS_PREFIX", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(prefix) + env.os.sep,
    )

    env._bootstrap_sagelite_gfan_runtime()

    assert env.os.environ["GFAN_BINS_PREFIX"] == str(existing) + env.os.sep


def test_latte_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    prefix = _runtime_bin_prefix(tmp_path, "companion", "count")
    integrate = prefix / "integrate"
    integrate.write_text("#!/bin/sh\n")
    integrate.chmod(0o755)

    monkeypatch.delenv("LATTE_BINS_PREFIX", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "LATTE_BINS_PREFIX",
        str(tmp_path / "stale-bin") + env.os.sep,
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(prefix) + env.os.sep
        if (module_name, attr_name) == ("sagelite_latte.runtime", "bin_prefix")
        else None,
    )

    env._bootstrap_sagelite_latte_runtime()

    assert env.os.environ["LATTE_BINS_PREFIX"] == str(prefix) + env.os.sep


def test_latte_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    prefix = _runtime_bin_prefix(tmp_path, "companion", "count")
    integrate = prefix / "integrate"
    integrate.write_text("#!/bin/sh\n")
    integrate.chmod(0o755)
    existing = _runtime_bin_prefix(tmp_path, "existing", "count")
    existing_integrate = existing / "integrate"
    existing_integrate.write_text("#!/bin/sh\n")
    existing_integrate.chmod(0o755)

    monkeypatch.setenv("LATTE_BINS_PREFIX", str(existing) + env.os.sep)
    monkeypatch.setattr(env.sage.config, "LATTE_BINS_PREFIX", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(prefix) + env.os.sep,
    )

    env._bootstrap_sagelite_latte_runtime()

    assert env.os.environ["LATTE_BINS_PREFIX"] == str(existing) + env.os.sep


def test_nauty_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    prefix = _runtime_bin_prefix(tmp_path, "companion", "geng")

    monkeypatch.delenv("SAGE_NAUTY_BINS_PREFIX", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "SAGE_NAUTY_BINS_PREFIX",
        str(tmp_path / "stale-bin") + env.os.sep,
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(prefix) + env.os.sep
        if (module_name, attr_name) == ("sagelite_nauty.runtime", "bin_prefix")
        else None,
    )

    env._bootstrap_sagelite_nauty_runtime()

    assert env.os.environ["SAGE_NAUTY_BINS_PREFIX"] == str(prefix) + env.os.sep


def test_nauty_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    prefix = _runtime_bin_prefix(tmp_path, "companion", "geng")
    existing = _runtime_bin_prefix(tmp_path, "existing", "geng")

    monkeypatch.setenv("SAGE_NAUTY_BINS_PREFIX", str(existing) + env.os.sep)
    monkeypatch.setattr(env.sage.config, "SAGE_NAUTY_BINS_PREFIX", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(prefix) + env.os.sep,
    )

    env._bootstrap_sagelite_nauty_runtime()

    assert env.os.environ["SAGE_NAUTY_BINS_PREFIX"] == str(existing) + env.os.sep


def test_rubiks_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    prefix = _runtime_bin_prefix(tmp_path, "companion", "cubex")

    monkeypatch.delenv("RUBIKS_BINS_PREFIX", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "RUBIKS_BINS_PREFIX",
        str(tmp_path / "stale-bin") + env.os.sep,
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(prefix) + env.os.sep
        if (module_name, attr_name) == ("sagelite_rubiks.runtime", "bin_prefix")
        else None,
    )

    env._bootstrap_sagelite_rubiks_runtime()

    assert env.os.environ["RUBIKS_BINS_PREFIX"] == str(prefix) + env.os.sep


def test_rubiks_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    prefix = _runtime_bin_prefix(tmp_path, "companion", "cubex")
    existing = _runtime_bin_prefix(tmp_path, "existing", "cubex")

    monkeypatch.setenv("RUBIKS_BINS_PREFIX", str(existing) + env.os.sep)
    monkeypatch.setattr(env.sage.config, "RUBIKS_BINS_PREFIX", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(prefix) + env.os.sep,
    )

    env._bootstrap_sagelite_rubiks_runtime()

    assert env.os.environ["RUBIKS_BINS_PREFIX"] == str(existing) + env.os.sep


def test_palp_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    prefix = _runtime_bin_prefix(tmp_path, "companion", "poly.x")

    monkeypatch.delenv("PALP_BINS_PREFIX", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "PALP_BINS_PREFIX",
        str(tmp_path / "stale-bin") + env.os.sep,
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(prefix) + env.os.sep
        if (module_name, attr_name) == ("sagelite_palp.runtime", "bin_prefix")
        else None,
    )

    env._bootstrap_sagelite_palp_runtime()

    assert env.os.environ["PALP_BINS_PREFIX"] == str(prefix) + env.os.sep


def test_palp_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    prefix = _runtime_bin_prefix(tmp_path, "companion", "poly.x")
    existing = _runtime_bin_prefix(tmp_path, "existing", "poly.x")

    monkeypatch.setenv("PALP_BINS_PREFIX", str(existing) + env.os.sep)
    monkeypatch.setattr(env.sage.config, "PALP_BINS_PREFIX", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(prefix) + env.os.sep,
    )

    env._bootstrap_sagelite_palp_runtime()

    assert env.os.environ["PALP_BINS_PREFIX"] == str(existing) + env.os.sep


def test_four_ti_2_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    hilbert = _runtime_executable(tmp_path, "companion", "hilbert")
    zsolve = _runtime_executable(tmp_path, "companion", "zsolve")

    monkeypatch.delenv("FOURTITWO_HILBERT", raising=False)
    monkeypatch.delenv("FOURTITWO_ZSOLVE", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "FOURTITWO_HILBERT",
        str(tmp_path / "stale-bin" / "hilbert"),
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_four_ti_2.runtime", "hilbert_command"): str(hilbert),
            ("sagelite_four_ti_2.runtime", "zsolve_command"): str(zsolve),
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_four_ti_2_runtime()

    assert env.os.environ["FOURTITWO_HILBERT"] == str(hilbert)
    assert env.os.environ["FOURTITWO_ZSOLVE"] == str(zsolve)


def test_four_ti_2_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    companion = _runtime_executable(tmp_path, "companion", "hilbert")
    existing = _runtime_executable(tmp_path, "existing", "hilbert")

    monkeypatch.setenv("FOURTITWO_HILBERT", str(existing))
    monkeypatch.setattr(env.sage.config, "FOURTITWO_HILBERT", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(companion)
        if (module_name, attr_name) == ("sagelite_four_ti_2.runtime", "hilbert_command")
        else None,
    )

    env._bootstrap_sagelite_four_ti_2_runtime()

    assert env.os.environ["FOURTITWO_HILBERT"] == str(existing)
