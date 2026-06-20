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
def clean_runtime_environment(monkeypatch):
    keys = [
        "ECLDIR",
        "ECL_CONFIG",
        "FOURTITWO_CIRCUITS",
        "FOURTITWO_GRAVER",
        "FOURTITWO_GROEBNER",
        "FOURTITWO_HILBERT",
        "FOURTITWO_MARKOV",
        "FOURTITWO_PPI",
        "FOURTITWO_QSOLVE",
        "FOURTITWO_RAYS",
        "FOURTITWO_ZSOLVE",
        "FRICAS",
        "FRICAS_COMMAND",
        "FRICAS_INITFILE",
        "FRICAS_PREFIX",
        "GAP_ROOT_PATHS",
        "GFAN_BINS_PREFIX",
        "GP_DATA_DIR",
        "GV_PLUGIN_PATH",
        "INFOPATH",
        "JMOL_DIR",
        "KENZO_FAS",
        "LATTE_BINS_PREFIX",
        "LD_LIBRARY_PATH",
        "LIE_INFO_DIR",
        "MAXIMA",
        "MAXIMA_FAS",
        "MAXIMA_IMAGESDIR",
        "MAXIMA_LAYOUT_AUTOTOOLS",
        "MAXIMA_PREFIX",
        "MATHJAX_DIR",
        "MTXLIB",
        "MWRANK",
        "PALP_BINS_PREFIX",
        "RUBIKS_BINS_PREFIX",
        "SAGE_GAP3_COMMAND",
        "SAGE_GAP_COMMAND",
        "SAGE_ECMBIN",
        "SAGE_LIE_COMMAND",
        "SAGE_NAUTY_BINS_PREFIX",
        "SINGULAR_DEFAULT_DIR",
        "SINGULAR_ROOT_DIR",
        "SYMPOW",
        "TACHYON",
        "THREEJS_DIR",
        "PATH",
    ]
    before = {key: env.os.environ.get(key) for key in keys}
    monkeypatch.setattr(env.importlib_metadata, "entry_points", lambda **kwargs: [])
    monkeypatch.setattr(env, "_sagelite_gap_package_root_paths", lambda: set())
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


def _gap_package_root(tmp_path: Path, name: str, package: str = "grape") -> Path:
    root = tmp_path / name
    package_root = root / "pkg" / package
    package_root.mkdir(parents=True)
    (package_root / "PackageInfo.g").write_text("PackageInfo := rec();\n")
    return root


def _maxima_runtime(tmp_path: Path, name: str) -> tuple[Path, Path, Path, Path]:
    root = tmp_path / name
    prefix = root
    fas = root / "lib" / "ecl" / "maxima.fas"
    command = root / "bin" / "maxima"
    imagesdir = root / "lib" / "maxima" / "5.47.0"
    (root / "share" / "maxima" / "5.47.0").mkdir(parents=True)
    imagesdir.mkdir(parents=True)
    fas.parent.mkdir(parents=True)
    command.parent.mkdir(parents=True)
    fas.write_text("maxima fas\n")
    command.write_text("#!/bin/sh\n")
    command.chmod(0o755)
    return prefix, fas, command, imagesdir


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


def _ecl_runtime(tmp_path: Path, name: str) -> tuple[Path, Path]:
    root = tmp_path / name
    command = root / "bin" / "ecl-config"
    ecldir = root / "lib" / "ecl-24.5.10"
    command.parent.mkdir(parents=True)
    ecldir.mkdir(parents=True)
    (ecldir / "asdf.fas").write_text("asdf fas\n")
    command.write_text(
        f"#!/bin/sh\n"
        f"if [ \"$1\" = \"--libs\" ]; then echo ' -L{root / 'lib'} -lecl'; fi\n"
    )
    command.chmod(0o755)
    return command, ecldir


def _pari_data_runtime(tmp_path: Path, name: str) -> Path:
    data_dir = tmp_path / name / "share" / "pari"
    (data_dir / "galdata").mkdir(parents=True)
    return data_dir


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


def _mathjax_runtime(tmp_path: Path, name: str) -> Path:
    mathjax_dir = tmp_path / name / "share" / "mathjax" / "mathjax"
    mathjax_dir.mkdir(parents=True)
    (mathjax_dir / "tex-chtml.js").write_text("console.log('mathjax');\n")
    (mathjax_dir / "loader.js").write_text("console.log('loader');\n")
    return mathjax_dir


def _threejs_runtime(tmp_path: Path, name: str) -> Path:
    threejs_dir = tmp_path / name / "share" / "threejs-sage"
    version_dir = threejs_dir / "r124"
    version_dir.mkdir(parents=True)
    (threejs_dir / "version").write_text("r124\n")
    (version_dir / "three.min.js").write_text("console.log('three');\n")
    return threejs_dir


def _meataxe_runtime(tmp_path: Path, name: str, *, complete: bool = True) -> Path:
    table_dir = tmp_path / name / "share" / "meataxe"
    table_dir.mkdir(parents=True)
    (table_dir / "p009.zzz").write_text("meataxe table\n")
    if complete:
        for table in ("p002.zzz", "p025.zzz", "p125.zzz", "p251.zzz"):
            (table_dir / table).write_text("meataxe table\n")
    return table_dir


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


def _tachyon_runtime(tmp_path: Path, name: str) -> Path:
    command = tmp_path / name / "bin" / "tachyon"
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


def _fricas_runtime(tmp_path: Path, name: str) -> tuple[Path, Path, Path]:
    prefix = tmp_path / name
    command = prefix / "bin" / "fricas"
    initfile = prefix / "lib" / "fricas" / "fricas.input"
    command.parent.mkdir(parents=True)
    initfile.parent.mkdir(parents=True)
    command.write_text("#!/bin/sh\n")
    command.chmod(0o755)
    initfile.write_text("-- FriCAS init\n")
    return prefix, command, initfile


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


def _singular_runtime(tmp_path: Path, name: str) -> tuple[Path, Path]:
    root = tmp_path / name / "singular"
    default_dir = root / "share" / "singular"
    (default_dir / "LIB").mkdir(parents=True)
    (default_dir / "LIB" / "standard.lib").write_text("// Singular library\n")
    return root, default_dir


def _info_runtime(tmp_path: Path, name: str) -> tuple[Path, Path]:
    root = tmp_path / name
    command = root / "bin" / "info"
    info_dir = root / "share" / "info"
    command.parent.mkdir(parents=True)
    info_dir.mkdir(parents=True)
    command.write_text("#!/bin/sh\n")
    command.chmod(0o755)
    (info_dir / "singular.info").write_text("Singular manual\n")
    return command, info_dir


