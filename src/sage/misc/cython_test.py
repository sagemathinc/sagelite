import shlex
import sys

from sage.misc import cython


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
