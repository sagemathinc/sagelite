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
            "CC": shlex.join([sys.executable, "-m", "ziglang", "cc", "-w"]),
            "CXX": shlex.join([sys.executable, "-m", "ziglang", "c++", "-w"]),
        },
    )

    with cython._cython_compiler_environment():
        assert shlex.split(cython.os.environ["CC"]) == [
            sys.executable,
            "-m",
            "ziglang",
            "cc",
            "-w",
        ]
        assert shlex.split(cython.os.environ["CXX"]) == [
            sys.executable,
            "-m",
            "ziglang",
            "c++",
            "-w",
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
