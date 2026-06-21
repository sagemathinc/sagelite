from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_validator():
    path = ROOT / "tools" / "validate-sagelite-wheelhouse.py"
    spec = importlib.util.spec_from_file_location("validate_sagelite_wheelhouse", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_builds_fresh_install_and_full_validation_commands(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    install_dir = tmp_path / "install"
    output_dir = tmp_path / "validation"
    commands = []

    def fake_run(command, env):
        commands.append(command)
        assert env["PYTHONNOUSERSITE"] == "1"
        assert "PYTHONPATH" not in env
        assert "LD_LIBRARY_PATH" not in env
        return subprocess.CompletedProcess(command, 0)

    validator._timestamp = lambda: "20260621-010203"
    validator._run = fake_run

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--install-dir",
            str(install_dir),
            "--output-dir",
            str(output_dir),
            "--label",
            "cibw-proof",
            "--python",
            "/opt/python/cp312/bin/python",
            "--full",
            "--nthreads",
            "4",
            "--manifest-compiled-limit",
            "250",
            "--",
            "--optional",
            "sage,optional,external",
        ]
    )

    assert exit_code == 0
    venv_python = install_dir / "bin" / "python"
    assert commands == [
        ["/opt/python/cp312/bin/python", "-m", "venv", os.fspath(install_dir)],
        [os.fspath(venv_python), "-m", "pip", "install", "-U", "pip"],
        [
            os.fspath(venv_python),
            "-m",
            "pip",
            "install",
            "--no-index",
            "--find-links",
            os.fspath(wheelhouse.resolve()),
            "sagelite[all-needed-extras]",
        ],
        [os.fspath(venv_python), "-m", "pip", "check"],
        [
            os.fspath(venv_python),
            os.fspath(ROOT / "tools" / "run-installed-wheel-doctests.py"),
            "--python",
            os.fspath(venv_python),
            "--output-dir",
            os.fspath(output_dir),
            "--label",
            "cibw-proof",
            "--runtime-summary",
            "--selftest",
            "--nthreads",
            "4",
            "--full",
            "--manifest-compiled-limit",
            "250",
            "--wheelhouse",
            os.fspath(wheelhouse.resolve()),
            "--",
            "--optional",
            "sage,optional,external",
        ],
    ]


def test_defaults_use_scratch_timestamped_paths_and_short_validation(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    commands = []

    def fake_run(command, env):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0)

    validator._timestamp = lambda: "20260621-020304"
    validator._run = fake_run

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--package",
            "sagelite",
        ]
    )

    assert exit_code == 0
    install_dir = tmp_path / "install-20260621-020304"
    output_dir = tmp_path / "validation-20260621-020304"
    venv_python = install_dir / "bin" / "python"
    assert commands[2][-1] == "sagelite"
    assert commands[4] == [
        os.fspath(venv_python),
        os.fspath(ROOT / "tools" / "run-installed-wheel-doctests.py"),
        "--python",
        os.fspath(venv_python),
        "--output-dir",
        os.fspath(output_dir),
        "--label",
        "repaired-wheel-20260621-020304",
        "--runtime-summary",
        "--selftest",
        "--nthreads",
        "1",
        "--short",
        "300",
        "--manifest-compiled-limit",
        "200",
        "--wheelhouse",
        os.fspath(wheelhouse.resolve()),
    ]


def test_stops_after_failed_step(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    commands = []

    def fake_run(command, env):
        commands.append(command)
        return subprocess.CompletedProcess(command, 12 if len(commands) == 3 else 0)

    validator._timestamp = lambda: "20260621-030405"
    validator._run = fake_run

    exit_code = validator.main(
        ["--wheelhouse", str(wheelhouse), "--work-dir", str(tmp_path)]
    )

    assert exit_code == 12
    assert len(commands) == 3


def test_missing_wheelhouse_fails_before_creating_commands(tmp_path):
    validator = _load_validator()
    commands = []
    validator._run = lambda command, env: commands.append(command)

    try:
        validator.main(["--wheelhouse", str(tmp_path / "missing")])
    except FileNotFoundError as exc:
        assert "wheelhouse directory does not exist" in str(exc)
    else:
        raise AssertionError("expected FileNotFoundError")

    assert commands == []
