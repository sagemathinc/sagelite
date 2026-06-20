from __future__ import annotations

import argparse
import importlib.util
import json
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
    monkeypatch.setenv("LD_LIBRARY_PATH", "/project/local/lib")
    commands = []

    def fake_run(command, check, text, env):
        commands.append(command)
        assert env["PYTHONNOUSERSITE"] == "1"
        assert "PYTHONPATH" not in env
        assert "LD_LIBRARY_PATH" not in env
        assert env["PATH"].split(os.pathsep)[0] == str(
            Path(sys.executable).resolve().parent
        )
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
    monkeypatch.setenv("LD_LIBRARY_PATH", "/project/local/lib")
    monkeypatch.delenv("PYTHONNOUSERSITE", raising=False)

    env = runner.build_clean_environment("/scratch/install/bin/python")

    assert env["PATH"] == f"/scratch/install/bin{os.pathsep}/usr/bin"
    assert env["PYTHONNOUSERSITE"] == "1"
    assert "PYTHONPATH" not in env
    assert "LD_LIBRARY_PATH" not in env


def test_manual_companion_packages_parse_hyphenated_wheel_names():
    runner = _load_runner()
    args = argparse.Namespace(
        installed_wheel=[
            Path("sagelite-10.9.post1-cp312-cp312-linux_x86_64.whl"),
            Path("sagelite-gap-runtime-10.9-py3-none-any.whl"),
            Path("sagelite_maxima_runtime-10.9.post13-py3-none-any.whl"),
            Path("not-a-wheel.txt"),
        ]
    )

    assert runner._manual_companion_packages(args) == [
        "sagelite-gap-runtime",
        "sagelite-maxima-runtime",
    ]


