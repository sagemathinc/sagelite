import importlib.util
import os
import sys
from pathlib import Path

import sage.env


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "threejs.py"
spec = importlib.util.spec_from_file_location("sage.features.threejs", MODULE_PATH)
threejs_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.threejs"] = threejs_module
spec.loader.exec_module(threejs_module)

Threejs = threejs_module.Threejs


def test_threejs_feature_uses_companion_version_file(monkeypatch, tmp_path):
    threejs_dir = tmp_path / "threejs-sage"
    version_dir = threejs_dir / "r124"
    version_dir.mkdir(parents=True)
    (threejs_dir / "version").write_text("r124\n", encoding="utf-8")
    (version_dir / "three.min.js").write_text(
        "console.log('three');\n", encoding="utf-8"
    )

    monkeypatch.setattr(sage.env, "SAGE_EXTCODE", os.fspath(tmp_path / "extcode"))
    monkeypatch.setattr(sage.env, "THREEJS_DIR", "")
    monkeypatch.setattr(
        sage.env,
        "_optional_runtime_value",
        lambda module_name, attr_name: os.fspath(threejs_dir)
        if (module_name, attr_name)
        == ("sagelite_threejs_runtime", "threejs_sage_path")
        else None,
    )
    monkeypatch.setattr(
        sage.env,
        "sage_data_paths",
        lambda name="": {os.fspath(threejs_dir)} if name == "threejs-sage" else set(),
    )

    feature = Threejs()

    assert feature.required_version() == "r124"
    assert feature.is_present()
