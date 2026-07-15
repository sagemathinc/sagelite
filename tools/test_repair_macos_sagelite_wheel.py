from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest


SCRIPT = (
    Path(__file__).parents[1]
    / ".github"
    / "workflows"
    / "repair-macos-sagelite-wheel.py"
)
SPEC = importlib.util.spec_from_file_location("repair_macos_sagelite_wheel", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
repair = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(repair)


@pytest.mark.parametrize(
    ("dependency", "owner"),
    [
        ("/opt/homebrew/lib/libgmp.10.dylib", "pari"),
        ("@loader_path/libmpfi.0.dylib", "pari"),
        ("/prefix/lib/libSingular-4.4.1.dylib", "singular"),
        ("/prefix/lib/libfactory-4.4.1.dylib", "singular"),
        ("/prefix/lib/libflint.22.dylib", None),
    ],
)
def test_companion_owner(dependency, owner):
    assert repair.companion_owner(dependency) == owner


def test_companion_dependency_is_relative_to_binary(tmp_path):
    binary = tmp_path / "sage" / "rings" / "integer.so"
    binary.parent.mkdir(parents=True)
    assert repair.companion_dependency(
        binary, tmp_path, "/build/lib/libgmp.10.dylib"
    ) == "@loader_path/../../sagelite_pari/data/lib/libgmp.10.dylib"


def test_delocate_command_excludes_companion_families(tmp_path):
    command = repair.delocate_command(
        tmp_path / "input.whl", tmp_path / "out", "/venv/bin/delocate-wheel"
    )
    assert command[0] == "/venv/bin/delocate-wheel"
    assert "--ignore-missing-dependencies" in command
    assert command[command.index("--require-archs") + 1] == "arm64"
    excluded = {
        command[index + 1]
        for index, value in enumerate(command)
        if value == "--exclude"
    }
    assert excluded == {
        *repair.PARI_RUNTIME_PREFIXES,
        *repair.SINGULAR_RUNTIME_PREFIXES,
    }


def test_rewrite_and_audit_companion_dependencies(tmp_path, monkeypatch):
    module = tmp_path / "sage" / "module.so"
    bundled = tmp_path / "sagelite.libs" / "libflint.22.dylib"
    module.parent.mkdir(parents=True)
    bundled.parent.mkdir(parents=True)
    module.write_bytes(b"module")
    bundled.write_bytes(b"flint")

    dependencies = {
        module: [
            "/opt/homebrew/lib/libflint.22.dylib",
            "/opt/homebrew/lib/libgmp.10.dylib",
            "/usr/lib/libSystem.B.dylib",
        ],
        bundled: [
            "@loader_path/libflint.22.dylib",
            "/opt/homebrew/lib/libgmp.10.dylib",
            "/usr/lib/libSystem.B.dylib",
        ],
    }
    monkeypatch.setattr(repair, "macho_files", lambda root: [module, bundled])
    monkeypatch.setattr(repair, "otool_libraries", lambda path: dependencies[path])
    monkeypatch.setattr(repair, "otool_install_ids", lambda path: set())
    monkeypatch.setattr(repair, "sign_macho", lambda path: None)

    def fake_run(command, **kwargs):
        assert command[0] == "install_name_tool"
        binary = Path(command[-1])
        args = command[1:-1]
        for index in range(0, len(args), 3):
            assert args[index] == "-change"
            old, new = args[index + 1 : index + 3]
            dependencies[binary] = [
                new if dependency == old else dependency
                for dependency in dependencies[binary]
            ]
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(repair.subprocess, "run", fake_run)
    changed_files, changed_dependencies = repair.rewrite_companion_dependencies(
        tmp_path
    )
    assert (changed_files, changed_dependencies) == (2, 2)
    assert dependencies[module][1] == (
        "@loader_path/../sagelite_pari/data/lib/libgmp.10.dylib"
    )
    assert dependencies[bundled][1] == (
        "@loader_path/../sagelite_pari/data/lib/libgmp.10.dylib"
    )

    dependencies[module][0] = "@loader_path/../sagelite.libs/libflint.22.dylib"
    assert repair.audit_portable_dependencies(tmp_path) == (2, 6)


def test_audit_rejects_absolute_and_unresolved_dependencies(tmp_path, monkeypatch):
    module = tmp_path / "sage" / "module.so"
    module.parent.mkdir(parents=True)
    module.write_bytes(b"module")
    monkeypatch.setattr(repair, "macho_files", lambda root: [module])
    monkeypatch.setattr(repair, "otool_install_ids", lambda path: set())
    monkeypatch.setattr(
        repair,
        "otool_libraries",
        lambda path: [
            "/opt/homebrew/lib/libflint.22.dylib",
            "@loader_path/missing.dylib",
            "@loader_path/../../host-only.dylib",
        ],
    )
    (tmp_path.parent / "host-only.dylib").write_bytes(b"host")
    with pytest.raises(RuntimeError, match=r"(?s)non-portable.*unresolved"):
        repair.audit_portable_dependencies(tmp_path)


def test_audit_does_not_treat_install_id_as_dependency(tmp_path, monkeypatch):
    library = tmp_path / "sagelite.libs" / "libexample.dylib"
    library.parent.mkdir(parents=True)
    library.write_bytes(b"library")
    install_id = "/DLC/sagelite.libs/libexample.dylib"
    monkeypatch.setattr(repair, "macho_files", lambda root: [library])
    monkeypatch.setattr(
        repair,
        "otool_libraries",
        lambda path: [install_id, "/usr/lib/libSystem.B.dylib"],
    )
    monkeypatch.setattr(repair, "otool_install_ids", lambda path: {install_id})
    assert repair.audit_portable_dependencies(tmp_path) == (1, 1)
