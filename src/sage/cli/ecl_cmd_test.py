import os
import subprocess
import sys
import types

from sage.cli import _ecl_command, main


def test_ecl_command_uses_companion_runtime(monkeypatch, tmp_path):
    command = tmp_path / "ecl"
    command.write_text("#!/bin/sh\n")
    command.chmod(0o755)
    runtime = types.SimpleNamespace(ecl_command=lambda: command)
    package = types.ModuleType("sagelite_ecl")

    monkeypatch.setitem(sys.modules, "sagelite_ecl", package)
    monkeypatch.setitem(sys.modules, "sagelite_ecl.runtime", runtime)

    assert _ecl_command() == os.fspath(command)


def test_ecl_command_falls_back_to_system_command(monkeypatch, tmp_path):
    command = tmp_path / "missing-ecl"
    runtime = types.SimpleNamespace(ecl_command=lambda: command)
    package = types.ModuleType("sagelite_ecl")

    monkeypatch.setitem(sys.modules, "sagelite_ecl", package)
    monkeypatch.setitem(sys.modules, "sagelite_ecl.runtime", runtime)

    assert _ecl_command() == "ecl"


def test_main_dispatches_lisp_option_to_ecl(monkeypatch, tmp_path):
    calls = []

    monkeypatch.setattr(sys, "argv", ["sage", "--lisp", "--version"])
    monkeypatch.setattr("sage.cli._ecl_command", lambda: os.fspath(tmp_path / "ecl"))
    monkeypatch.setattr(
        subprocess,
        "call",
        lambda command: calls.append(command) or 17,
    )

    assert main() == 17
    assert calls == [[os.fspath(tmp_path / "ecl"), "--version"]]
