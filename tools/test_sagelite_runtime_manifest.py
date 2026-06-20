from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_manifest():
    path = ROOT / "tools" / "sagelite_runtime_manifest.py"
    spec = importlib.util.spec_from_file_location("sagelite_runtime_manifest", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_collect_executables_records_path_and_version_probe(monkeypatch):
    manifest = _load_manifest()
    monkeypatch.setattr(manifest.shutil, "which", lambda name: f"/venv/bin/{name}")
    commands = []

    def fake_run(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, stdout="tool 1.2\n", stderr="")

    monkeypatch.setattr(manifest.subprocess, "run", fake_run)

    result = manifest.collect_executables(["gap"])

    assert result["gap"]["path"] == "/venv/bin/gap"
    assert result["gap"]["attempts"][0]["stdout"] == "tool 1.2"
    assert commands == [["/venv/bin/gap", "--version"]]


def test_collect_gap_package_programs_records_executable_wtdist(tmp_path):
    manifest = _load_manifest()
    package = tmp_path / "gaproot" / "pkg" / "guava-3.17"
    program = package / "bin" / "wtdist"
    program.parent.mkdir(parents=True)
    program.write_text("#!/bin/sh\n", encoding="utf-8")
    program.chmod(program.stat().st_mode | 0o111)

    result = manifest.collect_gap_package_programs([str(tmp_path / "gaproot")])

    guava = result["guava"]
    assert guava["complete"] is True
    assert guava["package_dirs"] == [str(package.resolve())]
    assert guava["program_dirs"][0]["programs"]["wtdist"] == {
        "path": str(program.resolve()),
        "exists": True,
        "is_file": True,
        "executable": True,
    }


def test_split_gap_roots_accepts_gap_semicolon_separator():
    manifest = _load_manifest()

    assert manifest._split_gap_roots("/sage/gap;/venv/gap") == [
        "/sage/gap",
        "/venv/gap",
    ]
    assert manifest._split_gap_roots(os.pathsep.join(["/a", "/b"])) == ["/a", "/b"]


def test_compare_manifests_surfaces_parity_buckets():
    manifest = _load_manifest()
    reference = {
        "label": "self-contained",
        "python": {
            "executable": "/sage/bin/python",
            "prefix": "/sage/local/var/lib/sage/venv-python3.12",
        },
        "packages": [
            {"name": "sagelite", "version": "10.9"},
            {"name": "sagelite-gap-runtime", "version": "10.9"},
        ],
        "features": {
            "features": [
                {"name": "gap_package_guava", "present": True},
                {"name": "sage.libs.coxeter3", "present": True},
            ]
        },
        "executables": {"gap": {"path": "/sage/local/bin/gap"}},
        "gap": {
            "sage_env_gap_roots": ["/sage/local/lib/gap"],
            "gap_package_programs": {
                "guava": {
                    "complete": True,
                    "package_dirs": ["/sage/local/lib/gap/pkg/guava"],
                    "program_dirs": [
                        {
                            "path": "/sage/local/lib/gap/pkg/guava/bin",
                            "programs": {
                                "wtdist": {
                                    "path": "/sage/local/lib/gap/pkg/guava/bin/wtdist",
                                    "exists": True,
                                    "is_file": True,
                                    "executable": True,
                                }
                            },
                        }
                    ],
                }
            },
        },
    }
    candidate = {
        "label": "pip",
        "python": {"executable": "/scratch/install/bin/python", "prefix": "/scratch/install"},
        "packages": [{"name": "sagelite", "version": "10.9.post1"}],
        "features": {
            "features": [
                {
                    "name": "gap_package_guava",
                    "present": False,
                    "reason": "wtdist missing",
                },
                {"name": "sage.libs.coxeter3", "present": True},
            ]
        },
        "executables": {"gap": {"path": "/usr/bin/gap"}},
        "compiled_modules": [
            {
                "sage_relative_path": "sage/libs/example.so",
                "dependencies_outside_policy": [
                    {"name": "libexample.so", "path": "/project/local/lib/libexample.so"}
                ],
            }
        ],
        "source_inspection": {
            "sage.rings.rational": {
                "sage_getfile_relative": "/scratch/build/src/sage/rings/rational.pyx"
            }
        },
        "gap": {
            "sage_env_gap_roots": ["/usr/share/gap"],
            "gap_package_programs": {
                "guava": {
                    "complete": False,
                    "package_dirs": ["/usr/share/gap/pkg/guava"],
                    "program_dirs": [
                        {
                            "path": "/usr/share/gap/pkg/guava/bin",
                            "programs": {
                                "wtdist": {
                                    "path": "/usr/share/gap/pkg/guava/bin/wtdist",
                                    "exists": False,
                                    "is_file": False,
                                    "executable": False,
                                }
                            },
                        }
                    ],
                }
            },
        },
    }

    diff = manifest.compare_manifests(reference, candidate)

    assert diff["missing_packages"] == ["sagelite-gap-runtime"]
    assert diff["version_differences"]["sagelite"] == {
        "reference": "10.9",
        "candidate": "10.9.post1",
    }
    assert diff["feature_differences"]["gap_package_guava"]["candidate_reason"] == "wtdist missing"
    assert diff["executable_differences"]["gap"]["candidate"] == "/usr/bin/gap"
    assert diff["candidate_dependency_leaks"][0]["module"] == "sage/libs/example.so"
    assert "sage.rings.rational" in diff["candidate_source_path_leaks"]
    assert diff["gap_package_program_differences"]["guava"][
        "candidate_complete"
    ] is False
    assert "/usr/share/gap" in diff["candidate_gap_host_leaks"]
    assert "/usr/share/gap/pkg/guava" in diff["candidate_gap_host_leaks"]


def test_cli_compare_writes_json_and_markdown(tmp_path):
    manifest = _load_manifest()
    reference = {
        "label": "reference",
        "python": {"executable": "/ref/python"},
        "packages": [],
        "features": {"features": []},
        "executables": {},
    }
    candidate = {
        "label": "candidate",
        "python": {"executable": "/cand/python"},
        "packages": [],
        "features": {"features": []},
        "executables": {},
    }
    ref_path = tmp_path / "ref.json"
    cand_path = tmp_path / "cand.json"
    json_out = tmp_path / "diff.json"
    md_out = tmp_path / "diff.md"
    ref_path.write_text(manifest.json.dumps(reference), encoding="utf-8")
    cand_path.write_text(manifest.json.dumps(candidate), encoding="utf-8")

    exit_code = manifest.main(
        [
            "compare",
            "--reference",
            str(ref_path),
            "--candidate",
            str(cand_path),
            "--json-output",
            str(json_out),
            "--md-output",
            str(md_out),
        ]
    )

    assert exit_code == 0
    assert json_out.is_file()
    assert "Sagelite runtime parity diff" in md_out.read_text(encoding="utf-8")
