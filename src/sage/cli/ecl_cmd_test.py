import os
import subprocess
import sys
import types

import pytest
import sage.cli as sage_cli

_ecl_command = getattr(sage_cli, "_ecl_command", None)
if _ecl_command is None:
    pytest.skip(
        "installed sagelite wheel does not expose sage.cli._ecl_command",
        allow_module_level=True,
    )

main = sage_cli.main


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


def test_main_dispatches_sh_option_to_shell(monkeypatch, tmp_path):
    calls = []

    monkeypatch.setattr(sys, "argv", ["sage", "--sh", "-c", "exit 42"])
    monkeypatch.setattr("sage.cli._shell_command", lambda: os.fspath(tmp_path / "sh"))
    monkeypatch.setattr(
        subprocess,
        "call",
        lambda command: calls.append(command) or 42,
    )

    assert main() == 42
    assert calls == [[os.fspath(tmp_path / "sh"), "-c", "exit 42"]]


def test_main_dispatches_python_options_to_current_interpreter(monkeypatch, tmp_path):
    calls = []

    monkeypatch.setattr(
        "sage.cli._python_command",
        lambda: os.fspath(tmp_path / "python"),
    )
    monkeypatch.setattr(
        subprocess,
        "call",
        lambda command: calls.append(command) or 0,
    )

    monkeypatch.setattr(sys, "argv", ["sage", "--python", "-c", "print(1)"])
    assert main() == 0
    monkeypatch.setattr(sys, "argv", ["sage", "--python3", "-V"])
    assert main() == 0

    assert calls == [
        [os.fspath(tmp_path / "python"), "-c", "print(1)"],
        [os.fspath(tmp_path / "python"), "-V"],
    ]


def test_main_prints_installed_advanced_help(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["sage", "--advanced"])

    assert main() == 0
    output = capsys.readouterr().out
    assert "run the Python interpreter used by this Sage installation" in output
    assert "run a system shell with the Sage environment" in output
    assert "run the Sage cleaner." in output