def _graphviz_runtime(tmp_path: Path, name: str) -> tuple[Path, Path, Path, Path]:
    root = tmp_path / name / "data"
    bin_dir = root / "bin"
    lib_dir = root / "lib"
    plugin_dir = lib_dir / "graphviz"
    bin_dir.mkdir(parents=True)
    plugin_dir.mkdir(parents=True)
    dot = bin_dir / "dot"
    dot.write_text("#!/bin/sh\n")
    dot.chmod(0o755)
    return dot, bin_dir, lib_dir, plugin_dir


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


def test_sage_data_paths_accepts_registered_named_directory(monkeypatch, tmp_path):
    root = tmp_path / "companion-data"
    direct = root / "cremona"
    direct.mkdir(parents=True)

    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(lambda: direct)],
    )
    monkeypatch.setattr(env, "SAGE_DATA_PATH", None)

    assert str(direct) in env.sage_data_paths("cremona")


def test_sage_data_paths_ignores_missing_named_subdirectories(
    monkeypatch, tmp_path
):
    root = tmp_path / "companion-data"
    direct = root / "cremona"
    unrelated = tmp_path / "other-companion-data"
    direct.mkdir(parents=True)
    unrelated.mkdir()

    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(lambda: [root, unrelated])],
    )
    monkeypatch.setattr(env, "SAGE_DATA_PATH", None)
    monkeypatch.setattr(env, "_optional_runtime_value", lambda *args: None)

    assert str(direct) in env.sage_data_paths("cremona")


def test_sage_data_paths_accepts_registered_file_path(monkeypatch, tmp_path):
    root = tmp_path / "companion-data"
    direct = root / "cremona"
    database = direct / "cremona_mini.db"
    direct.mkdir(parents=True)
    database.write_text("cremona\n")

    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(lambda: database)],
    )
    monkeypatch.setattr(env, "SAGE_DATA_PATH", None)

    assert str(direct) in env.sage_data_paths("cremona")


def test_sage_data_paths_keeps_registered_roots_without_name(monkeypatch, tmp_path):
    root = tmp_path / "companion-data"
    root.mkdir()

    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(lambda: root)],
    )
    monkeypatch.setattr(env, "SAGE_DATA_PATH", None)

    assert str(root) in env.sage_data_paths()


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
    monkeypatch.setattr(env, "_optional_runtime_value", lambda *args: None)

    assert env._registered_sage_data_paths() == {str(first), str(second)}


def test_sage_data_paths_accepts_registered_file_paths_in_iterables(
    monkeypatch, tmp_path
):
    first = tmp_path / "first"
    second = tmp_path / "second"
    database = second / "graphs.db"
    first.mkdir()
    second.mkdir()
    database.write_text("graphs\n")

    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(lambda: [first, database])],
    )
    monkeypatch.setattr(env, "_optional_runtime_value", lambda *args: None)

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
    monkeypatch.setattr(env, "_optional_runtime_value", lambda *args: None)

    assert env._registered_sage_data_paths() == {str(existing)}


def test_sage_data_paths_accepts_direct_sagelite_companion_paths(
    monkeypatch, tmp_path
):
    database_companion = tmp_path / "database-companion" / "data"
    pari_companion = tmp_path / "pari-companion" / "data" / "pari"
    static_companion = tmp_path / "static-companion" / "data"
    database_companion.mkdir(parents=True)
    pari_companion.mkdir(parents=True)
    static_companion.mkdir(parents=True)

    monkeypatch.setattr(env, "_entry_points", lambda group: [])

    values = {
        ("sagelite_database_jones_numfield", "sage_data_path"): database_companion,
        ("sagelite_pari_data", "sage_data_path"): pari_companion,
        ("sagelite_threejs_runtime", "sage_data_path"): static_companion,
    }
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: values.get((module_name, attr_name)),
    )

    assert env._registered_sage_data_paths() == {
        str(database_companion),
        str(pari_companion),
        str(static_companion),
    }


def test_sage_data_paths_filters_missing_direct_sagelite_companion_paths(
    monkeypatch, tmp_path
):
    missing = tmp_path / "missing" / "data"

    monkeypatch.setattr(env, "_entry_points", lambda group: [])
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(missing),
    )

    assert env._registered_sage_data_paths() == set()


def test_optional_runtime_data_dir_accepts_companion_directory(monkeypatch, tmp_path):
    companion = tmp_path / "companion" / "graphs"
    companion.mkdir(parents=True)
    (companion / "graphs.db").write_text("graphs\n")

    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(companion),
    )

    assert (
        env._optional_runtime_data_dir(
            "sagelite_database_graphs", "graphs_data_path", "graphs.db"
        )
        == str(companion)
    )


def test_optional_runtime_data_dir_accepts_companion_file_path(monkeypatch, tmp_path):
    companion = tmp_path / "companion" / "cremona"
    companion.mkdir(parents=True)
    database = companion / "cremona_mini.db"
    database.write_text("cremona\n")

    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(database),
    )

    assert (
        env._optional_runtime_data_dir(
            "sagelite_database_cremona_mini",
            "cremona_mini_path",
            "cremona_mini.db",
            path_is_file=True,
        )
        == str(companion)
    )


def test_optional_runtime_data_dir_ignores_missing_marker(monkeypatch, tmp_path):
    companion = tmp_path / "companion" / "ellcurves"
    companion.mkdir(parents=True)

    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(companion),
    )

    assert (
        env._optional_runtime_data_dir(
            "sagelite_database_ellcurves", "ellcurves_data_path", "rank0"
        )
        is None
    )


def test_fplll_default_strategy_file_keeps_usable_fpylll_path(tmp_path):
    strategy_dir = tmp_path / "strategies"
    strategy_dir.mkdir()
    strategy = strategy_dir / "default.json"
    strategy.write_text("[]")

    assert env._fplll_default_strategy_file(strategy_dir, strategy) == str(strategy)


def test_fplll_default_strategy_file_uses_companion_for_stale_fpylll_path(
    monkeypatch, tmp_path
):
    strategy_dir = tmp_path / "strategies"
    strategy_dir.mkdir()
    bundled_strategy = strategy_dir / "default.json"
    bundled_strategy.write_text("[]")

    def optional_runtime_value(module_name, attr_name):
        if (module_name, attr_name) == (
            "sagelite_fplll_data.runtime",
            "default_strategy",
        ):
            return str(bundled_strategy)
        return None

    monkeypatch.setattr(env, "_optional_runtime_value", optional_runtime_value)

    assert env._fplll_default_strategy_file(
        b"/stale/share/fplll/strategies",
        b"/stale/share/fplll/strategies/default.json",
    ) == str(bundled_strategy)


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

    assert env._gap_root_paths().split(";") == [str(configured)]


