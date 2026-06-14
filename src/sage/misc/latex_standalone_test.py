import importlib
import importlib.util
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "misc" / "latex_standalone.py"
spec = importlib.util.spec_from_file_location(
    "sage.misc.latex_standalone", MODULE_PATH
)
latex_standalone_module = importlib.util.module_from_spec(spec)
sys.modules["sage.misc.latex_standalone"] = latex_standalone_module
spec.loader.exec_module(latex_standalone_module)

Standalone = latex_standalone_module.Standalone


def test_svg_uses_pdf2svg_feature_executable(monkeypatch, tmp_path):
    pdf2svg_module = importlib.import_module("sage.features.pdf2svg")
    pdf2svg = tmp_path / "pdf2svg"
    pdf2svg.write_text("#!/bin/sh\n")
    pdf2svg.chmod(0o755)

    class FakePdf2Svg:
        def require(self):
            return None

        def absolute_filename(self):
            return os.fspath(pdf2svg)

    commands = []
    svg = tmp_path / "input.svg"

    class FakeResult:
        returncode = 0
        stderr = ""
        stdout = ""

        def __init__(self, args):
            self.args = args

        def check_returncode(self):
            return None

    def fake_run(command, capture_output, text):
        commands.append(command)
        Path(command[-1]).write_text("<svg/>\n")
        return FakeResult(command)

    monkeypatch.setattr(pdf2svg_module, "pdf2svg", FakePdf2Svg)
    monkeypatch.setattr(latex_standalone_module, "run", fake_run)
    monkeypatch.setenv("PATH", "")

    document = Standalone("Hello")
    monkeypatch.setattr(
        document,
        "pdf",
        lambda filename=None, view=False: str(tmp_path / "input.pdf"),
    )

    assert document.svg(
        filename=str(svg), view=False, program="pdf2svg"
    ) == os.fspath(svg)
    assert commands[0][0] == os.fspath(pdf2svg)


def test_eps_uses_pdftocairo_feature_executable(monkeypatch, tmp_path):
    poppler_module = importlib.import_module("sage.features.poppler")
    pdftocairo = tmp_path / "pdftocairo"
    pdftocairo.write_text("#!/bin/sh\n")
    pdftocairo.chmod(0o755)

    class FakePdfToCairo:
        def require(self):
            return None

        def absolute_filename(self):
            return os.fspath(pdftocairo)

    commands = []
    eps = tmp_path / "input.eps"

    class FakeResult:
        returncode = 0
        stderr = ""
        stdout = ""

        def __init__(self, args):
            self.args = args

        def check_returncode(self):
            return None

    def fake_run(command, capture_output, text):
        commands.append(command)
        Path(command[-1]).write_text("%!PS\n")
        return FakeResult(command)

    monkeypatch.setattr(poppler_module, "pdftocairo", FakePdfToCairo)
    monkeypatch.setattr(latex_standalone_module, "run", fake_run)
    monkeypatch.setenv("PATH", "")

    document = Standalone("Hello")
    monkeypatch.setattr(
        document,
        "pdf",
        lambda filename=None, view=False: str(tmp_path / "input.pdf"),
    )

    assert document.eps(
        filename=str(eps), view=False, program="pdftocairo"
    ) == os.fspath(eps)
    assert commands[0][0] == os.fspath(pdftocairo)
