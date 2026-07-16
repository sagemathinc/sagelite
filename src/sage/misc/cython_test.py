import shlex
import sys
from types import SimpleNamespace

from sage.misc import cython


def test_repair_installed_macos_extension_uses_packaged_dylib(
    tmp_path, monkeypatch
):
    target = tmp_path / "target"
    runtime = tmp_path / "site-packages" / "sagelite_runtime" / "data" / "lib"
    target.mkdir()
    runtime.mkdir(parents=True)
    extension = target / "example.so"
    extension.write_bytes(b"extension")
    library = runtime / "libgsl.28.dylib"
    library.write_bytes(b"library")
    commands = []

    def fake_run(command, **kwargs):
        commands.append(command)
        if command[0] == "otool":
            return SimpleNamespace(
                stdout=(
                    f"{extension}:\n"
                    "\t@loader_path/libgsl.28.dylib "
                    "(compatibility version 29.0.0, current version 29.0.0)\n"
                    "\t/usr/lib/libSystem.B.dylib "
                    "(compatibility version 1.0.0, current version 1.0.0)\n"
                )
            )
        return SimpleNamespace(stdout="")

    monkeypatch.setattr(cython, "SAGE_ROOT", None)
    monkeypatch.setattr(cython.sys, "platform", "darwin")
    monkeypatch.setattr(
        cython,
        "subprocess",
        SimpleNamespace(
            DEVNULL=-1,
            run=fake_run,
        ),
    )
    monkeypatch.setattr(cython.shutil, "which", lambda command: None)

    assert cython._repair_installed_sagelite_macos_extension(
        target, "example", [runtime], extension_suffixes=[".so"]
    ) == 1
    assert commands[1] == [
        "install_name_tool",
        "-change",
        "@loader_path/libgsl.28.dylib",
        "@rpath/libgsl.28.dylib",
        str(extension),
    ]


def test_cython_compiler_environment_uses_ziglang_fallback(monkeypatch):
    monkeypatch.delenv("CC", raising=False)
    monkeypatch.delenv("CXX", raising=False)
    monkeypatch.setattr(
        cython,
        "_cython_compiler_commands",
        lambda: {
            "CC": shlex.join([sys.executable, "-m", "ziglang", "cc"]),
            "CXX": shlex.join([sys.executable, "-m", "ziglang", "c++"]),
        },
    )

    with cython._cython_compiler_environment():
        assert shlex.split(cython.os.environ["CC"]) == [
            sys.executable,
            "-m",
            "ziglang",
            "cc",
        ]
        assert shlex.split(cython.os.environ["CXX"]) == [
            sys.executable,
            "-m",
            "ziglang",
            "c++",
        ]

    assert "CC" not in cython.os.environ
    assert "CXX" not in cython.os.environ


def test_cython_compiler_environment_preserves_explicit_compilers(monkeypatch):
    monkeypatch.setenv("CC", "custom-cc")
    monkeypatch.setenv("CXX", "custom-cxx")
    monkeypatch.setattr(cython, "_cython_compiler_commands", lambda: {})

    with cython._cython_compiler_environment():
        assert cython.os.environ["CC"] == "custom-cc"
        assert cython.os.environ["CXX"] == "custom-cxx"


def test_filter_zig_libcxx_diagnostics_is_narrow():
    warning = (
        "In file included from site-packages/ziglang/lib/libcxx/src/chrono.cpp:\n"
        "site-packages/ziglang/lib/libcxx/include/string:1078:80: warning: "
        "pointer is missing a nullability type specifier "
        "[-Wnullability-completeness]\n"
        "note: insert '_Nullable' if the pointer may be null\n"
        "site-packages/ziglang/lib/libcxx/include/system_error:152:\n"
        "119 warnings generated.\n"
    )

    assert cython._filter_zig_libcxx_diagnostics(warning) == ""

    with_error = warning + "extension.cpp:12:3: fatal error: missing header\n"
    assert cython._filter_zig_libcxx_diagnostics(with_error) == with_error

    with_other_warning = warning + "extension.cpp:12:3: warning: user warning\n"
    assert cython._filter_zig_libcxx_diagnostics(with_other_warning) == with_other_warning

    interleaved_warning = warning + (
        ":2503:1: warning: pointer is missing a nullability type specifier "
        "[-Wnullability-completeness]\n"
        "_Nullablewarning: \n"
    )
    assert cython._filter_zig_libcxx_diagnostics(interleaved_warning) == ""

    with_other_category = warning + (
        "extension.cpp:12:3: warning: unused variable [-Wunused-variable]\n"
    )
    assert cython._filter_zig_libcxx_diagnostics(with_other_category) == with_other_category