def test_gap_root_paths_does_not_append_registered_package_roots_to_environment(
    monkeypatch, tmp_path
):
    configured = _gap_root(tmp_path, "configured")
    package = _gap_package_root(tmp_path, "grape")

    monkeypatch.setenv("GAP_ROOT_PATHS", str(configured))
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", "", raising=False)
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))
    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(lambda: package)],
    )
    monkeypatch.setattr(
        env, "_sagelite_gap_package_root_paths", lambda: {str(package)}
    )

    assert env._gap_root_paths().split(";") == [str(configured)]


def test_gap_root_paths_prefers_valid_configured_core_over_companion(
    monkeypatch, tmp_path
):
    configured = _gap_root(tmp_path, "configured")
    companion = _gap_root(tmp_path, "companion")

    monkeypatch.delenv("GAP_ROOT_PATHS", raising=False)
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", str(configured), raising=False)
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(companion),
    )

    assert env._gap_root_paths().split(";") == [str(configured)]


def test_gap_root_paths_does_not_append_registered_package_roots_to_configured_core(
    monkeypatch, tmp_path
):
    configured = _gap_root(tmp_path, "configured")
    package = _gap_package_root(tmp_path, "grape")

    monkeypatch.delenv("GAP_ROOT_PATHS", raising=False)
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", str(configured), raising=False)
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))
    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(lambda: package)],
    )
    monkeypatch.setattr(
        env, "_sagelite_gap_package_root_paths", lambda: {str(package)}
    )

    assert env._gap_root_paths().split(";") == [str(configured)]


def test_gap_root_paths_prefers_companion_over_host_system_config(
    monkeypatch, tmp_path
):
    configured = _gap_root(tmp_path, "host-configured")
    companion = _gap_root(tmp_path, "companion")
    package = _gap_package_root(tmp_path, "guava", package="guava")

    monkeypatch.delenv("GAP_ROOT_PATHS", raising=False)
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", str(configured), raising=False)
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))
    monkeypatch.setattr(
        env,
        "_is_host_system_gap_root",
        lambda root: root == str(configured),
    )
    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(lambda: package)],
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(companion)
        if (module_name, attr_name) == ("sagelite_gap_runtime.runtime", "gap_root_paths")
        else None,
    )

    assert env._gap_root_paths().split(";") == [str(companion), str(package)]


def test_gap_root_paths_appends_registered_package_roots(monkeypatch, tmp_path):
    core = _gap_root(tmp_path, "core")
    package = _gap_package_root(tmp_path, "grape")

    monkeypatch.delenv("GAP_ROOT_PATHS", raising=False)
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", "", raising=False)
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(core)
        if (module_name, attr_name) == ("sagelite_gap_runtime.runtime", "gap_root_paths")
        else None,
    )
    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(lambda: package)],
    )

    assert env._gap_root_paths().split(";") == [str(core), str(package)]


def test_gap_root_paths_appends_direct_package_companion_roots(monkeypatch, tmp_path):
    core = _gap_root(tmp_path, "core")
    package = _gap_package_root(tmp_path, "grape")

    monkeypatch.delenv("GAP_ROOT_PATHS", raising=False)
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", "", raising=False)
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))
    monkeypatch.setattr(env, "_entry_points", lambda group: [])
    monkeypatch.setattr(
        env, "_sagelite_gap_package_root_paths", lambda: {str(package)}
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_gap_runtime.runtime", "gap_root_paths"): str(core),
            ("sagelite_gap_package_grape.runtime", "gap_root_paths"): str(package),
        }.get((module_name, attr_name)),
    )

    assert env._gap_root_paths().split(";") == [str(core), str(package)]


def test_gap_root_paths_supports_legacy_entry_point_api(monkeypatch, tmp_path):
    core = _gap_root(tmp_path, "core")
    package = _gap_package_root(tmp_path, "grape")

    monkeypatch.delenv("GAP_ROOT_PATHS", raising=False)
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", "", raising=False)
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(core)
        if (module_name, attr_name) == ("sagelite_gap_runtime.runtime", "gap_root_paths")
        else None,
    )

    def legacy_entry_points(**kwargs):
        if kwargs:
            raise TypeError("legacy importlib.metadata API")
        return {"sagemath.gap_root_paths": [_EntryPoint(lambda: package)]}

    monkeypatch.setattr(env.importlib_metadata, "entry_points", legacy_entry_points)

    assert env._gap_root_paths().split(";") == [str(core), str(package)]


def test_gap_root_paths_ignores_package_roots_without_core(monkeypatch, tmp_path):
    package = _gap_package_root(tmp_path, "grape")

    monkeypatch.delenv("GAP_ROOT_PATHS", raising=False)
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", "", raising=False)
    monkeypatch.setattr(env, "_optional_runtime_value", lambda module_name, attr_name: None)
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))
    monkeypatch.setattr(
        env.importlib_metadata,
        "entry_points",
        lambda **kwargs: [_EntryPoint(lambda: package)],
    )

    assert env._gap_root_paths() == ""


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


def test_gap_runtime_does_not_mix_companion_command_with_configured_core(
    monkeypatch, tmp_path
):
    configured = _gap_root(tmp_path, "configured")
    companion = _gap_root(tmp_path, "companion")
    command = _gap_runtime_command(tmp_path, "companion")

    monkeypatch.delenv("SAGE_GAP_COMMAND", raising=False)
    monkeypatch.delenv("GAP_ROOT_PATHS", raising=False)
    monkeypatch.setattr(env.sage.config, "GAP_ROOT_PATHS", str(configured), raising=False)
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "ext_data"))
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_gap_runtime.runtime", "gap_command"): str(command),
            ("sagelite_gap_runtime.runtime", "gap_root_paths"): str(companion),
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_gap_runtime()

    assert "SAGE_GAP_COMMAND" not in env.os.environ


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


