from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_runner():
    path = ROOT / "tools" / "run-installed-wheel-doctests.py"
    spec = importlib.util.spec_from_file_location("run_installed_wheel_doctests", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_runner_uses_short_installed_doctest_defaults(monkeypatch, tmp_path):
    runner = _load_runner()
    monkeypatch.setattr(runner, "_timestamp", lambda: "20260616-010203")
    commands = []

    def fake_run(command, check, text, env):
        commands.append(command)
        assert env["PYTHONNOUSERSITE"] == "1"
        assert "PYTHONPATH" not in env
        assert env["PATH"].split(os.pathsep)[0] == str(Path(sys.executable).parent)
        if command[2] == "sage.doctest":
            log_path = Path(command[5])
            stats_path = Path(command[7])
            log_path.write_text("Running doctests\n", encoding="utf-8")
            stats_path.write_text("{}\n", encoding="utf-8")
            return subprocess.CompletedProcess(command, 0)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    exit_code = runner.main(["--output-dir", str(tmp_path)])

    assert exit_code == 0
    assert commands[0] == [
        sys.executable,
        "-m",
        "sage.doctest",
        "--installed",
        "--logfile",
        str(tmp_path / "doctest-installed-short-20260616-010203.log"),
        "--stats-path",
        str(tmp_path / "doctest-installed-short-20260616-010203.json"),
        "--optional",
        "sage,optional",
        "-p",
        "1",
        "--short",
        "300",
        "--only-errors",
    ]
    assert commands[1] == [
        sys.executable,
        str(ROOT / "tools" / "analyze-doctest-log.py"),
        "--log",
        str(tmp_path / "doctest-installed-short-20260616-010203.log"),
        "--json-out",
        str(tmp_path / "doctest-installed-short-20260616-010203.analysis.json"),
        "--md-out",
        str(tmp_path / "doctest-installed-short-20260616-010203.analysis.md"),
        "--stats",
        str(tmp_path / "doctest-installed-short-20260616-010203.json"),
    ]


def test_runner_passes_through_extra_doctest_args(monkeypatch, tmp_path):
    runner = _load_runner()
    monkeypatch.setattr(runner, "_timestamp", lambda: "20260616-020304")
    commands = []

    def fake_run(command, check, text, env):
        commands.append(command)
        if command[2] == "sage.doctest":
            Path(command[5]).write_text("Running doctests\n", encoding="utf-8")
            Path(command[7]).write_text("{}\n", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    exit_code = runner.main(
        [
            "--output-dir",
            str(tmp_path),
            "--label",
            "Probe Maxima",
            "--short",
            "45",
            "--optional",
            "sage,optional,external",
            "--nthreads",
            "2",
            "--show-passes",
            "--",
            "--probe",
            "maxima",
            "--hide",
            "gap",
        ]
    )

    assert exit_code == 0
    assert commands[0] == [
        sys.executable,
        "-m",
        "sage.doctest",
        "--installed",
        "--logfile",
        str(tmp_path / "doctest-installed-probe-maxima-20260616-020304.log"),
        "--stats-path",
        str(tmp_path / "doctest-installed-probe-maxima-20260616-020304.json"),
        "--optional",
        "sage,optional,external",
        "-p",
        "2",
        "--short",
        "45",
        "--probe",
        "maxima",
        "--hide",
        "gap",
    ]


def test_runner_can_omit_short_flag_for_full_runs(monkeypatch, tmp_path):
    runner = _load_runner()
    monkeypatch.setattr(runner, "_timestamp", lambda: "20260616-030405")
    commands = []

    def fake_run(command, check, text, env):
        commands.append(command)
        if command[2] == "sage.doctest":
            Path(command[5]).write_text("Running doctests\n", encoding="utf-8")
            Path(command[7]).write_text("{}\n", encoding="utf-8")
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    exit_code = runner.main(["--output-dir", str(tmp_path), "--full"])

    assert exit_code == 0
    assert "--short" not in commands[0]
    assert str(tmp_path / "doctest-installed-full-20260616-030405.log") in commands[0]


def test_runner_still_analyzes_logs_when_stats_file_is_missing(monkeypatch, tmp_path):
    runner = _load_runner()
    monkeypatch.setattr(runner, "_timestamp", lambda: "20260616-040506")
    commands = []

    def fake_run(command, check, text, env):
        commands.append(command)
        if command[2] == "sage.doctest":
            Path(command[5]).write_text("Running doctests\n", encoding="utf-8")
            return subprocess.CompletedProcess(command, 1)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    exit_code = runner.main(["--output-dir", str(tmp_path)])

    assert exit_code == 1
    assert commands[1] == [
        sys.executable,
        str(ROOT / "tools" / "analyze-doctest-log.py"),
        "--log",
        str(tmp_path / "doctest-installed-short-20260616-040506.log"),
        "--json-out",
        str(tmp_path / "doctest-installed-short-20260616-040506.analysis.json"),
        "--md-out",
        str(tmp_path / "doctest-installed-short-20260616-040506.analysis.md"),
    ]


def test_runner_prioritizes_analyzer_failure_exit_code(monkeypatch, tmp_path):
    runner = _load_runner()
    monkeypatch.setattr(runner, "_timestamp", lambda: "20260616-050607")
    calls = {"count": 0}

    def fake_run(command, check, text, env):
        calls["count"] += 1
        if calls["count"] == 1:
            Path(command[5]).write_text("Running doctests\n", encoding="utf-8")
            Path(command[7]).write_text("{}\n", encoding="utf-8")
            return subprocess.CompletedProcess(command, 1)
        return subprocess.CompletedProcess(command, 7)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    exit_code = runner.main(["--output-dir", str(tmp_path)])

    assert exit_code == 7


def test_runner_sanitizes_installed_doctest_environment(monkeypatch):
    runner = _load_runner()
    monkeypatch.setenv("PATH", "/usr/bin")
    monkeypatch.setenv("PYTHONPATH", "/home/user/sage/src")
    monkeypatch.delenv("PYTHONNOUSERSITE", raising=False)

    env = runner.build_clean_environment("/scratch/install/bin/python")

    assert env["PATH"] == f"/scratch/install/bin{os.pathsep}/usr/bin"
    assert env["PYTHONNOUSERSITE"] == "1"
    assert "PYTHONPATH" not in env