def test_runner_runtime_summary_records_manifest_and_wheel_inputs(monkeypatch, tmp_path):
    runner = _load_runner()
    monkeypatch.setattr(runner, "_timestamp", lambda: "20260616-060708")
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (wheelhouse / "sagelite-10.9.post1-cp312-cp312-linux_x86_64.whl").write_text(
        "",
        encoding="utf-8",
    )
    gap_wheel = wheelhouse / "sagelite_gap_runtime-10.9-py3-none-any.whl"
    gap_wheel.write_text("", encoding="utf-8")
    commands = []

    def fake_run(command, check, text, env):
        commands.append(command)
        assert env["PYTHONNOUSERSITE"] == "1"
        assert "PYTHONPATH" not in env
        if command[1] == str(runner.MANIFEST):
            Path(command[6]).write_text(
                json.dumps(
                    {
                        "schema": "manifest",
                        "packages": [
                            {
                                "name": "sagelite",
                                "version": "10.9.post1",
                                "location": "/scratch/install/lib/python3.12/site-packages",
                            },
                            {
                                "name": "sagelite-gap-runtime",
                                "version": "10.9",
                                "location": "/scratch/install/lib/python3.12/site-packages",
                            },
                            {
                                "name": "sagelite_maxima_runtime",
                                "version": "10.9.post13",
                                "location": "/scratch/install/lib/python3.12/site-packages",
                            },
                            {
                                "name": "numpy",
                                "version": "2.2.0",
                                "location": "/scratch/install/lib/python3.12/site-packages",
                            },
                        ],
                        "features": {
                            "features": [
                                {"name": "gap", "present": True},
                                {"name": "gap_package_guava", "present": False},
                                {
                                    "name": "fricas",
                                    "present": None,
                                    "exception": "RuntimeError: probe failed",
                                },
                            ]
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            return subprocess.CompletedProcess(command, 0)
        if command[2] == "sage.doctest":
            Path(command[5]).write_text("Running doctests\n", encoding="utf-8")
            Path(command[7]).write_text("{}\n", encoding="utf-8")
            return subprocess.CompletedProcess(command, 0)
        if command[1] == str(runner.ANALYZER):
            Path(command[5]).write_text(
                json.dumps(
                    {
                        "totals": {"modules_failed": 2, "modules_seen": 10},
                        "category_counts": {"optional-external": 2},
                        "fingerprint_counts": {"missing-executable": 2},
                        "actionable_buckets": [
                            {
                                "category": "optional-external",
                                "fingerprint": "missing-executable",
                                "suggested_package": "sagelite-cddlib-runtime",
                                "count": 2,
                                "failed_examples": 2,
                                "evidence": "standalone executable not found",
                                "modules": [
                                    "sage.geometry.polyhedron.backend_cdd",
                                    "sage.geometry.polyhedron.backend_cdd_rdf",
                                ],
                            }
                        ],
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            return subprocess.CompletedProcess(command, 0)
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(runner.subprocess, "run", fake_run)

    exit_code = runner.main(
        [
            "--output-dir",
            str(tmp_path),
            "--runtime-summary",
            "--manifest-compiled-limit",
            "2",
            "--wheelhouse",
            str(wheelhouse),
            "--installed-wheel",
            str(gap_wheel),
        ]
    )

    assert exit_code == 0
    assert commands[0] == [
        sys.executable,
        str(ROOT / "tools" / "sagelite_runtime_manifest.py"),
        "collect",
        "--label",
        "short",
        "--output",
        str(tmp_path / "doctest-installed-short-20260616-060708.runtime-manifest.json"),
        "--compiled-limit",
        "2",
    ]
    assert commands[1][2] == "sage.doctest"

    summary_path = (
        tmp_path / "doctest-installed-short-20260616-060708.runtime-summary.json"
    )
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["environment"]["PYTHONNOUSERSITE"] == "1"
    assert summary["environment"]["PYTHONPATH_present"] is False
    assert summary["runtime_manifest"]["created"] is True
    assert summary["features"]["counts"] == {
        "absent": 1,
        "errored": 1,
        "present": 1,
        "unknown": 0,
    }
    assert summary["features"]["present"] == ["gap"]
    assert summary["features"]["absent"] == ["gap_package_guava"]
    assert summary["features"]["errored"] == ["fricas"]
    assert summary["analysis"]["created"] is True
    assert summary["analysis"]["available"] is True
    assert summary["analysis"]["totals"] == {"modules_failed": 2, "modules_seen": 10}
    assert summary["analysis"]["fingerprint_counts"] == {"missing-executable": 2}
    assert summary["analysis"]["top_actionable_buckets"] == [
        {
            "category": "optional-external",
            "fingerprint": "missing-executable",
            "suggested_package": "sagelite-cddlib-runtime",
            "count": 2,
            "failed_examples": 2,
            "evidence": "standalone executable not found",
            "modules": [
                "sage.geometry.polyhedron.backend_cdd",
                "sage.geometry.polyhedron.backend_cdd_rdf",
            ],
        }
    ]
    assert summary["wheels"]["installed_wheels"] == [gap_wheel.name]
    assert summary["wheels"]["companion_packages"] == [
        "sagelite-gap-runtime",
        "sagelite-maxima-runtime",
    ]
    assert summary["wheels"]["installed_sagelite_packages"] == {
        "available": True,
        "companion_packages": [
            "sagelite-gap-runtime",
            "sagelite-maxima-runtime",
        ],
        "packages": [
            {
                "name": "sagelite",
                "version": "10.9.post1",
                "location": "/scratch/install/lib/python3.12/site-packages",
            },
            {
                "name": "sagelite-gap-runtime",
                "version": "10.9",
                "location": "/scratch/install/lib/python3.12/site-packages",
            },
            {
                "name": "sagelite-maxima-runtime",
                "version": "10.9.post13",
                "location": "/scratch/install/lib/python3.12/site-packages",
            },
        ],
    }
    assert summary["wheels"]["wheelhouse_files"][str(wheelhouse)] == [
        "sagelite-10.9.post1-cp312-cp312-linux_x86_64.whl",
        "sagelite_gap_runtime-10.9-py3-none-any.whl",
    ]
