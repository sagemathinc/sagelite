from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import types
from argparse import Namespace
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


def test_collect_platform_tags_records_packaging_sys_tags(monkeypatch):
    manifest = _load_manifest()
    tags_module = types.ModuleType("packaging.tags")
    tags_module.sys_tags = lambda: iter(
        ["cp312-cp312-manylinux_2_28_x86_64", "py3-none-any"]
    )

    monkeypatch.setattr(manifest.sysconfig, "get_platform", lambda: "linux-x86_64")
    monkeypatch.setattr(manifest.importlib, "import_module", lambda name: tags_module)

    tags = manifest.collect_platform_tags()

    assert tags == {
        "sysconfig_platform": "linux-x86_64",
        "tags": ["cp312-cp312-manylinux_2_28_x86_64", "py3-none-any"],
    }


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
    assert result["gap"]["host_path"] is False
    assert result["gap"]["attempts"][0]["stdout"] == "tool 1.2"
    assert commands == [["/venv/bin/gap", "--version"]]


def test_collect_executables_marks_host_system_paths(monkeypatch):
    manifest = _load_manifest()
    monkeypatch.setattr(manifest.shutil, "which", lambda name: f"/usr/bin/{name}")
    monkeypatch.setattr(
        manifest,
        "_version_probe",
        lambda path: {"attempts": [{"command": [path, "--version"]}]},
    )

    result = manifest.collect_executables(["maxima"])

    assert result["maxima"]["path"] == "/usr/bin/maxima"
    assert result["maxima"]["host_path"] is True


def test_default_executables_include_installed_sagelite_console_scripts(monkeypatch):
    manifest = _load_manifest()

    class FakeDistribution:
        def __init__(self, name, scripts):
            self.name = name
            self.metadata = {"Name": name}
            self.entry_points = [
                manifest.importlib.metadata.EntryPoint(
                    name=script,
                    value=f"{name.replace('-', '_')}.runtime:{script}",
                    group="console_scripts",
                )
                for script in scripts
            ]

    monkeypatch.setattr(
        manifest.importlib.metadata,
        "distributions",
        lambda: [
            FakeDistribution("sagelite-topcom-runtime", ["points2alltriangs"]),
            FakeDistribution("sagelite-nauty-runtime", ["dreadnaut"]),
            FakeDistribution("unrelated-runtime", ["host-tool"]),
        ],
    )

    executables = manifest.collect_default_executables()

    assert "gap" in executables
    assert "points2alltriangs" in executables
    assert "dreadnaut" in executables
    assert "host-tool" not in executables


def test_collect_manifest_uses_discovered_default_executables(monkeypatch):
    manifest = _load_manifest()
    seen = {}

    monkeypatch.setattr(
        manifest,
        "collect_default_executables",
        lambda: ["gap", "points2alltriangs"],
    )
    monkeypatch.setattr(manifest, "collect_python_info", lambda: {})
    monkeypatch.setattr(manifest, "collect_sage_environment", lambda: {})
    monkeypatch.setattr(manifest, "collect_installed_packages", lambda: [])
    monkeypatch.setattr(manifest, "collect_features", lambda timeout: {})
    monkeypatch.setattr(manifest, "collect_gap_details", lambda: {})
    monkeypatch.setattr(manifest, "collect_maxima_details", lambda: {})
    monkeypatch.setattr(manifest, "collect_fricas_details", lambda: {})
    monkeypatch.setattr(manifest, "collect_fplll_details", lambda: {})
    monkeypatch.setattr(manifest, "collect_compiled_modules", lambda limit: [])
    monkeypatch.setattr(manifest, "collect_source_inspection", lambda modules: {})

    def fake_collect_executables(names):
        seen["names"] = names
        return {name: {"path": None} for name in names}

    monkeypatch.setattr(manifest, "collect_executables", fake_collect_executables)

    result = manifest.collect_manifest(
        Namespace(
            label="test",
            executable=None,
            feature_timeout=0,
            compiled_limit=0,
            inspect_module=[],
        )
    )

    assert seen["names"] == ["gap", "points2alltriangs"]
    assert sorted(result["executables"]) == ["gap", "points2alltriangs"]


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


