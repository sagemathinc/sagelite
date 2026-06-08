import os
import subprocess
import sys
import importlib.util
import importlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = ROOT / "src" / "sage" / "graphs" / "lovasz_theta.py"
spec = importlib.util.spec_from_file_location("sage.graphs.lovasz_theta", MODULE_PATH)
lovasz_theta_module = importlib.util.module_from_spec(spec)
sys.modules["sage.graphs.lovasz_theta"] = lovasz_theta_module
spec.loader.exec_module(lovasz_theta_module)

lovasz_theta = lovasz_theta_module.lovasz_theta


def test_lovasz_theta_uses_csdp_feature_executable(monkeypatch, tmp_path):
    import networkx

    csdp = importlib.import_module("sage.features.csdp")

    theta = tmp_path / "theta"
    theta.write_text("#!/bin/sh\n")
    theta.chmod(0o755)

    class FakeCSDP:
        def require(self):
            return None

        def absolute_filename(self):
            return os.fspath(theta)

    class FakeGraph:
        def order(self):
            return 2

        def relabel(self, inplace=False, perm=None):
            return self

        def networkx_graph(self):
            graph = networkx.Graph()
            graph.add_edge(1, 2)
            return graph

    commands = []

    def fake_check_output(command):
        commands.append(command)
        return b"The Lovasz Theta Number is 1.0\n"

    monkeypatch.setattr(csdp, "CSDP", FakeCSDP)
    monkeypatch.setattr(subprocess, "check_output", fake_check_output)
    monkeypatch.setenv("PATH", "")

    assert lovasz_theta(FakeGraph()) == 1.0
    assert commands[0][0] == os.fspath(theta)
