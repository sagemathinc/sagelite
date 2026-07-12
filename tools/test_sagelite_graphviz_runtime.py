import importlib.util
import os
from pathlib import Path


RUNTIME = (
    Path(__file__).resolve().parents[1]
    / "companion-packages"
    / "sagelite-graphviz-runtime"
    / "src"
    / "sagelite_graphviz"
    / "runtime.py"
)


def _runtime_module():
    spec = importlib.util.spec_from_file_location("sagelite_graphviz_runtime_test", RUNTIME)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_executable_path_restores_wheel_package_data_modes(tmp_path, monkeypatch):
    module = _runtime_module()
    package = tmp_path / "sagelite_graphviz"
    bindir = package / "data" / "bin"
    bindir.mkdir(parents=True)
    wrapper = bindir / "dot"
    executable = bindir / "dot-real"
    wrapper.write_text("#!/bin/sh\n")
    executable.write_bytes(b"graphviz")
    wrapper.chmod(0o600)
    executable.chmod(0o600)
    monkeypatch.setattr(module, "__file__", os.fspath(package / "runtime.py"))

    assert module.executable_path() == wrapper
    assert os.access(wrapper, os.X_OK)
    assert os.access(executable, os.X_OK)