def test_collect_fplll_details_records_sage_resolved_strategy(monkeypatch, tmp_path):
    manifest = _load_manifest()
    companion_strategy = tmp_path / "strategies" / "default.json"
    companion_strategy.parent.mkdir()
    companion_strategy.write_text("[]", encoding="utf-8")

    runtime = types.ModuleType("sagelite_fplll_data.runtime")
    runtime.default_strategy = lambda: companion_strategy
    fpylll = types.ModuleType("fpylll")
    fpylll.__version__ = "0.6.4"
    config = types.ModuleType("fpylll.config")
    config.default_strategy_path = "/project/local/share/fplll/strategies"
    config.default_strategy = "/project/local/share/fplll/strategies/default.json"
    sage_env = types.ModuleType("sage.env")
    sage_env._fplll_default_strategy_file = lambda path, strategy: str(
        companion_strategy
    )

    monkeypatch.setitem(sys.modules, "sagelite_fplll_data.runtime", runtime)
    monkeypatch.setitem(sys.modules, "fpylll", fpylll)
    monkeypatch.setitem(sys.modules, "fpylll.config", config)
    monkeypatch.setitem(sys.modules, "sage.env", sage_env)

    details = manifest.collect_fplll_details()

    assert details["companion_default_strategy"] == str(companion_strategy)
    assert details["companion_default_strategy_exists"] is True
    assert details["fpylll_config_default_strategy_path"] == (
        "/project/local/share/fplll/strategies"
    )
    assert details["sage_resolved_default_strategy"] == str(companion_strategy)
    assert details["sage_resolved_default_strategy_exists"] is True


def test_ldd_marks_not_found_dependencies_outside_policy(monkeypatch, tmp_path):
    manifest = _load_manifest()
    extension = tmp_path / "sage" / "libs" / "missing_dep.so"
    extension.parent.mkdir(parents=True)
    extension.write_bytes(b"")

    ldd_stdout = """
        linux-vdso.so.1 (0x00007ffd00000000)
        libmissing.so.0 => not found
        libpython3.12.so.1.0 => /venv/lib/libpython3.12.so.1.0 (0x00007f0000000000)
    """

    def fake_run_probe(command, timeout=5.0):  # noqa: ARG001
        if command[0] == "ldd":
            return manifest.ProbeResult(command, 0, ldd_stdout, "")
        return manifest.ProbeResult(command, 0, "", "")

    monkeypatch.setattr(manifest, "_run_probe", fake_run_probe)

    ldd = manifest._ldd(extension)
    missing = ldd["dependencies"][1]

    assert missing == {"name": "libmissing.so.0", "path": "not found"}
    assert manifest._is_allowed_dependency(missing["path"], [Path("/venv")]) is False