def test_fricas_runtime_uses_companion(monkeypatch, tmp_path):
    prefix, command, initfile = _fricas_runtime(tmp_path, "companion")

    for name in ("FRICAS", "FRICAS_COMMAND", "FRICAS_PREFIX", "FRICAS_INITFILE"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_fricas.runtime", "executable_path"): str(command),
            ("sagelite_fricas.runtime", "fricas_prefix"): str(prefix),
            ("sagelite_fricas.runtime", "initfile_path"): str(initfile),
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_fricas_runtime()

    assert env.os.environ["FRICAS"] == str(command)
    assert env.os.environ["FRICAS_COMMAND"] == str(command)
    assert env.os.environ["FRICAS_PREFIX"] == str(prefix)
    assert env.os.environ["FRICAS_INITFILE"] == str(initfile)


def test_fricas_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    existing = _runtime_executable(tmp_path, "existing", "fricas")
    prefix, command, initfile = _fricas_runtime(tmp_path, "companion")

    monkeypatch.setenv("FRICAS", str(existing))
    monkeypatch.delenv("FRICAS_COMMAND", raising=False)
    monkeypatch.delenv("FRICAS_PREFIX", raising=False)
    monkeypatch.delenv("FRICAS_INITFILE", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_fricas.runtime", "executable_path"): str(command),
            ("sagelite_fricas.runtime", "fricas_prefix"): str(prefix),
            ("sagelite_fricas.runtime", "initfile_path"): str(initfile),
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_fricas_runtime()

    assert env.os.environ["FRICAS"] == str(existing)
    assert "FRICAS_COMMAND" not in env.os.environ
    assert "FRICAS_PREFIX" not in env.os.environ
    assert "FRICAS_INITFILE" not in env.os.environ


def test_maxima_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    prefix, fas, command, imagesdir = _maxima_runtime(tmp_path, "companion")
    ecldir = tmp_path / "companion" / "lib" / "ecl-24.5.10"
    runtime_library_dir = tmp_path / "companion" / "lib" / "runtime"
    ecldir.mkdir(parents=True)
    runtime_library_dir.mkdir(parents=True)

    monkeypatch.delenv("MAXIMA", raising=False)
    monkeypatch.delenv("MAXIMA_PREFIX", raising=False)
    monkeypatch.delenv("MAXIMA_FAS", raising=False)
    monkeypatch.delenv("MAXIMA_IMAGESDIR", raising=False)
    monkeypatch.delenv("ECLDIR", raising=False)
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
            ("sagelite_maxima.runtime", "maxima_imagesdir"): imagesdir,
            ("sagelite_maxima.runtime", "ecl_dir"): ecldir,
            ("sagelite_maxima.runtime", "maxima_layout_autotools"): "true",
            ("sagelite_maxima.runtime", "runtime_library_dir"): runtime_library_dir,
        }
        return values.get((module_name, attr_name))

    monkeypatch.setattr(env, "_optional_runtime_value", runtime_value)

    env._bootstrap_sagelite_maxima_runtime()

    assert env.os.environ["MAXIMA"] == str(command)
    assert env.os.environ["MAXIMA_PREFIX"] == str(prefix)
    assert env.os.environ["MAXIMA_FAS"] == str(fas)
    assert env.os.environ["MAXIMA_IMAGESDIR"] == str(imagesdir)
    assert env.os.environ["ECLDIR"] == str(ecldir)
    assert env.os.environ["MAXIMA_LAYOUT_AUTOTOOLS"] == "true"
    assert env.os.environ["LD_LIBRARY_PATH"].split(env.os.pathsep)[0] == str(
        runtime_library_dir
    )


def test_maxima_runtime_prefers_companion_over_configured_paths(monkeypatch, tmp_path):
    prefix, fas, command, imagesdir = _maxima_runtime(tmp_path, "companion")
    ecldir = tmp_path / "companion" / "lib" / "ecl-24.5.10"
    ecldir.mkdir(parents=True)
    (ecldir / "maxima.asd").write_text("maxima asd\n")

    for name in (
        "MAXIMA",
        "MAXIMA_PREFIX",
        "MAXIMA_FAS",
        "MAXIMA_IMAGESDIR",
        "ECLDIR",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "MAXIMA",
        str(tmp_path / "stale" / "bin" / "maxima"),
        raising=False,
    )
    monkeypatch.setattr(
        env.sage.config, "MAXIMA_PREFIX", str(tmp_path / "stale"), raising=False
    )
    monkeypatch.setattr(
        env.sage.config,
        "MAXIMA_FAS",
        str(tmp_path / "stale" / "maxima.fas"),
        raising=False,
    )
    monkeypatch.setattr(
        env.sage.config,
        "MAXIMA_IMAGESDIR",
        str(tmp_path / "stale" / "lib" / "maxima" / "5.47.0"),
        raising=False,
    )

    def runtime_value(module_name, attr_name):
        values = {
            ("sagelite_maxima.runtime", "maxima_command"): command,
            ("sagelite_maxima.runtime", "maxima_prefix"): prefix,
            ("sagelite_maxima.runtime", "maxima_fas"): fas,
            ("sagelite_maxima.runtime", "maxima_imagesdir"): imagesdir,
            ("sagelite_maxima.runtime", "ecl_dir"): ecldir,
        }
        return values.get((module_name, attr_name))

    monkeypatch.setattr(env, "_optional_runtime_value", runtime_value)

    env._bootstrap_sagelite_maxima_runtime()

    assert env.os.environ["MAXIMA"] == str(command)
    assert env.os.environ["MAXIMA_PREFIX"] == str(prefix)
    assert env.os.environ["MAXIMA_FAS"] == str(fas)
    assert env.os.environ["MAXIMA_IMAGESDIR"] == str(imagesdir)
    assert env.os.environ["ECLDIR"] == str(ecldir)


def test_maxima_runtime_keeps_usable_configured_paths(monkeypatch, tmp_path):
    companion_prefix, companion_fas, companion_command, companion_imagesdir = (
        _maxima_runtime(tmp_path, "companion")
    )
    configured_prefix, configured_fas, configured_command, configured_imagesdir = (
        _maxima_runtime(tmp_path, "configured")
    )
    companion_ecldir = tmp_path / "companion" / "lib" / "ecl-24.5.10"
    companion_ecldir.mkdir(parents=True)
    (companion_ecldir / "maxima.asd").write_text("companion maxima asd\n")
    runtime_library_dir = tmp_path / "companion" / "lib" / "runtime"
    runtime_library_dir.mkdir(parents=True)

    for name in (
        "MAXIMA",
        "MAXIMA_PREFIX",
        "MAXIMA_FAS",
        "MAXIMA_IMAGESDIR",
        "ECLDIR",
        "MAXIMA_LAYOUT_AUTOTOOLS",
        "LD_LIBRARY_PATH",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(env.sage.config, "MAXIMA", str(configured_command), raising=False)
    monkeypatch.setattr(
        env.sage.config, "MAXIMA_PREFIX", str(configured_prefix), raising=False
    )
    monkeypatch.setattr(env.sage.config, "MAXIMA_FAS", str(configured_fas), raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "MAXIMA_IMAGESDIR",
        str(configured_imagesdir),
        raising=False,
    )

    def runtime_value(module_name, attr_name):
        values = {
            ("sagelite_maxima.runtime", "maxima_command"): companion_command,
            ("sagelite_maxima.runtime", "maxima_prefix"): companion_prefix,
            ("sagelite_maxima.runtime", "maxima_fas"): companion_fas,
            ("sagelite_maxima.runtime", "maxima_imagesdir"): companion_imagesdir,
            ("sagelite_maxima.runtime", "ecl_dir"): companion_ecldir,
            ("sagelite_maxima.runtime", "maxima_layout_autotools"): "true",
            ("sagelite_maxima.runtime", "runtime_library_dir"): runtime_library_dir,
        }
        return values.get((module_name, attr_name))

    monkeypatch.setattr(env, "_optional_runtime_value", runtime_value)

    env._bootstrap_sagelite_maxima_runtime()

    assert "MAXIMA" not in env.os.environ
    assert "MAXIMA_PREFIX" not in env.os.environ
    assert "MAXIMA_FAS" not in env.os.environ
    assert "MAXIMA_IMAGESDIR" not in env.os.environ
    assert "ECLDIR" not in env.os.environ
    assert "MAXIMA_LAYOUT_AUTOTOOLS" not in env.os.environ
    assert "LD_LIBRARY_PATH" not in env.os.environ


def test_maxima_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    prefix, fas, command, imagesdir = _maxima_runtime(tmp_path, "companion")
    existing_command = tmp_path / "existing-bin" / "maxima"
    existing = tmp_path / "configured"
    existing_fas = tmp_path / "configured" / "maxima.fas"
    existing_imagesdir = tmp_path / "configured" / "lib" / "maxima" / "5.47.0"
    existing_ecldir = existing / "lib" / "ecl"
    existing_command.parent.mkdir()
    existing_command.write_text("#!/bin/sh\n")
    existing_command.chmod(0o755)
    existing_fas.parent.mkdir()
    existing_fas.write_text("existing maxima fas\n")
    existing_imagesdir.mkdir(parents=True)
    existing_ecldir.mkdir(parents=True)
    (existing_ecldir / "maxima.asd").write_text("existing maxima asd\n")

    monkeypatch.setenv("MAXIMA", str(existing_command))
    monkeypatch.setenv("MAXIMA_PREFIX", str(existing))
    monkeypatch.setenv("MAXIMA_FAS", str(existing_fas))
    monkeypatch.setenv("MAXIMA_IMAGESDIR", str(existing_imagesdir))
    monkeypatch.setenv("MAXIMA_LAYOUT_AUTOTOOLS", "true")
    monkeypatch.setenv("ECLDIR", str(existing_ecldir))
    monkeypatch.setenv("LD_LIBRARY_PATH", "/existing/lib")
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
                "maxima_imagesdir": imagesdir,
                "runtime_library_dir": tmp_path / "companion" / "lib" / "runtime",
            }[attr_name]
        ),
    )

    env._bootstrap_sagelite_maxima_runtime()

    assert env.os.environ["MAXIMA"] == str(existing_command)
    assert env.os.environ["MAXIMA_PREFIX"] == str(existing)
    assert env.os.environ["MAXIMA_FAS"] == str(existing_fas)
    assert env.os.environ["MAXIMA_IMAGESDIR"] == str(existing_imagesdir)
    assert env.os.environ["ECLDIR"] == str(existing_ecldir)
    assert env.os.environ["LD_LIBRARY_PATH"].endswith("/existing/lib")


