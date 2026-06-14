import importlib
import importlib.util
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "misc" / "latex.py"
spec = importlib.util.spec_from_file_location("sage.misc.latex", MODULE_PATH)
latex_module = importlib.util.module_from_spec(spec)
sys.modules["sage.misc.latex"] = latex_module
spec.loader.exec_module(latex_module)


def test_run_latex_uses_dvipng_feature_executable(monkeypatch, tmp_path):
    dvipng_module = importlib.import_module("sage.features.dvipng")
    latex_features = importlib.import_module("sage.features.latex")
    imagemagick_module = importlib.import_module("sage.features.imagemagick")
    dvipng = tmp_path / "dvipng"
    dvipng.write_text("#!/bin/sh\n")
    dvipng.chmod(0o755)

    class FakeLatex:
        def require(self):
            return None

    class FakeDvipng:
        def is_present(self):
            return True

        def absolute_filename(self):
            return os.fspath(dvipng)

    class FakeImageMagick:
        def is_present(self):
            return False

    class FakeMagick:
        def absolute_filename(self):
            return os.fspath(tmp_path / "magick")

    commands = []

    def fake_call(command, stdout, stderr, cwd):
        commands.append(command)
        if command[0] == os.fspath(dvipng):
            Path(cwd, command[-1]).write_text("png\n")
        return 0

    tex = tmp_path / "input.tex"
    tex.write_text("\\documentclass{article}\\begin{document}x\\end{document}\n")

    monkeypatch.setattr(latex_features, "latex", FakeLatex)
    monkeypatch.setattr(dvipng_module, "dvipng", FakeDvipng)
    monkeypatch.setattr(imagemagick_module, "ImageMagick", FakeImageMagick)
    monkeypatch.setattr(imagemagick_module, "Magick", FakeMagick)
    monkeypatch.setattr(latex_module, "call", fake_call)
    monkeypatch.setenv("PATH", "")

    assert latex_module._run_latex_(os.fspath(tex), engine="latex", png=True) == "dvi"
    assert commands[1][0] == os.fspath(dvipng)