def test_candidate_python_path_leaks_ignore_venv_and_report_source_tree(tmp_path):
    manifest = _load_manifest()
    venv = tmp_path / "install"
    source = tmp_path / "current-source" / "src"
    (source / "sage").mkdir(parents=True)
    candidate = {
        "python": {
            "prefix": str(venv),
            "exec_prefix": str(venv),
            "path": [
                str(venv / "lib" / "python3.12" / "site-packages"),
                str(source),
                "/project/.mesonpy-abcd/src",
            ],
        }
    }

    leaks = manifest._candidate_python_path_leaks(candidate)

    assert leaks == [
        {
            "path": str(source),
            "reason": "temporary or project build tree, source-tree sage package",
        },
        {
            "path": "/project/.mesonpy-abcd/src",
            "reason": "meson build tree, temporary or project build tree",
        },
    ]


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
        "executables": {"gap": {"path": "/sage/local/bin/gap", "host_path": False}},
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
        "maxima": {
            "executable": "/sage/local/bin/maxima",
            "MAXIMA_PREFIX": "/sage/local",
            "sage_env_MAXIMA_FAS": "/sage/local/lib/ecl/maxima.fas",
        },
        "fricas": {
            "executable": "/sage/local/bin/fricas",
            "FRICAS_PREFIX": "/sage/local",
            "FRICAS_INITFILE": "/sage/local/lib/fricas/fricas.input",
        },
        "fplll": {
            "companion_default_strategy": "/sage/local/share/fplll/strategies/default.json",
            "companion_default_strategy_exists": True,
            "fpylll_version": "0.6.4",
            "fpylll_config_default_strategy": "/sage/local/share/fplll/strategies/default.json",
            "sage_resolved_default_strategy": "/sage/local/share/fplll/strategies/default.json",
            "sage_resolved_default_strategy_exists": True,
        },
    }
    candidate = {
        "label": "pip",
        "python": {
            "executable": "/scratch/install/bin/python",
            "prefix": "/scratch/install",
            "exec_prefix": "/scratch/install",
            "path": ["/scratch/install/lib/python3.12/site-packages", "/project/src"],
        },
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
        "executables": {"gap": {"path": "/usr/bin/gap", "host_path": True}},
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
        "maxima": {
            "executable": "/usr/bin/maxima",
            "MAXIMA_PREFIX": "/usr",
            "sage_env_MAXIMA_FAS": None,
        },
        "fricas": {
            "executable": "/usr/bin/fricas",
            "FRICAS_PREFIX": "/usr",
            "FRICAS_INITFILE": None,
        },
        "fplll": {
            "companion_default_strategy": None,
            "companion_default_strategy_exists": False,
            "fpylll_version": "0.6.4",
            "fpylll_config_default_strategy": "/project/local/share/fplll/strategies/default.json",
            "sage_resolved_default_strategy": "/project/local/share/fplll/strategies/default.json",
            "sage_resolved_default_strategy_exists": False,
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
    assert diff["candidate_executable_host_leaks"] == [
        {"name": "gap", "path": "/usr/bin/gap"}
    ]
    assert diff["candidate_dependency_leaks"][0]["module"] == "sage/libs/example.so"
    assert diff["candidate_python_path_leaks"] == [
        {"path": "/project/src", "reason": "temporary or project build tree"}
    ]
    assert "sage.rings.rational" in diff["candidate_source_path_leaks"]
    assert diff["gap_package_program_differences"]["guava"][
        "candidate_complete"
    ] is False
    assert "/usr/share/gap" in diff["candidate_gap_host_leaks"]
    assert "/usr/share/gap/pkg/guava" in diff["candidate_gap_host_leaks"]
    assert diff["maxima_differences"]["executable"] == {
        "reference": "/sage/local/bin/maxima",
        "candidate": "/usr/bin/maxima",
    }
    assert diff["maxima_differences"]["sage_env_MAXIMA_FAS"] == {
        "reference": "/sage/local/lib/ecl/maxima.fas",
        "candidate": None,
    }
    assert diff["fricas_differences"]["FRICAS_INITFILE"] == {
        "reference": "/sage/local/lib/fricas/fricas.input",
        "candidate": None,
    }
    assert diff["fricas_differences"]["FRICAS_PREFIX"] == {
        "reference": "/sage/local",
        "candidate": "/usr",
    }
    assert diff["fplll_differences"]["fpylll_config_default_strategy"] == {
        "reference": "/sage/local/share/fplll/strategies/default.json",
        "candidate": "/project/local/share/fplll/strategies/default.json",
    }
    assert diff["fplll_differences"]["sage_resolved_default_strategy_exists"] == {
        "reference": True,
        "candidate": False,
    }

    markdown = manifest.render_diff_markdown(diff)
    assert "### Candidate executable host path leaks" in markdown
    assert "### Candidate Python path leaks" in markdown
    assert "### Maxima runtime differences" in markdown
    assert "### FriCAS runtime differences" in markdown
    assert "### FPLLL runtime differences" in markdown


def test_compare_manifests_reports_feature_collection_errors_without_null_diffs():
    manifest = _load_manifest()
    reference = {
        "label": "self-contained",
        "python": {"executable": "/usr/bin/python3"},
        "packages": [],
        "features": {"error": "ModuleNotFoundError: No module named 'sage'"},
        "executables": {},
    }
    candidate = {
        "label": "pip",
        "python": {"executable": "/scratch/install/bin/python"},
        "packages": [],
        "features": {
            "features": [
                {"name": "sage.libs.coxeter3", "present": True},
            ]
        },
        "executables": {},
    }

    diff = manifest.compare_manifests(reference, candidate)

    assert diff["feature_collection_errors"] == {
        "reference": "ModuleNotFoundError: No module named 'sage'",
    }
    assert diff["feature_differences"] == {}
    markdown = manifest.render_diff_markdown(diff)
    assert "### Feature collection issues" in markdown
    assert "### Feature presence differences\n\nCount: 0" in markdown


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