def test_maxima_runtime_replaces_generic_ecldir(monkeypatch, tmp_path):
    prefix, fas, command, imagesdir = _maxima_runtime(tmp_path, "companion")
    generic_ecldir = tmp_path / "generic-ecl" / "lib" / "ecl-24.5.10"
    maxima_ecldir = tmp_path / "companion" / "lib" / "ecl-24.5.10"
    generic_ecldir.mkdir(parents=True)
    maxima_ecldir.mkdir(parents=True)
    (maxima_ecldir / "maxima.asd").write_text("maxima asd\n")

    monkeypatch.setenv("ECLDIR", str(generic_ecldir))
    monkeypatch.delenv("MAXIMA", raising=False)
    monkeypatch.delenv("MAXIMA_PREFIX", raising=False)
    monkeypatch.delenv("MAXIMA_FAS", raising=False)
    monkeypatch.delenv("MAXIMA_IMAGESDIR", raising=False)
    monkeypatch.setattr(env.sage.config, "MAXIMA", "", raising=False)
    monkeypatch.setattr(env.sage.config, "MAXIMA_PREFIX", "", raising=False)
    monkeypatch.setattr(env.sage.config, "MAXIMA_FAS", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_maxima.runtime", "maxima_command"): command,
            ("sagelite_maxima.runtime", "maxima_prefix"): prefix,
            ("sagelite_maxima.runtime", "maxima_fas"): fas,
            ("sagelite_maxima.runtime", "maxima_imagesdir"): imagesdir,
            ("sagelite_maxima.runtime", "ecl_dir"): maxima_ecldir,
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_maxima_runtime()

    assert env.os.environ["ECLDIR"] == str(maxima_ecldir)


def test_maxima_runtime_keeps_ecldir_with_maxima_asd(monkeypatch, tmp_path):
    prefix, fas, command, imagesdir = _maxima_runtime(tmp_path, "companion")
    existing_ecldir = tmp_path / "existing-ecl" / "lib" / "ecl-24.5.10"
    maxima_ecldir = tmp_path / "companion" / "lib" / "ecl-24.5.10"
    existing_ecldir.mkdir(parents=True)
    maxima_ecldir.mkdir(parents=True)
    (existing_ecldir / "maxima.asd").write_text("existing maxima asd\n")
    (maxima_ecldir / "maxima.asd").write_text("companion maxima asd\n")

    monkeypatch.setenv("ECLDIR", str(existing_ecldir))
    monkeypatch.delenv("MAXIMA", raising=False)
    monkeypatch.delenv("MAXIMA_PREFIX", raising=False)
    monkeypatch.delenv("MAXIMA_FAS", raising=False)
    monkeypatch.delenv("MAXIMA_IMAGESDIR", raising=False)
    monkeypatch.setattr(env.sage.config, "MAXIMA", "", raising=False)
    monkeypatch.setattr(env.sage.config, "MAXIMA_PREFIX", "", raising=False)
    monkeypatch.setattr(env.sage.config, "MAXIMA_FAS", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_maxima.runtime", "maxima_command"): command,
            ("sagelite_maxima.runtime", "maxima_prefix"): prefix,
            ("sagelite_maxima.runtime", "maxima_fas"): fas,
            ("sagelite_maxima.runtime", "maxima_imagesdir"): imagesdir,
            ("sagelite_maxima.runtime", "ecl_dir"): maxima_ecldir,
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_maxima_runtime()

    assert env.os.environ["ECLDIR"] == str(existing_ecldir)


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


def test_kenzo_runtime_does_not_mix_companion_fas_with_system_ecl(
    monkeypatch, tmp_path
):
    system_ecldir = tmp_path / "system" / "ecl"
    companion_ecldir = tmp_path / "companion" / "ecl"
    fas = _kenzo_runtime(tmp_path, "companion")
    system_ecldir.mkdir(parents=True)
    companion_ecldir.mkdir(parents=True)

    monkeypatch.delenv("KENZO_FAS", raising=False)
    monkeypatch.setenv("ECLDIR", str(system_ecldir))
    monkeypatch.setattr(
        env.sage.config,
        "KENZO_FAS",
        str(tmp_path / "stale-lib" / "ecl" / "kenzo.fas"),
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_kenzo.runtime", "kenzo_fas"): fas,
            ("sagelite_ecl.runtime", "ecl_dir"): companion_ecldir,
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_kenzo_runtime()

    assert "KENZO_FAS" not in env.os.environ


def test_pari_data_runtime_uses_companion_when_environment_is_missing(monkeypatch, tmp_path):
    data_dir = _pari_data_runtime(tmp_path, "companion")

    monkeypatch.delenv("GP_DATA_DIR", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: data_dir
        if (module_name, attr_name) == ("sagelite_pari_data.runtime", "pari_data_dir")
        else None,
    )

    env._bootstrap_sagelite_pari_data_runtime()

    assert env.os.environ["GP_DATA_DIR"] == str(data_dir)


def test_pari_data_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    companion = _pari_data_runtime(tmp_path, "companion")
    existing = _pari_data_runtime(tmp_path, "existing")

    monkeypatch.setenv("GP_DATA_DIR", str(existing))
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: companion,
    )

    env._bootstrap_sagelite_pari_data_runtime()

    assert env.os.environ["GP_DATA_DIR"] == str(existing)


def test_pari_data_runtime_rejects_incomplete_companion(monkeypatch, tmp_path):
    data_dir = tmp_path / "companion" / "share" / "pari"
    data_dir.mkdir(parents=True)

    monkeypatch.delenv("GP_DATA_DIR", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: data_dir,
    )

    env._bootstrap_sagelite_pari_data_runtime()

    assert "GP_DATA_DIR" not in env.os.environ


def test_pari_script_dir_uses_registered_companion_path(monkeypatch, tmp_path):
    companion = tmp_path / "companion" / "data" / "pari" / "simon"
    companion.mkdir(parents=True)
    (companion / "qfsolve.gp").write_text("qfsolve\n")

    monkeypatch.setattr(env, "sage_data_paths", lambda name: {str(companion.parent)})
    monkeypatch.setattr(env, "SAGE_EXTCODE", str(tmp_path / "missing-ext-data"))

    assert env.pari_script_dir("simon") == companion


def test_meataxe_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    table_dir = _meataxe_runtime(tmp_path, "companion")

    monkeypatch.delenv("MTXLIB", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "MTXLIB",
        str(tmp_path / "stale-share" / "meataxe"),
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: table_dir
        if (module_name, attr_name) == ("sagelite_meataxe.runtime", "meataxe_dir")
        else None,
    )

    env._bootstrap_sagelite_meataxe_runtime()

    assert env.os.environ["MTXLIB"] == str(table_dir)


def test_meataxe_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    companion = _meataxe_runtime(tmp_path, "companion")
    existing = _meataxe_runtime(tmp_path, "existing")

    monkeypatch.setenv("MTXLIB", str(existing))
    monkeypatch.setattr(env.sage.config, "MTXLIB", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: companion,
    )

    env._bootstrap_sagelite_meataxe_runtime()

    assert env.os.environ["MTXLIB"] == str(existing)


def test_meataxe_runtime_rejects_incomplete_companion(monkeypatch, tmp_path):
    table_dir = tmp_path / "companion" / "share" / "meataxe"
    table_dir.mkdir(parents=True)

    monkeypatch.delenv("MTXLIB", raising=False)
    monkeypatch.setattr(env.sage.config, "MTXLIB", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: table_dir,
    )

    env._bootstrap_sagelite_meataxe_runtime()

    assert "MTXLIB" not in env.os.environ


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


def test_lie_runtime_sets_pexpect_command(monkeypatch, tmp_path):
    command = _runtime_executable(tmp_path, "companion", "lie")

    monkeypatch.delenv("SAGE_LIE_COMMAND", raising=False)
    monkeypatch.setattr(env.shutil, "which", lambda program: None)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: (
            str(command)
            if (module_name, attr_name) == ("sagelite_lie.runtime", "lie_command")
            else None
        ),
    )

    env._bootstrap_sagelite_lie_runtime()

    assert env.os.environ["SAGE_LIE_COMMAND"] == str(command)
    assert env.var("SAGE_LIE_COMMAND", "lie") == str(command)


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


def test_lie_runtime_keeps_existing_pexpect_command(monkeypatch, tmp_path):
    existing = _runtime_executable(tmp_path, "existing", "lie")
    companion = _runtime_executable(tmp_path, "companion", "lie")

    monkeypatch.setenv("SAGE_LIE_COMMAND", str(existing))
    monkeypatch.setattr(env.shutil, "which", lambda program: None)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(companion),
    )

    env._bootstrap_sagelite_lie_runtime()

    assert env.os.environ["SAGE_LIE_COMMAND"] == str(existing)


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


