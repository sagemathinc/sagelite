import importlib.util
import os
import subprocess
import sys
import types
from pathlib import Path

import sage.features


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "features" / "ffmpeg.py"
spec = importlib.util.spec_from_file_location("sage.features.ffmpeg", MODULE_PATH)
ffmpeg_module = importlib.util.module_from_spec(spec)
sys.modules["sage.features.ffmpeg"] = ffmpeg_module
spec.loader.exec_module(ffmpeg_module)

FFmpeg = ffmpeg_module.FFmpeg


def test_ffmpeg_executable_discovers_imageio_ffmpeg_runtime(monkeypatch, tmp_path):
    executable = tmp_path / "ffmpeg"
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)
    imageio_ffmpeg = types.ModuleType("imageio_ffmpeg")
    imageio_ffmpeg.get_ffmpeg_exe = lambda: os.fspath(executable)

    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    monkeypatch.setitem(sys.modules, "imageio_ffmpeg", imageio_ffmpeg)

    feature = FFmpeg()

    assert feature.absolute_filename() == os.fspath(executable)


def test_ffmpeg_functional_check_uses_imageio_ffmpeg_runtime(
    monkeypatch, tmp_path
):
    executable = tmp_path / "ffmpeg"
    executable.write_text("#!/bin/sh\n")
    executable.chmod(0o755)
    imageio_ffmpeg = types.ModuleType("imageio_ffmpeg")
    imageio_ffmpeg.get_ffmpeg_exe = lambda: os.fspath(executable)
    calls = []

    def fake_run(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setenv("PATH", "")
    monkeypatch.setattr(sage.features, "SAGE_LOCAL", None)
    monkeypatch.setitem(sys.modules, "imageio_ffmpeg", imageio_ffmpeg)
    monkeypatch.setattr(subprocess, "run", fake_run)

    assert FFmpeg().is_functional()
    assert calls
    assert all(command[0] == os.fspath(executable) for command in calls)
