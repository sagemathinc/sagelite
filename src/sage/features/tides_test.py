import importlib.util
import os
import sys
from pathlib import Path

import sage.env
from sage.features import _trivial_unique_representation_cache


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "tides.py"
spec = importlib.util.spec_from_file_location("sage.features.tides", MODULE_PATH)
tides_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.tides"] = tides_module
spec.loader.exec_module(tides_module)

Tides = tides_module.Tides


def _write_tides_runtime(tmp_path, *, complete=True):
    package = tmp_path / "sagelite_tides"
    include = package / "data" / "include"
    lib = package / "data" / "lib"
    include.mkdir(parents=True)
    lib.mkdir(parents=True)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def data_dir():\n"
        "    return Path(__file__).resolve().parent / 'data'\n\n"
        "def include_dir():\n"
        "    return data_dir() / 'include'\n\n"
        "def library_path():\n"
        "    return data_dir() / 'lib' / 'libTIDES.a'\n"
    )
    (include / "minc_tides.h").write_text("/* min tides */\n")
    if complete:
        (include / "mp_tides.h").write_text("/* mp tides */\n")
        (lib / "libTIDES.a").write_text("!<arch>\n")
    return package


def test_tides_feature_discovers_sagelite_companion(monkeypatch, tmp_path):
    _write_tides_runtime(tmp_path)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setattr(sage.env, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_tides", None)
    sys.modules.pop("sagelite_tides.runtime", None)
    _trivial_unique_representation_cache.clear()

    assert Tides().is_present()


def test_tides_feature_rejects_incomplete_sagelite_companion(monkeypatch, tmp_path):
    _write_tides_runtime(tmp_path, complete=False)

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setattr(sage.env, "SAGE_LOCAL", None)
    sys.modules.pop("sagelite_tides", None)
    sys.modules.pop("sagelite_tides.runtime", None)
    _trivial_unique_representation_cache.clear()

    presence = Tides().is_present()

    assert not presence
    assert "mp_tides.h" in presence.reason
    assert "libTIDES.a" in presence.reason


def test_tides_feature_accepts_sage_local_runtime(monkeypatch, tmp_path):
    prefix = tmp_path / "prefix"
    include = prefix / "include"
    lib = prefix / "lib"
    include.mkdir(parents=True)
    lib.mkdir()
    (include / "minc_tides.h").write_text("/* min tides */\n")
    (include / "mp_tides.h").write_text("/* mp tides */\n")
    (lib / "libTIDES.a").write_text("!<arch>\n")

    monkeypatch.setattr(sage.env, "SAGE_LOCAL", os.fspath(prefix))
    sys.modules.pop("sagelite_tides", None)
    sys.modules.pop("sagelite_tides.runtime", None)
    _trivial_unique_representation_cache.clear()

    assert Tides().is_present()