def test_mathjax_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    mathjax_dir = _mathjax_runtime(tmp_path, "companion")

    monkeypatch.delenv("MATHJAX_DIR", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "MATHJAX_DIR",
        str(tmp_path / "stale-share" / "mathjax"),
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(mathjax_dir)
        if (module_name, attr_name) == ("sagelite_mathjax_runtime", "mathjax_dir")
        else None,
    )

    env._bootstrap_sagelite_mathjax_runtime()

    assert env.os.environ["MATHJAX_DIR"] == str(mathjax_dir)


def test_mathjax_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    companion = _mathjax_runtime(tmp_path, "companion")
    existing = _mathjax_runtime(tmp_path, "existing")

    monkeypatch.setenv("MATHJAX_DIR", str(existing))
    monkeypatch.setattr(env.sage.config, "MATHJAX_DIR", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(companion)
        if (module_name, attr_name) == ("sagelite_mathjax_runtime", "mathjax_dir")
        else None,
    )

    env._bootstrap_sagelite_mathjax_runtime()

    assert env.os.environ["MATHJAX_DIR"] == str(existing)


def test_mathjax_runtime_rejects_incomplete_companion(monkeypatch, tmp_path):
    mathjax_dir = tmp_path / "companion" / "share" / "mathjax" / "mathjax"
    mathjax_dir.mkdir(parents=True)
    (mathjax_dir / "loader.js").write_text("console.log('loader');\n")

    monkeypatch.delenv("MATHJAX_DIR", raising=False)
    monkeypatch.setattr(env.sage.config, "MATHJAX_DIR", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: str(mathjax_dir)
        if (module_name, attr_name) == ("sagelite_mathjax_runtime", "mathjax_dir")
        else None,
    )

    env._bootstrap_sagelite_mathjax_runtime()

    assert "MATHJAX_DIR" not in env.os.environ


