import importlib.util
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "imagemagick.py"
spec = importlib.util.spec_from_file_location("sage.features.imagemagick", MODULE_PATH)
imagemagick_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.imagemagick"] = imagemagick_module
spec.loader.exec_module(imagemagick_module)

Magick = imagemagick_module.Magick


def test_magick_functional_uses_sagelite_companion_executable(monkeypatch, tmp_path):
    package = tmp_path / "sagelite_imagemagick"
    bindir = package / "data" / "bin"
    executable = bindir / "magick"
    bindir.mkdir(parents=True)
    executable.write_text("#!/bin/sh\nexit 0\n")
    executable.chmod(0o755)
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n\n"
        "def executable_path(program='magick'):\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / program\n"
    )

    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "")
    sys.modules.pop("sagelite_imagemagick", None)
    sys.modules.pop("sagelite_imagemagick.runtime", None)

    feature = Magick()

    assert feature.absolute_filename() == os.fspath(executable)
    assert bool(feature.is_functional())
