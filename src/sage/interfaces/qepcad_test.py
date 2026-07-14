import importlib.util
import os
import stat
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "interfaces" / "qepcad.py"
spec = importlib.util.spec_from_file_location("sage.interfaces.qepcad", MODULE_PATH)
qepcad_module = importlib.util.module_from_spec(spec)
sys.modules["sage.interfaces.qepcad"] = qepcad_module
spec.loader.exec_module(qepcad_module)


def _write_fake_qepcad_runtime(tmp_path):
    package = tmp_path / "sagelite_qepcad"
    root = package / "data" / "root"
    executable = root / "bin" / "qepcad"
    help_file = root / "share" / "qepcad" / "qepcad.help"
    rc_file = root / "etc" / "default.qepcadrc"

    package.mkdir()
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n"
        "def root_dir():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'root'\n"
        "def executable_path():\n"
        "    return root_dir() / 'bin' / 'qepcad'\n"
        "def help_path():\n"
        "    return root_dir() / 'share' / 'qepcad' / 'qepcad.help'\n"
        "def default_qepcadrc_path():\n"
        "    return root_dir() / 'etc' / 'default.qepcadrc'\n"
    )

    executable.parent.mkdir(parents=True)
    executable.write_text("#!/bin/sh\n")
    executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
    help_file.parent.mkdir(parents=True)
    help_file.write_text("@\n\nfinish 1 abcde m\n@\nFinish QEPCAD.\n@\n@@@\n")
    rc_file.parent.mkdir(parents=True)
    rc_file.write_text("SINGULAR yes\n")
    return root


def _write_fake_singular_runtime(tmp_path):
    package = tmp_path / "sagelite_singular_runtime"
    executable = package / "data" / "bin" / "Singular"
    package.mkdir()
    (package / "__init__.py").write_text("")
    (package / "runtime.py").write_text(
        "from pathlib import Path\n"
        "def executable_path():\n"
        "    return Path(__file__).resolve().parent / 'data' / 'bin' / 'Singular'\n"
    )
    executable.parent.mkdir(parents=True)
    executable.write_text("#!/bin/sh\n")
    executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
    return executable


def test_qepcad_cmd_discovers_sagelite_companion(monkeypatch, tmp_path):
    root = _write_fake_qepcad_runtime(tmp_path)
    monkeypatch.syspath_prepend(os.fspath(tmp_path))

    try:
        command = qepcad_module._qepcad_cmd(memcells=123)
        assert command == f"env qe={root} {root / 'bin' / 'qepcad'} +N123"
    finally:
        sys.modules.pop("sagelite_qepcad", None)
        sys.modules.pop("sagelite_qepcad.runtime", None)


def test_qepcad_cmd_exposes_singular_companion_to_child(monkeypatch, tmp_path):
    root = _write_fake_qepcad_runtime(tmp_path)
    singular = _write_fake_singular_runtime(tmp_path)
    monkeypatch.syspath_prepend(os.fspath(tmp_path))
    monkeypatch.setenv("PATH", "/usr/bin:/bin")

    try:
        command = qepcad_module._qepcad_cmd(memcells=123)
        assert command == (
            f"env qe={root} PATH={singular.parent}:/usr/bin:/bin "
            f"{root / 'bin' / 'qepcad'} +N123"
        )
    finally:
        sys.modules.pop("sagelite_qepcad", None)
        sys.modules.pop("sagelite_qepcad.runtime", None)
        sys.modules.pop("sagelite_singular_runtime", None)
        sys.modules.pop("sagelite_singular_runtime.runtime", None)


def test_qepcad_help_discovers_sagelite_companion(monkeypatch, tmp_path):
    root = _write_fake_qepcad_runtime(tmp_path)
    monkeypatch.syspath_prepend(os.fspath(tmp_path))

    try:
        qepcad_module._command_info_cache = None
        qepcad_module._update_command_info()

        assert qepcad_module._qepcad_help_path() == os.fspath(
            root / "share" / "qepcad" / "qepcad.help"
        )
        assert qepcad_module._command_info_cache["finish"][3] == "Finish QEPCAD.\n"
    finally:
        qepcad_module._command_info_cache = None
        sys.modules.pop("sagelite_qepcad", None)
        sys.modules.pop("sagelite_qepcad.runtime", None)


def test_qepcad_default_qepcadrc_discovers_sagelite_companion(monkeypatch, tmp_path):
    root = _write_fake_qepcad_runtime(tmp_path)
    monkeypatch.syspath_prepend(os.fspath(tmp_path))

    try:
        assert qepcad_module._qepcad_default_qepcadrc_path() == os.fspath(
            root / "etc" / "default.qepcadrc"
        )
    finally:
        sys.modules.pop("sagelite_qepcad", None)
        sys.modules.pop("sagelite_qepcad.runtime", None)