def test_threejs_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    threejs_dir = _threejs_runtime(tmp_path, "companion")

    monkeypatch.delenv("THREEJS_DIR", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "THREEJS_DIR",
        str(tmp_path / "stale-share" / "threejs-sage"),
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: threejs_dir
        if (module_name, attr_name)
        == ("sagelite_threejs_runtime", "threejs_sage_path")
        else None,
    )

    env._bootstrap_sagelite_threejs_runtime()

    assert env.os.environ["THREEJS_DIR"] == str(threejs_dir)


def test_threejs_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    threejs_dir = _threejs_runtime(tmp_path, "companion")
    existing_threejs_dir = _threejs_runtime(tmp_path, "existing")

    monkeypatch.setenv("THREEJS_DIR", str(existing_threejs_dir))
    monkeypatch.setattr(env.sage.config, "THREEJS_DIR", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: threejs_dir,
    )

    env._bootstrap_sagelite_threejs_runtime()

    assert env.os.environ["THREEJS_DIR"] == str(existing_threejs_dir)


def test_threejs_runtime_rejects_incomplete_companion(monkeypatch, tmp_path):
    incomplete = tmp_path / "companion" / "share" / "threejs-sage"
    incomplete.mkdir(parents=True)
    (incomplete / "version").write_text("r124\n")

    monkeypatch.delenv("THREEJS_DIR", raising=False)
    monkeypatch.setattr(env.sage.config, "THREEJS_DIR", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: incomplete,
    )

    env._bootstrap_sagelite_threejs_runtime()

    assert "THREEJS_DIR" not in env.os.environ


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


def test_ecl_runtime_uses_companion_when_config_is_stale(monkeypatch, tmp_path):
    command, ecldir = _ecl_runtime(tmp_path, "companion")

    monkeypatch.delenv("ECL_CONFIG", raising=False)
    monkeypatch.delenv("ECLDIR", raising=False)
    monkeypatch.setattr(
        env.sage.config,
        "ECL_CONFIG",
        str(tmp_path / "stale-bin" / "ecl-config"),
        raising=False,
    )
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_ecl.runtime", "ecl_config_command"): str(command),
            ("sagelite_ecl.runtime", "ecl_dir"): str(ecldir),
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_ecl_runtime()

    assert env.os.environ["ECL_CONFIG"] == str(command)
    assert env.os.environ["ECLDIR"] == str(ecldir)


def test_ecl_runtime_uses_configured_ecldir(monkeypatch, tmp_path):
    command, ecldir = _ecl_runtime(tmp_path, "configured")

    monkeypatch.delenv("ECL_CONFIG", raising=False)
    monkeypatch.delenv("ECLDIR", raising=False)
    monkeypatch.setattr(env.sage.config, "ECL_CONFIG", str(command), raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: None,
    )

    env._bootstrap_sagelite_ecl_runtime()

    assert "ECL_CONFIG" not in env.os.environ
    assert env.os.environ["ECLDIR"] == str(ecldir)


def test_ecl_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    command, ecldir = _ecl_runtime(tmp_path, "companion")
    existing_command, existing_ecldir = _ecl_runtime(tmp_path, "existing")

    monkeypatch.setenv("ECL_CONFIG", str(existing_command))
    monkeypatch.setenv("ECLDIR", str(existing_ecldir))
    monkeypatch.setattr(env.sage.config, "ECL_CONFIG", "", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_ecl.runtime", "ecl_config_command"): str(command),
            ("sagelite_ecl.runtime", "ecl_dir"): str(ecldir),
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_ecl_runtime()

    assert env.os.environ["ECL_CONFIG"] == str(existing_command)
    assert env.os.environ["ECLDIR"] == str(existing_ecldir)


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


def test_tachyon_runtime_uses_companion_when_command_is_missing(monkeypatch, tmp_path):
    command = _tachyon_runtime(tmp_path, "companion")

    monkeypatch.delenv("TACHYON", raising=False)
    monkeypatch.setattr(env.shutil, "which", lambda name: None)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: command
        if (module_name, attr_name) == ("sagelite_tachyon.runtime", "executable_path")
        else None,
    )

    env._bootstrap_sagelite_tachyon_runtime()

    assert env.os.environ["TACHYON"] == str(command)


def test_tachyon_runtime_keeps_existing_environment(monkeypatch, tmp_path):
    command = _tachyon_runtime(tmp_path, "companion")
    existing_command = _tachyon_runtime(tmp_path, "existing")

    monkeypatch.setenv("TACHYON", str(existing_command))
    monkeypatch.setattr(env.shutil, "which", lambda name: None)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: command,
    )

    env._bootstrap_sagelite_tachyon_runtime()

    assert env.os.environ["TACHYON"] == str(existing_command)


def test_tachyon_runtime_keeps_system_command(monkeypatch, tmp_path):
    command = _tachyon_runtime(tmp_path, "companion")
    system_command = _tachyon_runtime(tmp_path, "system")

    monkeypatch.delenv("TACHYON", raising=False)
    monkeypatch.setattr(env.shutil, "which", lambda name: str(system_command))
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: command,
    )

    env._bootstrap_sagelite_tachyon_runtime()

    assert "TACHYON" not in env.os.environ


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
    (prefix / "genposetg").write_text("#!/bin/sh\n")
    (prefix / "genposetg").chmod(0o755)

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
    monkeypatch.setattr(
        env,
        "_command_starts",
        lambda path: str(path).startswith(str(prefix)),
    )

    env._bootstrap_sagelite_nauty_runtime()

    assert env.os.environ["SAGE_NAUTY_BINS_PREFIX"] == str(prefix) + env.os.sep


def test_nauty_runtime_prefers_usable_system_prefix(monkeypatch, tmp_path):
    companion = _runtime_bin_prefix(tmp_path, "companion", "geng")
    (companion / "genposetg").write_text("#!/bin/sh\n")
    (companion / "genposetg").chmod(0o755)

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
        lambda module_name, attr_name: str(companion) + env.os.sep
        if (module_name, attr_name) == ("sagelite_nauty.runtime", "bin_prefix")
        else None,
    )
    monkeypatch.setattr(
        env,
        "_command_starts",
        lambda path: str(path).startswith("/usr/bin/nauty-"),
    )

    env._bootstrap_sagelite_nauty_runtime()

    assert env.os.environ["SAGE_NAUTY_BINS_PREFIX"] == "/usr/bin/nauty-"


def test_nauty_runtime_ignores_broken_companion(monkeypatch, tmp_path):
    prefix = _runtime_bin_prefix(tmp_path, "companion", "geng")
    (prefix / "genposetg").write_text("#!/bin/sh\n")
    (prefix / "genposetg").chmod(0o755)

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
    monkeypatch.setattr(env, "_command_starts", lambda path: False)

    env._bootstrap_sagelite_nauty_runtime()

    assert "SAGE_NAUTY_BINS_PREFIX" not in env.os.environ


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


def test_singular_runtime_uses_companion_when_environment_is_missing(
    monkeypatch, tmp_path
):
    root, default_dir = _singular_runtime(tmp_path, "companion")

    monkeypatch.delenv("SINGULAR_ROOT_DIR", raising=False)
    monkeypatch.delenv("SINGULAR_DEFAULT_DIR", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_singular_runtime.runtime", "singular_root_dir"): root,
            ("sagelite_singular_runtime.runtime", "singular_default_dir"): default_dir,
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_singular_runtime()

    assert env.os.environ["SINGULAR_ROOT_DIR"] == str(root)
    assert env.os.environ["SINGULAR_DEFAULT_DIR"] == str(default_dir)


def test_singular_runtime_rejects_incomplete_companion(monkeypatch, tmp_path):
    root = tmp_path / "companion" / "singular"
    default_dir = root / "share" / "singular"
    default_dir.mkdir(parents=True)

    monkeypatch.delenv("SINGULAR_ROOT_DIR", raising=False)
    monkeypatch.delenv("SINGULAR_DEFAULT_DIR", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_singular_runtime.runtime", "singular_root_dir"): root,
            ("sagelite_singular_runtime.runtime", "singular_default_dir"): default_dir,
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_singular_runtime()

    assert "SINGULAR_ROOT_DIR" not in env.os.environ
    assert "SINGULAR_DEFAULT_DIR" not in env.os.environ


def test_info_runtime_prepends_companion_paths(monkeypatch, tmp_path):
    command, info_dir = _info_runtime(tmp_path, "companion")
    existing_bin = tmp_path / "existing" / "bin"
    existing_info = tmp_path / "existing" / "info"
    existing_bin.mkdir(parents=True)
    existing_info.mkdir(parents=True)

    monkeypatch.setenv("PATH", str(existing_bin))
    monkeypatch.setenv("INFOPATH", str(existing_info))
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_info.runtime", "executable_path"): command,
            ("sagelite_info.runtime", "info_dir"): info_dir,
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_info_runtime()

    assert env.os.environ["PATH"].split(env.os.pathsep) == [
        str(command.parent),
        str(existing_bin),
    ]
    assert env.os.environ["INFOPATH"].split(env.os.pathsep) == [
        str(info_dir),
        str(existing_info),
    ]


def test_info_runtime_rejects_incomplete_companion(monkeypatch, tmp_path):
    command, info_dir = _info_runtime(tmp_path, "companion")
    (info_dir / "singular.info").unlink()

    monkeypatch.setenv("PATH", "")
    monkeypatch.delenv("INFOPATH", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_info.runtime", "executable_path"): command,
            ("sagelite_info.runtime", "info_dir"): info_dir,
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_info_runtime()

    assert env.os.environ["PATH"] == str(command.parent)
    assert "INFOPATH" not in env.os.environ


def test_graphviz_runtime_prepends_companion_subprocess_paths(monkeypatch, tmp_path):
    dot, bin_dir, lib_dir, plugin_dir = _graphviz_runtime(tmp_path, "companion")
    existing_bin = tmp_path / "existing" / "bin"
    existing_lib = tmp_path / "existing" / "lib"
    existing_plugins = tmp_path / "existing" / "graphviz"
    existing_bin.mkdir(parents=True)
    existing_lib.mkdir(parents=True)
    existing_plugins.mkdir(parents=True)

    monkeypatch.setenv("PATH", str(existing_bin))
    monkeypatch.setenv("LD_LIBRARY_PATH", str(existing_lib))
    monkeypatch.setenv("GV_PLUGIN_PATH", str(existing_plugins))
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_graphviz.runtime", "executable_path"): dot,
            ("sagelite_graphviz.runtime", "bin_dir"): bin_dir,
            ("sagelite_graphviz.runtime", "library_dir"): lib_dir,
            ("sagelite_graphviz.runtime", "plugin_dir"): plugin_dir,
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_graphviz_runtime()

    assert env.os.environ["PATH"].split(env.os.pathsep) == [
        str(bin_dir),
        str(existing_bin),
    ]
    assert env.os.environ["LD_LIBRARY_PATH"].split(env.os.pathsep) == [
        str(lib_dir),
        str(existing_lib),
    ]
    assert env.os.environ["GV_PLUGIN_PATH"].split(env.os.pathsep) == [
        str(plugin_dir),
        str(existing_plugins),
    ]


def test_graphviz_runtime_keeps_existing_programs(monkeypatch, tmp_path):
    dot, bin_dir, lib_dir, plugin_dir = _graphviz_runtime(tmp_path, "companion")
    existing_bin = tmp_path / "existing" / "bin"
    existing_bin.mkdir(parents=True)
    for program in ("dot", "neato", "twopi"):
        command = existing_bin / program
        command.write_text("#!/bin/sh\n")
        command.chmod(0o755)

    monkeypatch.setenv("PATH", str(existing_bin))
    monkeypatch.delenv("LD_LIBRARY_PATH", raising=False)
    monkeypatch.delenv("GV_PLUGIN_PATH", raising=False)
    monkeypatch.setattr(
        env,
        "_optional_runtime_value",
        lambda module_name, attr_name: {
            ("sagelite_graphviz.runtime", "executable_path"): dot,
            ("sagelite_graphviz.runtime", "bin_dir"): bin_dir,
            ("sagelite_graphviz.runtime", "library_dir"): lib_dir,
            ("sagelite_graphviz.runtime", "plugin_dir"): plugin_dir,
        }.get((module_name, attr_name)),
    )

    env._bootstrap_sagelite_graphviz_runtime()

    assert env.os.environ["PATH"] == str(existing_bin)
    assert "LD_LIBRARY_PATH" not in env.os.environ
    assert "GV_PLUGIN_PATH" not in env.os.environ
