from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EMPTY_FILE_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


def _load_validator():
    path = ROOT / "tools" / "validate-sagelite-wheelhouse.py"
    spec = importlib.util.spec_from_file_location("validate_sagelite_wheelhouse", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _companion_version(package: str) -> str:
    with (ROOT / "companion-packages" / package / "pyproject.toml").open("rb") as f:
        return tomllib.load(f)["project"]["version"]


def test_builds_fresh_install_and_full_validation_commands(tmp_path, monkeypatch):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    repaired_wheel = (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    )
    repaired_wheel.write_text("")
    (wheelhouse / "sagelite_gap_runtime-10.9-py3-none-any.whl").write_text("")
    install_dir = tmp_path / "install"
    output_dir = tmp_path / "validation"
    commands = []
    stale_environment = {
        "SAGE_ROOT": "/project/source",
        "SAGELITE_GAP_ROOT": "/tmp/stale-gap",
        "MAXIMA_PREFIX": "/tmp/stale-maxima",
        "FRICAS": "/tmp/stale-fricas",
        "ALDORROOT": "/tmp/stale-aldor",
        "FPLLL_DEFAULT_STRATEGY": "/project/local/share/fplll/strategies/default.json",
        "GAP_ROOT_PATHS": "/usr/share/gap",
        "MAXIMA": "/usr/bin/maxima",
    }
    for key, value in stale_environment.items():
        monkeypatch.setenv(key, value)

    def fake_run(command, env):
        commands.append(command)
        assert env["PYTHONNOUSERSITE"] == "1"
        assert "PYTHONPATH" not in env
        assert "LD_LIBRARY_PATH" not in env
        for key in stale_environment:
            assert key not in env
        return subprocess.CompletedProcess(command, 0)

    validator._timestamp = lambda: "20260621-010203"
    validator._run = fake_run

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--install-dir",
            str(install_dir),
            "--output-dir",
            str(output_dir),
            "--label",
            "cibw-proof",
            "--python",
            "/opt/python/cp312/bin/python",
            "--require-primary-sagelite-wheel-python-tag",
            "--require-primary-sagelite-wheel-abi-tag",
            "--require-primary-sagelite-wheel-platform-machine",
            "--full",
            "--nthreads",
            "4",
            "--manifest-compiled-limit",
            "250",
            "--",
            "--optional",
            "sage,optional,external",
        ]
    )

    assert exit_code == 0
    venv_python = install_dir / "bin" / "python"
    metadata = json.loads((output_dir / "install-metadata.json").read_text())
    summary = (output_dir / "validation-summary.md").read_text(encoding="utf-8")
    assert metadata["schema"] == "sagelite-wheelhouse-validation-install-v1"
    assert metadata["label"] == "cibw-proof"
    assert metadata["package"] == "sagelite[all-needed-extras]"
    assert metadata["base_python"] == "/opt/python/cp312/bin/python"
    assert metadata["install_dir"] == os.fspath(install_dir)
    assert metadata["venv_python"] == os.fspath(venv_python)
    assert metadata["wheelhouses"] == [os.fspath(wheelhouse.resolve())]
    assert metadata["wheelhouse_inventory"][
        "contains_repaired_primary_sagelite_wheel"
    ] is True
    assert metadata["wheelhouse_inventory"]["wheelhouse_input_identity"][
        "wheel_count"
    ] == 2
    assert metadata["wheelhouse_inventory"]["wheelhouse_input_identity"][
        "total_size_bytes"
    ] == 0
    assert (
        len(metadata["wheelhouse_inventory"]["wheelhouse_input_identity"]["sha256"])
        == 64
    )
    assert metadata["wheelhouse_inventory"][
        "contains_raw_linux_primary_sagelite_wheel"
    ] is False
    assert metadata["wheelhouse_inventory"][
        "contains_companion_sagelite_wheels"
    ] is True
    assert metadata["wheelhouse_inventory"]["contains_third_party_wheels"] is False
    assert metadata["wheelhouse_inventory"]["third_party_wheels"] == []
    assert [
        file["name"]
        for file in metadata["wheelhouse_inventory"]["companion_sagelite_wheels"]
    ] == ["sagelite_gap_runtime-10.9-py3-none-any.whl"]
    assert metadata["wheelhouse_inventory"]["companion_sagelite_package_names"] == [
        "sagelite-gap-runtime"
    ]
    assert "sagelite-gap-runtime" not in metadata["wheelhouse_inventory"][
        "missing_all_needed_extra_sagelite_packages"
    ]
    assert "sagelite-maxima-runtime" in metadata["wheelhouse_inventory"][
        "missing_all_needed_extra_sagelite_packages"
    ]
    assert metadata["wheelhouse_inventory"][
        "contains_all_needed_extra_sagelite_wheels"
    ] is False
    assert "brial" in metadata["native_wheel_catalog"]["required_meson_options"]
    assert (
        "sage.libs.ntl.error"
        in metadata["native_wheel_catalog"]["required_native_import_modules"]
    )
    assert "libntl" in metadata["native_wheel_catalog"][
        "required_native_library_prefixes"
    ]
    host = metadata["validation_host"]
    assert host["base_python"] == {
        "requested": "/opt/python/cp312/bin/python",
        "resolved_executable": None,
        "exists": False,
        "matches_controller": False,
        "tag_probe": {
            "attempted": False,
            "error": "base Python executable could not be resolved",
        },
    }
    assert host["controller_python"]["executable"] == sys.executable
    assert host["controller_python"]["cache_tag"]
    assert host["controller_python"]["sysconfig_platform"]
    assert metadata["validation_contract"]["expected_python_tag"] == "cp312"
    assert metadata["validation_contract"]["expected_abi_tag"] == "cp312"
    primary_compatibility = metadata["validation_contract"][
        "primary_sagelite_wheel_compatibility"
    ]
    assert primary_compatibility == [
        {
            "name": repaired_wheel.name,
            "project_name": "sagelite",
            "size_bytes": 0,
            "sha256": EMPTY_FILE_SHA256,
            "python_tags": ["cp312"],
            "abi_tags": ["cp312"],
            "platform_tags": ["manylinux_2_28_x86_64"],
            "python_compatible": True,
            "abi_compatible": True,
            "platform_compatible": True,
            "matched_platform_tags": ["manylinux_2_28_x86_64"],
            "repaired_linux": True,
            "raw_linux": False,
            "compatible": True,
            "mismatches": [],
        }
    ]
    assert metadata["validation_contract"]["incompatible_primary_sagelite_wheels"] == []
    assert "require-primary-sagelite-wheel-python-tag" in metadata[
        "validation_contract"
    ]["enabled_preflights"]
    assert "require-primary-sagelite-wheel-abi-tag" in metadata[
        "validation_contract"
    ]["enabled_preflights"]
    assert "reject-duplicate-primary-sagelite-wheels" not in metadata[
        "validation_contract"
    ]["enabled_preflights"]
    assert [
        file["name"]
        for file in metadata["wheelhouse_inventory"]["primary_sagelite_wheels"]
    ] == [repaired_wheel.name]
    assert metadata["status"] == "passed"
    assert metadata["exit_code"] == 0
    assert metadata["validation_started_at_utc"].endswith("Z")
    assert metadata["validation_finished_at_utc"].endswith("Z")
    assert isinstance(metadata["validation_elapsed_seconds"], float)
    assert metadata["environment"]["PYTHONNOUSERSITE"] == "1"
    assert metadata["environment"]["PYTHONPATH"] is None
    assert metadata["environment"]["LD_LIBRARY_PATH"] is None
    assert metadata["environment"]["GAP_ROOT_PATHS"] is None
    assert metadata["environment"]["MAXIMA"] is None
    assert metadata["removed_environment_keys"] == [
        "GAP_ROOT_PATHS",
        "LD_LIBRARY_PATH",
        "MAXIMA",
        "PYTHONPATH",
    ]
    assert metadata["removed_environment_prefixes"] == [
        "SAGE_",
        "SAGELITE_",
        "MAXIMA_",
        "FRICAS",
        "ALDOR",
        "FPLLL",
    ]
    assert commands == [
        ["/opt/python/cp312/bin/python", "-m", "venv", os.fspath(install_dir)],
        [os.fspath(venv_python), "-m", "pip", "install", "-U", "pip"],
        [
            os.fspath(venv_python),
            "-m",
            "pip",
            "install",
            "--no-index",
            "--find-links",
            os.fspath(wheelhouse.resolve()),
            "sagelite[all-needed-extras]",
        ],
        [os.fspath(venv_python), "-m", "pip", "check"],
        [
            os.fspath(venv_python),
            os.fspath(ROOT / "tools" / "run-installed-wheel-doctests.py"),
            "--python",
            os.fspath(venv_python),
            "--output-dir",
            os.fspath(output_dir),
            "--label",
            "cibw-proof",
            "--runtime-summary",
            "--selftest",
            "--nthreads",
            "4",
            "--full",
            "--manifest-compiled-limit",
            "250",
            "--wheelhouse",
            os.fspath(wheelhouse.resolve()),
            "--",
            "--optional",
            "sage,optional,external",
        ],
    ]
    assert metadata["commands"] == commands
    assert [result["returncode"] for result in metadata["command_results"]] == [
        0,
        0,
        0,
        0,
        0,
    ]
    assert [result["status"] for result in metadata["command_results"]] == [
        "passed",
        "passed",
        "passed",
        "passed",
        "passed",
    ]
    assert [result["command"] for result in metadata["command_results"]] == commands
    assert [result["index"] for result in metadata["command_results"]] == [
        1,
        2,
        3,
        4,
        5,
    ]
    assert [result["phase"] for result in metadata["command_results"]] == [
        "create virtual environment",
        "upgrade pip",
        "install wheelhouse package",
        "run pip check",
        "run installed doctest validation",
    ]
    assert all(
        isinstance(result["elapsed_seconds"], float)
        for result in metadata["command_results"]
    )
    assert all(
        result["started_at_utc"].endswith("Z")
        for result in metadata["command_results"]
    )
    assert all(
        result["finished_at_utc"].endswith("Z")
        for result in metadata["command_results"]
    )
    assert "# Sagelite wheelhouse validation: cibw-proof" in summary
    assert "- Status: `passed`" in summary
    assert "- Exit code: `0`" in summary
    assert "- Started at: `" in summary
    assert "- Finished at: `" in summary
    assert "- Elapsed seconds: `" in summary
    assert "- Base Python: `/opt/python/cp312/bin/python`" in summary
    assert "- Resolved base Python: `None`" in summary
    assert "- Controller Python:" in summary
    assert "- Staged wheel count: `2`" in summary
    assert "- Staged wheel total bytes: `0`" in summary
    assert "- Staged wheelhouse SHA256: `" in summary
    assert "- Primary compatibility checked wheels: `1`" in summary
    assert "- Primary compatibility passed wheels: `1`" in summary
    assert "- Incompatible primary sagelite wheels: `none`" in summary
    assert (
        f"  - `{repaired_wheel.name}`: compatible `True` "
        "(python: `True`; abi: `True`; platform: `True`; repaired: `True`; "
        "raw-linux: `False`; mismatches: `none`)"
    ) in summary
    assert "matched platform tags: `manylinux_2_28_x86_64`" in summary
    assert f"sha256 `{EMPTY_FILE_SHA256}`" in summary
    assert "- Base Python tag probe attempted: `False`" in summary
    assert "- Primary sagelite requirement: `sagelite[all-needed-extras]`" in summary
    assert "- Primary sagelite requirement specifier: ``" in summary
    assert "- Unsatisfied primary sagelite wheel requirements: `none`" in summary
    assert (
        f"  - `{repaired_wheel.name}`: version `10.9.post1`; "
        "specifier ``; satisfied `True`; "
        "reason `no sagelite version specifier requested`"
    ) in summary
    assert "- Expected wheel Python tag: `cp312`" in summary
    assert "- Expected wheel ABI tag: `cp312`" in summary
    assert "`require-primary-sagelite-wheel-python-tag`" in summary
    assert "`require-primary-sagelite-wheel-abi-tag`" in summary
    assert (
        f"- `{repaired_wheel.name}` "
        "(python: cp312; abi: cp312; platform: manylinux_2_28_x86_64)"
    ) in summary
    assert f"- size: 0; sha256: {EMPTY_FILE_SHA256}" in summary
    assert "- Companion sagelite wheels:" in summary
    assert "- `sagelite_gap_runtime-10.9-py3-none-any.whl`" in summary
    assert "- Third-party wheels:" in summary
    assert "- Contains companion sagelite wheels: `True`" in summary
    assert "- Contains third-party wheels: `False`" in summary
    assert "- Contains all-needed-extra sagelite wheels: `False`" in summary
    assert "- Companion sagelite package count: `1`" in summary
    assert "- Third-party wheel count: `0`" in summary
    assert "- Missing all-needed-extra sagelite package count: `28`" in summary
    assert "- Companion compatibility checked wheels: `1`" in summary
    assert "- Companion compatibility passed wheels: `1`" in summary
    assert (
        "  - `sagelite_gap_runtime-10.9-py3-none-any.whl`: compatible `True` "
        "(python: `True`; abi: `True`; platform: `True`; mismatches: `none`)"
    ) in summary
    assert "matched platform tags: `any`" in summary
    assert "`sagelite-maxima-runtime`" in summary
    assert "- Contains repaired primary sagelite wheel: `True`" in summary
    assert "## Native Wheel Catalog" in summary
    assert "- Required Meson options:" in summary
    assert "`brial`" in summary
    assert "- Required native import modules: `19`" in summary
    assert "`libntl`" in summary
    assert "### 5. run installed doctest validation: passed" in summary
    assert "- Started at: `" in summary
    assert "- Finished at: `" in summary
    assert "--optional sage,optional,external" in summary


def test_defaults_use_scratch_timestamped_paths_and_short_validation(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    commands = []

    def fake_run(command, env):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0)

    validator._timestamp = lambda: "20260621-020304"
    validator._run = fake_run

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--package",
            "sagelite",
        ]
    )

    assert exit_code == 0
    install_dir = tmp_path / "install-20260621-020304"
    output_dir = tmp_path / "validation-20260621-020304"
    venv_python = install_dir / "bin" / "python"
    metadata = json.loads((output_dir / "install-metadata.json").read_text())
    assert commands[2][-1] == "sagelite"
    assert metadata["label"] == "repaired-wheel-20260621-020304"
    assert metadata["package"] == "sagelite"
    assert metadata["commands"] == commands
    assert metadata["status"] == "passed"
    assert metadata["exit_code"] == 0
    assert metadata["validation_contract"]["enabled_preflights"] == []
    assert commands[4] == [
        os.fspath(venv_python),
        os.fspath(ROOT / "tools" / "run-installed-wheel-doctests.py"),
        "--python",
        os.fspath(venv_python),
        "--output-dir",
        os.fspath(output_dir),
        "--label",
        "repaired-wheel-20260621-020304",
        "--runtime-summary",
        "--selftest",
        "--nthreads",
        "1",
        "--short",
        "300",
        "--manifest-compiled-limit",
        "200",
        "--wheelhouse",
        os.fspath(wheelhouse.resolve()),
    ]


def test_validation_summary_uses_cached_inventory(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    wheel = wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    wheel.write_text("")
    inventory = validator.wheelhouse_inventory([wheelhouse])
    wheel.unlink()
    output_dir = tmp_path / "validation"
    output_dir.mkdir()

    validator.write_validation_summary(
        output_dir,
        label="cached-inventory",
        package="sagelite[all-needed-extras]",
        install_dir=tmp_path / "install",
        wheelhouses=[wheelhouse],
        inventory=inventory,
        status="running",
        exit_code=None,
    )

    summary = (output_dir / "validation-summary.md").read_text(encoding="utf-8")
    assert "- Staged wheel count: `1`" in summary
    assert f"- `{wheel.name}` (python: cp312; abi: cp312;" in summary
    assert f"- size: 0; sha256: {EMPTY_FILE_SHA256}" in summary


def test_contract_reports_third_party_wheel_compatibility(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    primary = (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    )
    primary.write_text("")
    universal = wheelhouse / "packaging-24.0-py3-none-any.whl"
    universal.write_text("")
    incompatible = wheelhouse / "cypari2-2.2.1-cp313-cp313-any.whl"
    incompatible.write_text("")
    install_dir = tmp_path / "install"
    output_dir = tmp_path / "validation"

    validator._run = lambda command, env: subprocess.CompletedProcess(command, 0)

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--install-dir",
            str(install_dir),
            "--output-dir",
            str(output_dir),
            "--python",
            "/opt/python/cp312/bin/python",
            "--require-primary-sagelite-wheel-python-tag",
            "--require-primary-sagelite-wheel-abi-tag",
        ]
    )

    assert exit_code == 0
    metadata = json.loads((output_dir / "install-metadata.json").read_text())
    summary = (output_dir / "validation-summary.md").read_text(encoding="utf-8")
    third_party_compatibility = metadata["validation_contract"][
        "third_party_wheel_compatibility"
    ]
    third_party_wheels = metadata["wheelhouse_inventory"]["third_party_wheels"]
    assert [item["name"] for item in third_party_wheels] == [
        incompatible.name,
        universal.name,
    ]
    assert metadata["wheelhouse_inventory"]["contains_third_party_wheels"] is True
    assert [item["name"] for item in third_party_compatibility] == [
        incompatible.name,
        universal.name,
    ]
    assert third_party_compatibility[0]["compatible"] is False
    assert third_party_compatibility[0]["mismatches"] == ["python", "abi"]
    assert third_party_compatibility[0]["matched_platform_tags"] == ["any"]
    assert third_party_compatibility[1]["compatible"] is True
    assert metadata["validation_contract"]["incompatible_third_party_wheels"] == [
        third_party_compatibility[0]
    ]
    assert "- Third-party compatibility checked wheels: `2`" in summary
    assert "- Third-party compatibility passed wheels: `1`" in summary
    assert "- Third-party wheels:" in summary
    assert "- Contains third-party wheels: `True`" in summary
    assert "- Third-party wheel count: `2`" in summary
    assert (
        f"- `{incompatible.name}` (python: cp313; abi: cp313; platform: any)"
        in summary
    )
    assert (
        f"- `{universal.name}` (python: py3; abi: none; platform: any)"
        in summary
    )
    assert f"- Incompatible third-party wheels: `{incompatible.name}`" in summary
    assert (
        f"  - `{incompatible.name}`: compatible `False` "
        "(python: `False`; abi: `False`; platform: `True`; "
        "mismatches: `python`, `abi`)"
    ) in summary


def test_require_compatible_third_party_wheels_rejects_mismatch(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    primary = (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    )
    primary.write_text("")
    incompatible = wheelhouse / "cypari2-2.2.1-cp313-cp313-any.whl"
    incompatible.write_text("")
    install_dir = tmp_path / "install"
    output_dir = tmp_path / "validation"
    commands = []

    validator._run = lambda command, env: commands.append(command)

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--install-dir",
            str(install_dir),
            "--output-dir",
            str(output_dir),
            "--python",
            "/opt/python/cp312/bin/python",
            "--require-compatible-third-party-wheels",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads((output_dir / "install-metadata.json").read_text())
    summary = (output_dir / "validation-summary.md").read_text(encoding="utf-8")
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "third-party wheels are not compatible" in metadata["preflight_error"]
    assert incompatible.name in metadata["preflight_error"]
    assert metadata["validation_contract"]["incompatible_third_party_wheels"][0][
        "name"
    ] == incompatible.name
    assert metadata["validation_contract"]["enabled_preflights"] == [
        "require-compatible-third-party-wheels"
    ]
    assert (
        "- Enabled preflights: `require-compatible-third-party-wheels`"
        in summary
    )
    assert f"- Incompatible third-party wheels: `{incompatible.name}`" in summary
    assert "## Preflight Error" in summary
    assert "mismatches: python, abi" in summary


def test_stops_after_failed_step(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    commands = []

    def fake_run(command, env):
        commands.append(command)
        return subprocess.CompletedProcess(command, 12 if len(commands) == 3 else 0)

    validator._timestamp = lambda: "20260621-030405"
    validator._run = fake_run

    exit_code = validator.main(
        ["--wheelhouse", str(wheelhouse), "--work-dir", str(tmp_path)]
    )

    assert exit_code == 12
    assert len(commands) == 3
    metadata = json.loads(
        (tmp_path / "validation-20260621-030405" / "install-metadata.json").read_text()
    )
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 12
    assert metadata["validation_started_at_utc"].endswith("Z")
    assert metadata["validation_finished_at_utc"].endswith("Z")
    assert isinstance(metadata["validation_elapsed_seconds"], float)
    assert metadata["commands"] == commands + [
        [
            os.fspath(tmp_path / "install-20260621-030405" / "bin" / "python"),
            "-m",
            "pip",
            "check",
        ],
        [
            os.fspath(tmp_path / "install-20260621-030405" / "bin" / "python"),
            os.fspath(ROOT / "tools" / "run-installed-wheel-doctests.py"),
            "--python",
            os.fspath(tmp_path / "install-20260621-030405" / "bin" / "python"),
            "--output-dir",
            os.fspath(tmp_path / "validation-20260621-030405"),
            "--label",
            "repaired-wheel-20260621-030405",
            "--runtime-summary",
            "--selftest",
            "--nthreads",
            "1",
            "--short",
            "300",
            "--manifest-compiled-limit",
            "200",
            "--wheelhouse",
            os.fspath(wheelhouse.resolve()),
        ],
    ]
    assert [result["status"] for result in metadata["command_results"]] == [
        "passed",
        "passed",
        "failed",
    ]
    assert [result["returncode"] for result in metadata["command_results"]] == [
        0,
        0,
        12,
    ]
    assert all(
        "started_at_utc" in result and "finished_at_utc" in result
        for result in metadata["command_results"]
    )
    assert [result["command"] for result in metadata["command_results"]] == commands
    assert [result["phase"] for result in metadata["command_results"]] == [
        "create virtual environment",
        "upgrade pip",
        "install wheelhouse package",
    ]
    summary = (
        tmp_path / "validation-20260621-030405" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    assert "### 3. install wheelhouse package: failed" in summary
    assert "- Controller Python:" in summary


def test_missing_wheelhouse_fails_before_creating_commands(tmp_path):
    validator = _load_validator()
    commands = []
    validator._run = lambda command, env: commands.append(command)

    try:
        validator.main(["--wheelhouse", str(tmp_path / "missing")])
    except FileNotFoundError as exc:
        assert "wheelhouse directory does not exist" in str(exc)
    else:
        raise AssertionError("expected FileNotFoundError")

    assert commands == []


def test_records_raw_linux_wheelhouse_inventory(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    raw_wheel = wheelhouse / "sagelite-10.9.post1-cp312-cp312-linux_x86_64.whl"
    raw_wheel.write_text("")
    (wheelhouse / "sagelite_fplll_data-10.9-py3-none-any.whl").write_text("")
    commands = []

    def fake_run(command, env):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0)

    validator._timestamp = lambda: "20260621-040506"
    validator._run = fake_run

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--package",
            "sagelite",
        ]
    )

    assert exit_code == 0
    metadata = json.loads(
        (tmp_path / "validation-20260621-040506" / "install-metadata.json").read_text()
    )
    inventory = metadata["wheelhouse_inventory"]
    assert inventory["contains_primary_sagelite_wheel"] is True
    assert inventory["contains_companion_sagelite_wheels"] is True
    assert inventory["contains_repaired_primary_sagelite_wheel"] is False
    assert inventory["contains_raw_linux_primary_sagelite_wheel"] is True
    assert inventory["primary_sagelite_wheels"] == [
        {
            "name": raw_wheel.name,
            "path": os.fspath(raw_wheel.resolve()),
            "wheelhouse": os.fspath(wheelhouse.resolve()),
            "project_name": "sagelite",
            "version": "10.9.post1",
            "size_bytes": 0,
            "sha256": EMPTY_FILE_SHA256,
            "python_tags": ["cp312"],
            "abi_tags": ["cp312"],
            "platform_tags": ["linux_x86_64"],
            "is_sagelite_project_wheel": True,
            "is_primary_sagelite_wheel": True,
            "is_repaired_linux_wheel": False,
            "is_raw_linux_wheel": True,
        }
    ]
    assert [
        wheel["name"] for wheel in inventory["companion_sagelite_wheels"]
    ] == ["sagelite_fplll_data-10.9-py3-none-any.whl"]
    assert inventory["companion_sagelite_package_names"] == ["sagelite-fplll-data"]
    assert inventory["companion_sagelite_wheels"][0]["version"] == "10.9"
    assert "sagelite-fplll-data" not in inventory[
        "missing_all_needed_extra_sagelite_packages"
    ]
    assert "sagelite-gap-runtime" in inventory[
        "missing_all_needed_extra_sagelite_packages"
    ]


def test_require_repaired_sagelite_wheel_rejects_raw_wheelhouse(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    raw_wheel = wheelhouse / "sagelite-10.9.post1-cp312-cp312-linux_x86_64.whl"
    raw_wheel.write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-050607"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--require-repaired-sagelite-wheel",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-050607" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-050607" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert metadata["validation_started_at_utc"].endswith("Z")
    assert metadata["validation_finished_at_utc"].endswith("Z")
    assert isinstance(metadata["validation_elapsed_seconds"], float)
    assert "repaired sagelite wheel is required" in metadata["preflight_error"]
    assert raw_wheel.name in metadata["preflight_error"]
    assert metadata["command_results"] == []
    assert (
        "sage.libs.ntl.error"
        in metadata["native_wheel_catalog"]["required_native_import_modules"]
    )
    assert metadata["wheelhouse_inventory"][
        "contains_raw_linux_primary_sagelite_wheel"
    ] is True
    assert "- Status: `failed`" in summary
    assert "- Exit code: `2`" in summary
    assert "- Enabled preflights: `require-repaired-sagelite-wheel`" in summary
    assert (
        f"- `{raw_wheel.name}` "
        "(python: cp312; abi: cp312; platform: linux_x86_64)"
    ) in summary
    assert "- Contains repaired primary sagelite wheel: `False`" in summary
    assert "- Contains raw Linux primary sagelite wheel: `True`" in summary
    assert "- Primary compatibility checked wheels: `1`" in summary
    assert "- Primary compatibility passed wheels: `0`" in summary
    assert f"- Incompatible primary sagelite wheels: `{raw_wheel.name}`" in summary
    assert (
        f"  - `{raw_wheel.name}`: compatible `False` "
        "(python: `True`; abi: `True`; platform: `True`; repaired: `False`; "
        "raw-linux: `True`; mismatches: `repaired`)"
    ) in summary
    assert "matched platform tags: `linux_x86_64`" in summary
    assert "## Native Wheel Catalog" in summary
    assert "## Preflight Error" in summary
    assert "repaired sagelite wheel is required" in summary


def test_strict_repaired_wheelhouse_preflight_rejects_raw_wheelhouse(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    raw_wheel = wheelhouse / "sagelite-10.9.post1-cp312-cp312-linux_x86_64.whl"
    raw_wheel.write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-081500"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--python",
            "/opt/python/cp312/bin/python",
            "--strict-repaired-wheelhouse-preflight",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-081500" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-081500" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    enabled_preflights = metadata["validation_contract"]["enabled_preflights"]
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "repaired sagelite wheel is required" in metadata["preflight_error"]
    assert raw_wheel.name in metadata["preflight_error"]
    assert enabled_preflights == [
        "strict-repaired-wheelhouse-preflight",
        "reject-duplicate-primary-sagelite-wheels",
        "require-repaired-sagelite-wheel",
        "require-package-all-needed-extras",
        "require-all-needed-extra-sagelite-wheels",
        "reject-duplicate-companion-sagelite-wheels",
        "require-sagelite-companion-wheel-requirements",
        "require-primary-sagelite-wheel-requirement",
        "require-compatible-companion-sagelite-wheels",
        "require-primary-sagelite-wheel-python-tag",
        "require-primary-sagelite-wheel-abi-tag",
        "require-primary-sagelite-wheel-platform-machine",
        "require-primary-sagelite-wheel-compatible-platform-tag",
    ]
    assert (
        "- Enabled preflights: "
        "`strict-repaired-wheelhouse-preflight`, "
        "`reject-duplicate-primary-sagelite-wheels`, "
        "`require-repaired-sagelite-wheel`, "
        "`require-package-all-needed-extras`, "
        "`require-all-needed-extra-sagelite-wheels`, "
        "`reject-duplicate-companion-sagelite-wheels`, "
        "`require-sagelite-companion-wheel-requirements`, "
        "`require-primary-sagelite-wheel-requirement`, "
        "`require-compatible-companion-sagelite-wheels`, "
        "`require-primary-sagelite-wheel-python-tag`, "
        "`require-primary-sagelite-wheel-abi-tag`, "
        "`require-primary-sagelite-wheel-platform-machine`, "
        "`require-primary-sagelite-wheel-compatible-platform-tag`"
    ) in summary
    assert "- Contains raw Linux primary sagelite wheel: `True`" in summary
    assert "## Preflight Error" in summary


def test_strict_repaired_wheelhouse_preflight_rejects_narrow_package(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    ).write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-081700"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--python",
            "/opt/python/cp312/bin/python",
            "--package",
            "sagelite",
            "--strict-repaired-wheelhouse-preflight",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-081700" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-081700" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    contract = metadata["validation_contract"]
    assert contract["primary_sagelite_requirement"] == {
        "package": "sagelite",
        "name": "sagelite",
        "extras": [],
        "specifier": "",
        "applies_to_sagelite": True,
        "requests_all_needed_extras": False,
        "error": None,
    }
    assert "strict repaired-wheelhouse validation must install" in metadata[
        "preflight_error"
    ]
    assert "requested package extras: none" in metadata["preflight_error"]
    assert "- Primary sagelite requirement extras: `none`" in summary
    assert "- Primary sagelite requests all-needed-extras: `False`" in summary
    assert "## Preflight Error" in summary


def test_require_package_all_needed_extras_allows_default_package(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    ).write_text("")
    commands = []
    def fake_run(command, env):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0)

    validator._run = fake_run
    validator._timestamp = lambda: "20260621-081900"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--python",
            "/opt/python/cp312/bin/python",
            "--require-package-all-needed-extras",
        ]
    )

    assert exit_code == 0
    assert len(commands) == 5
    metadata = json.loads(
        (tmp_path / "validation-20260621-081900" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-081900" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    contract = metadata["validation_contract"]
    assert contract["primary_sagelite_requirement"]["extras"] == [
        "all-needed-extras"
    ]
    assert contract["primary_sagelite_requirement"][
        "requests_all_needed_extras"
    ] is True
    assert metadata["preflight_error"] is None
    assert "- Primary sagelite requirement extras: `all-needed-extras`" in summary
    assert "- Primary sagelite requests all-needed-extras: `True`" in summary


def test_require_repaired_sagelite_wheel_rejects_missing_primary_wheel(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (wheelhouse / "sagelite_gap_runtime-10.9-py3-none-any.whl").write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-060708"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--require-repaired-sagelite-wheel",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-060708" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-060708" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "exactly one primary sagelite wheel is required" in metadata[
        "preflight_error"
    ]
    assert "primary sagelite wheels: none" in metadata["preflight_error"]
    assert metadata["wheelhouse_inventory"]["primary_sagelite_wheels"] == []
    assert "- Primary sagelite wheels:\n  - none" in summary
    assert (
        "- Companion sagelite wheels:\n"
        "  - `sagelite_gap_runtime-10.9-py3-none-any.whl`"
    ) in summary
    assert "- Contains companion sagelite wheels: `True`" in summary
    assert "- Contains all-needed-extra sagelite wheels: `False`" in summary
    assert "## Preflight Error" in summary
    assert "exactly one primary sagelite wheel is required" in summary


def test_require_all_needed_extra_sagelite_wheels_rejects_missing_companions(
    tmp_path,
):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    ).write_text("")
    (wheelhouse / "sagelite_gap_runtime-10.9-py3-none-any.whl").write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-063000"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--require-all-needed-extra-sagelite-wheels",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-063000" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-063000" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "all-needed-extras companion sagelite wheels are required" in metadata[
        "preflight_error"
    ]
    assert "sagelite-gap-runtime" not in metadata["preflight_error"]
    assert "sagelite-maxima-runtime" in metadata["preflight_error"]
    assert metadata["wheelhouse_inventory"][
        "contains_all_needed_extra_sagelite_wheels"
    ] is False
    assert "- Contains all-needed-extra sagelite wheels: `False`" in summary
    assert "- Missing all-needed-extra sagelite package count: `28`" in summary
    assert "`sagelite-maxima-runtime`" in summary
    assert "## Preflight Error" in summary
    assert "all-needed-extras companion sagelite wheels are required" in summary


def test_require_all_needed_extra_sagelite_wheels_allows_complete_companions(
    tmp_path,
):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    ).write_text("")
    for package in validator._all_needed_extra_sagelite_packages():
        wheel_name = package.replace("-", "_") + "-10.9-py3-none-any.whl"
        (wheelhouse / wheel_name).write_text("")
    commands = []

    def fake_run(command, env):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0)

    validator._timestamp = lambda: "20260621-063500"
    validator._run = fake_run

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--require-all-needed-extra-sagelite-wheels",
        ]
    )

    assert exit_code == 0
    assert len(commands) == 5
    metadata = json.loads(
        (tmp_path / "validation-20260621-063500" / "install-metadata.json").read_text()
    )
    assert metadata["status"] == "passed"
    assert metadata["wheelhouse_inventory"][
        "contains_all_needed_extra_sagelite_wheels"
    ] is True
    assert metadata["wheelhouse_inventory"][
        "missing_all_needed_extra_sagelite_packages"
    ] == []


def test_require_repaired_sagelite_wheel_rejects_mixed_primary_wheels(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    raw_wheel = wheelhouse / "sagelite-10.9.post1-cp312-cp312-linux_x86_64.whl"
    repaired_wheel = (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    )
    raw_wheel.write_text("")
    repaired_wheel.write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-070809"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--require-repaired-sagelite-wheel",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-070809" / "install-metadata.json").read_text()
    )
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "exactly one primary sagelite wheel is required" in metadata[
        "preflight_error"
    ]
    assert raw_wheel.name in metadata["preflight_error"]
    assert repaired_wheel.name in metadata["preflight_error"]
    assert metadata["wheelhouse_inventory"][
        "contains_repaired_primary_sagelite_wheel"
    ] is True
    assert metadata["wheelhouse_inventory"][
        "contains_raw_linux_primary_sagelite_wheel"
    ] is True
    assert metadata["wheelhouse_inventory"]["duplicate_primary_sagelite_wheel_names"] == [
        raw_wheel.name,
        repaired_wheel.name,
    ]


def test_reject_duplicate_primary_sagelite_wheels_preflight(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    py312_wheel = (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    )
    py313_wheel = (
        wheelhouse / "sagelite-10.9.post1-cp313-cp313-manylinux_2_28_x86_64.whl"
    )
    py312_wheel.write_text("")
    py313_wheel.write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-071300"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--reject-duplicate-primary-sagelite-wheels",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-071300" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-071300" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "duplicate primary sagelite wheels are not allowed" in metadata[
        "preflight_error"
    ]
    assert py312_wheel.name in metadata["preflight_error"]
    assert py313_wheel.name in metadata["preflight_error"]
    assert metadata["wheelhouse_inventory"]["duplicate_primary_sagelite_wheel_names"] == [
        py312_wheel.name,
        py313_wheel.name,
    ]
    assert (
        "- Enabled preflights: `reject-duplicate-primary-sagelite-wheels`"
    ) in summary
    assert (
        "- Duplicate primary sagelite wheels: "
        f"`{py312_wheel.name}`, `{py313_wheel.name}`"
    ) in summary
    assert "## Preflight Error" in summary
    assert "duplicate primary sagelite wheels are not allowed" in summary


def test_strict_repaired_wheelhouse_preflight_rejects_duplicate_primary_first(
    tmp_path,
):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    py312_wheel = (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    )
    py313_wheel = (
        wheelhouse / "sagelite-10.9.post1-cp313-cp313-manylinux_2_28_x86_64.whl"
    )
    py312_wheel.write_text("")
    py313_wheel.write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-071400"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--strict-repaired-wheelhouse-preflight",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-071400" / "install-metadata.json").read_text()
    )
    enabled = metadata["validation_contract"]["enabled_preflights"]
    assert enabled[:3] == [
        "strict-repaired-wheelhouse-preflight",
        "reject-duplicate-primary-sagelite-wheels",
        "require-repaired-sagelite-wheel",
    ]
    assert "duplicate primary sagelite wheels are not allowed" in metadata[
        "preflight_error"
    ]


def test_inventory_records_complete_all_needed_extra_companion_coverage(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    ).write_text("")
    expected_packages = validator._all_needed_extra_sagelite_packages()
    for package in expected_packages:
        version = _companion_version(package)
        wheel_name = package.replace("-", "_") + f"-{version}-py3-none-any.whl"
        (wheelhouse / wheel_name).write_text("")

    inventory = validator.wheelhouse_inventory([wheelhouse])

    assert inventory["contains_all_needed_extra_sagelite_wheels"] is True
    assert inventory["all_needed_extra_sagelite_packages"] == expected_packages
    assert inventory["companion_sagelite_package_names"] == expected_packages
    assert inventory["missing_all_needed_extra_sagelite_packages"] == []
    assert inventory["duplicate_companion_sagelite_package_names"] == []
    assert inventory["unsatisfied_companion_sagelite_requirements"] == []


def test_inventory_records_stable_wheelhouse_input_identity(tmp_path):
    validator = _load_validator()
    first_wheelhouse = tmp_path / "first-wheelhouse"
    second_wheelhouse = tmp_path / "second-wheelhouse"
    first_wheelhouse.mkdir()
    second_wheelhouse.mkdir()
    primary = first_wheelhouse / (
        "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    )
    companion = second_wheelhouse / "sagelite_gap_runtime-10.9-py3-none-any.whl"
    primary.write_text("primary")
    companion.write_text("companion")

    identity = validator.wheelhouse_inventory(
        [first_wheelhouse, second_wheelhouse]
    )["wheelhouse_input_identity"]
    reversed_identity = validator.wheelhouse_inventory(
        [second_wheelhouse, first_wheelhouse]
    )["wheelhouse_input_identity"]

    assert identity == reversed_identity
    assert identity["wheel_count"] == 2
    assert identity["total_size_bytes"] == len("primary") + len("companion")
    assert len(identity["sha256"]) == 64


def test_inventory_records_duplicate_companion_packages(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (wheelhouse / "sagelite_gap_runtime-10.9-py3-none-any.whl").write_text("")
    (wheelhouse / "sagelite_gap_runtime-10.9.post1-py3-none-any.whl").write_text("")

    inventory = validator.wheelhouse_inventory([wheelhouse])
    summary_dir = tmp_path / "validation"
    summary_dir.mkdir()
    validator.write_validation_summary(
        summary_dir,
        label="duplicates",
        package="sagelite[all-needed-extras]",
        install_dir=tmp_path / "install",
        wheelhouses=[wheelhouse],
        status="failed",
        exit_code=2,
    )
    summary = (summary_dir / "validation-summary.md").read_text(encoding="utf-8")

    assert inventory["companion_sagelite_package_names"] == ["sagelite-gap-runtime"]
    assert inventory["duplicate_companion_sagelite_package_names"] == [
        "sagelite-gap-runtime"
    ]
    assert "- Duplicate companion sagelite packages: `sagelite-gap-runtime`" in summary
    assert "- Unsatisfied companion sagelite requirements:" in summary


def test_reject_unsatisfied_companion_sagelite_requirements_preflight(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    ).write_text("")
    outdated_gap_runtime = wheelhouse / "sagelite_gap_runtime-10.9-py3-none-any.whl"
    outdated_gap_runtime.write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-071000"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--require-sagelite-companion-wheel-requirements",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-071000" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-071000" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    unsatisfied = metadata["wheelhouse_inventory"][
        "unsatisfied_companion_sagelite_requirements"
    ]
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "companion wheel versions do not satisfy" in metadata["preflight_error"]
    assert outdated_gap_runtime.name in metadata["preflight_error"]
    assert ">=10.9.post2" in metadata["preflight_error"]
    assert "<10.10" in metadata["preflight_error"]
    assert unsatisfied == [
        {
            "name": outdated_gap_runtime.name,
            "project_name": "sagelite-gap-runtime",
            "version": "10.9",
            "required_specifiers": ["<10.10,>=10.9.post2"],
            "reason": "version does not satisfy sagelite requirements",
        }
    ]
    assert (
        "- Enabled preflights: "
        "`require-sagelite-companion-wheel-requirements`"
    ) in summary
    assert (
        "- Unsatisfied companion sagelite requirements: "
        f"`{outdated_gap_runtime.name}`"
    ) in summary
    assert "## Preflight Error" in summary
    assert "companion wheel versions do not satisfy" in summary


def test_reject_unsatisfied_primary_sagelite_wheel_requirement_preflight(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    stale_primary = (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    )
    stale_primary.write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-071200"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--package",
            "sagelite==10.9.post2",
            "--require-primary-sagelite-wheel-requirement",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-071200" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-071200" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    contract = metadata["validation_contract"]
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "primary sagelite wheel version does not satisfy" in metadata[
        "preflight_error"
    ]
    assert stale_primary.name in metadata["preflight_error"]
    assert contract["primary_sagelite_requirement"] == {
        "package": "sagelite==10.9.post2",
        "name": "sagelite",
        "extras": [],
        "specifier": "==10.9.post2",
        "applies_to_sagelite": True,
        "requests_all_needed_extras": False,
        "error": None,
    }
    assert contract["unsatisfied_primary_sagelite_wheel_requirements"] == [
        {
            "name": stale_primary.name,
            "project_name": "sagelite",
            "version": "10.9.post1",
            "requested_package": "sagelite==10.9.post2",
            "required_specifier": "==10.9.post2",
            "satisfied": False,
            "reason": "version does not satisfy requested package requirement",
        }
    ]
    assert (
        "- Enabled preflights: "
        "`require-primary-sagelite-wheel-requirement`"
    ) in summary
    assert "- Primary sagelite requirement: `sagelite==10.9.post2`" in summary
    assert "- Primary sagelite requirement specifier: `==10.9.post2`" in summary
    assert (
        f"- Unsatisfied primary sagelite wheel requirements: `{stale_primary.name}`"
    ) in summary
    assert (
        f"  - `{stale_primary.name}`: version `10.9.post1`; "
        "specifier `==10.9.post2`; satisfied `False`; "
        "reason `version does not satisfy requested package requirement`"
    ) in summary
    assert "## Preflight Error" in summary


def test_reject_duplicate_companion_sagelite_wheels_preflight(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    ).write_text("")
    (wheelhouse / "sagelite_gap_runtime-10.9-py3-none-any.whl").write_text("")
    (wheelhouse / "sagelite_gap_runtime-10.9.post1-py3-none-any.whl").write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-071500"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--reject-duplicate-companion-sagelite-wheels",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-071500" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-071500" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "duplicate sagelite companion wheels are not allowed" in metadata[
        "preflight_error"
    ]
    assert "sagelite-gap-runtime" in metadata["preflight_error"]
    assert metadata["wheelhouse_inventory"][
        "duplicate_companion_sagelite_package_names"
    ] == ["sagelite-gap-runtime"]
    assert "- Duplicate companion sagelite packages: `sagelite-gap-runtime`" in summary
    assert "## Preflight Error" in summary
    assert "duplicate sagelite companion wheels are not allowed" in summary


def test_require_compatible_companion_sagelite_wheels_rejects_mismatch(
    tmp_path, monkeypatch
):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    ).write_text("")
    mismatched_companion = (
        wheelhouse
        / "sagelite_gap_runtime-10.9-cp313-cp313-manylinux_2_28_x86_64.whl"
    )
    mismatched_companion.write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-072000"
    monkeypatch.setattr(
        validator,
        "_compatible_platform_tags",
        lambda: ["manylinux_2_28_x86_64", "linux_x86_64"],
    )

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--python",
            "/opt/python/cp312/bin/python",
            "--require-compatible-companion-sagelite-wheels",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-072000" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-072000" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "companion wheels are not compatible" in metadata["preflight_error"]
    assert mismatched_companion.name in metadata["preflight_error"]
    companion_wheel = metadata["wheelhouse_inventory"]["companion_sagelite_wheels"][0]
    assert companion_wheel["python_tags"] == ["cp313"]
    assert companion_wheel["abi_tags"] == ["cp313"]
    incompatibility = metadata["validation_contract"][
        "incompatible_companion_sagelite_wheels"
    ][0]
    assert incompatibility["name"] == mismatched_companion.name
    assert incompatibility["python_compatible"] is False
    assert incompatibility["abi_compatible"] is False
    assert incompatibility["platform_compatible"] is True
    assert incompatibility["matched_platform_tags"] == ["manylinux_2_28_x86_64"]
    assert incompatibility["mismatches"] == ["python", "abi"]
    assert (
        f"- `{mismatched_companion.name}` "
        "(python: cp313; abi: cp313; platform: manylinux_2_28_x86_64)"
    ) in summary
    assert (
        f"- Incompatible companion sagelite wheels: "
        f"`{mismatched_companion.name}`"
    ) in summary
    assert (
        f"  - `{mismatched_companion.name}`: compatible `False` "
        "(python: `False`; abi: `False`; platform: `True`; "
        "mismatches: `python`, `abi`)"
    ) in summary
    assert "matched platform tags: `manylinux_2_28_x86_64`" in summary
    assert "- Companion compatibility checked wheels: `1`" in summary
    assert "- Companion compatibility passed wheels: `0`" in summary
    assert "## Preflight Error" in summary
    assert "companion wheels are not compatible" in summary
    assert "mismatches: python, abi" in summary


def test_require_compatible_companion_sagelite_wheels_allows_usable_tags(
    tmp_path, monkeypatch
):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    ).write_text("")
    (wheelhouse / "sagelite_gap_runtime-10.9-py3-none-any.whl").write_text("")
    (
        wheelhouse
        / "sagelite_maxima_runtime-10.9-cp312-cp312-manylinux_2_28_x86_64.whl"
    ).write_text("")
    commands = []

    def fake_run(command, env):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0)

    validator._run = fake_run
    validator._timestamp = lambda: "20260621-072100"
    monkeypatch.setattr(
        validator,
        "_compatible_platform_tags",
        lambda: ["manylinux_2_28_x86_64", "linux_x86_64"],
    )

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--python",
            "/opt/python/cp312/bin/python",
            "--require-compatible-companion-sagelite-wheels",
        ]
    )

    assert exit_code == 0
    assert len(commands) == 5
    metadata = json.loads(
        (tmp_path / "validation-20260621-072100" / "install-metadata.json").read_text()
    )
    assert metadata["status"] == "passed"
    assert metadata["preflight_error"] is None
    assert metadata["validation_contract"][
        "incompatible_companion_sagelite_wheels"
    ] == []
    companion_compatibility = metadata["validation_contract"][
        "companion_sagelite_wheel_compatibility"
    ]
    assert companion_compatibility[0]["matched_platform_tags"] == ["any"]
    assert companion_compatibility[1]["matched_platform_tags"] == [
        "manylinux_2_28_x86_64"
    ]
    summary = (
        tmp_path / "validation-20260621-072100" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    assert "- Companion compatibility checked wheels: `2`" in summary
    assert "- Companion compatibility passed wheels: `2`" in summary
    assert (
        "  - `sagelite_gap_runtime-10.9-py3-none-any.whl`: compatible `True` "
        "(python: `True`; abi: `True`; platform: `True`; mismatches: `none`)"
    ) in summary
    assert (
        "  - `sagelite_maxima_runtime-10.9-cp312-cp312-manylinux_2_28_x86_64.whl`: "
        "compatible `True` "
        "(python: `True`; abi: `True`; platform: `True`; mismatches: `none`)"
    ) in summary


def test_require_primary_sagelite_wheel_python_tag_rejects_mismatch(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    mismatched_wheel = (
        wheelhouse / "sagelite-10.9.post1-cp313-cp313-manylinux_2_28_x86_64.whl"
    )
    mismatched_wheel.write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-072500"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--python",
            "/opt/python/cp312/bin/python",
            "--require-repaired-sagelite-wheel",
            "--require-primary-sagelite-wheel-python-tag",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-072500" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-072500" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "Python tag does not match requested base Python tag cp312" in metadata[
        "preflight_error"
    ]
    assert mismatched_wheel.name in metadata["preflight_error"]
    assert metadata["wheelhouse_inventory"]["primary_sagelite_wheels"][0][
        "python_tags"
    ] == ["cp313"]
    assert (
        f"- `{mismatched_wheel.name}` "
        "(python: cp313; abi: cp313; platform: manylinux_2_28_x86_64)"
    ) in summary
    assert "## Preflight Error" in summary
    assert "Python tag does not match requested base Python tag cp312" in summary


def test_require_primary_sagelite_wheel_abi_tag_rejects_mismatch(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    mismatched_wheel = (
        wheelhouse / "sagelite-10.9.post1-cp312-cp313-manylinux_2_28_x86_64.whl"
    )
    mismatched_wheel.write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-073000"

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--python",
            "/opt/python/cp312/bin/python",
            "--require-repaired-sagelite-wheel",
            "--require-primary-sagelite-wheel-python-tag",
            "--require-primary-sagelite-wheel-abi-tag",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-073000" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-073000" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "ABI tag does not match requested base Python ABI tag cp312" in metadata[
        "preflight_error"
    ]
    assert mismatched_wheel.name in metadata["preflight_error"]
    primary_wheel = metadata["wheelhouse_inventory"]["primary_sagelite_wheels"][0]
    assert primary_wheel["python_tags"] == ["cp312"]
    assert primary_wheel["abi_tags"] == ["cp313"]
    assert (
        f"- `{mismatched_wheel.name}` "
        "(python: cp312; abi: cp313; platform: manylinux_2_28_x86_64)"
    ) in summary
    assert "## Preflight Error" in summary
    assert "ABI tag does not match requested base Python ABI tag cp312" in summary


def test_require_primary_sagelite_wheel_platform_machine_rejects_mismatch(
    tmp_path, monkeypatch
):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    mismatched_wheel = (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_aarch64.whl"
    )
    mismatched_wheel.write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-073500"
    monkeypatch.setattr(validator.platform, "machine", lambda: "x86_64")

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--python",
            "/opt/python/cp312/bin/python",
            "--require-repaired-sagelite-wheel",
            "--require-primary-sagelite-wheel-python-tag",
            "--require-primary-sagelite-wheel-abi-tag",
            "--require-primary-sagelite-wheel-platform-machine",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-073500" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-073500" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "platform tag does not match validation host machine x86_64" in metadata[
        "preflight_error"
    ]
    assert mismatched_wheel.name in metadata["preflight_error"]
    assert metadata["validation_host"]["controller_python"]["machine"] == "x86_64"
    primary_wheel = metadata["wheelhouse_inventory"]["primary_sagelite_wheels"][0]
    assert primary_wheel["platform_tags"] == ["manylinux_2_28_aarch64"]
    assert (
        f"- `{mismatched_wheel.name}` "
        "(python: cp312; abi: cp312; platform: manylinux_2_28_aarch64)"
    ) in summary
    assert "## Preflight Error" in summary
    assert "platform tag does not match validation host machine x86_64" in summary


def test_require_primary_sagelite_wheel_compatible_platform_tag_rejects_mismatch(
    tmp_path, monkeypatch
):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    mismatched_wheel = (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_99_x86_64.whl"
    )
    mismatched_wheel.write_text("")
    commands = []
    validator._run = lambda command, env: commands.append(command)
    validator._timestamp = lambda: "20260621-074000"
    monkeypatch.setattr(validator.platform, "machine", lambda: "x86_64")
    monkeypatch.setattr(
        validator,
        "_compatible_platform_tags",
        lambda: ["manylinux_2_28_x86_64", "linux_x86_64"],
    )

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--python",
            "/opt/python/cp312/bin/python",
            "--require-repaired-sagelite-wheel",
            "--require-primary-sagelite-wheel-python-tag",
            "--require-primary-sagelite-wheel-abi-tag",
            "--require-primary-sagelite-wheel-platform-machine",
            "--require-primary-sagelite-wheel-compatible-platform-tag",
        ]
    )

    assert exit_code == 2
    assert commands == []
    metadata = json.loads(
        (tmp_path / "validation-20260621-074000" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-074000" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    assert metadata["status"] == "failed"
    assert metadata["exit_code"] == 2
    assert "platform tag is not compatible with the validation host" in metadata[
        "preflight_error"
    ]
    assert "manylinux_2_28_x86_64" in metadata["preflight_error"]
    assert mismatched_wheel.name in metadata["preflight_error"]
    controller = metadata["validation_host"]["controller_python"]
    assert controller["compatible_platform_tag_count"] == 2
    assert controller["compatible_platform_tags_sample"] == [
        "manylinux_2_28_x86_64",
        "linux_x86_64",
    ]
    contract = metadata["validation_contract"]
    assert contract["expected_python_tag"] == "cp312"
    assert contract["expected_abi_tag"] == "cp312"
    assert contract["expected_platform_machine"] == "x86_64"
    primary_compatibility = contract["primary_sagelite_wheel_compatibility"]
    assert primary_compatibility[0]["name"] == mismatched_wheel.name
    assert primary_compatibility[0]["python_compatible"] is True
    assert primary_compatibility[0]["abi_compatible"] is True
    assert primary_compatibility[0]["platform_compatible"] is False
    assert primary_compatibility[0]["matched_platform_tags"] == []
    assert primary_compatibility[0]["repaired_linux"] is True
    assert primary_compatibility[0]["compatible"] is False
    assert primary_compatibility[0]["mismatches"] == ["platform"]
    assert contract["incompatible_primary_sagelite_wheels"][0]["name"] == (
        mismatched_wheel.name
    )
    assert contract["compatible_platform_tag_count"] == 2
    assert contract["compatible_platform_tags_sample"] == [
        "manylinux_2_28_x86_64",
        "linux_x86_64",
    ]
    assert "require-primary-sagelite-wheel-compatible-platform-tag" in contract[
        "enabled_preflights"
    ]
    primary_wheel = metadata["wheelhouse_inventory"]["primary_sagelite_wheels"][0]
    assert primary_wheel["platform_tags"] == ["manylinux_2_99_x86_64"]
    assert (
        f"- `{mismatched_wheel.name}` "
        "(python: cp312; abi: cp312; platform: manylinux_2_99_x86_64)"
    ) in summary
    assert "- Primary compatibility checked wheels: `1`" in summary
    assert "- Primary compatibility passed wheels: `0`" in summary
    assert (
        f"- Incompatible primary sagelite wheels: `{mismatched_wheel.name}`"
    ) in summary
    assert (
        f"  - `{mismatched_wheel.name}`: compatible `False` "
        "(python: `True`; abi: `True`; platform: `False`; repaired: `True`; "
        "raw-linux: `False`; mismatches: `platform`)"
    ) in summary
    assert "- Controller compatible platform tag count: `2`" in summary
    assert "## Preflight Error" in summary
    assert "platform tag is not compatible with the validation host" in summary


def test_platform_tag_preflight_uses_base_python_probe_tags(tmp_path, monkeypatch):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    wheel = wheelhouse / (
        "sagelite-10.9.post1-cp312-cp312-manylinux_2_17_x86_64.whl"
    )
    wheel.write_text("")
    commands = []

    def fake_run(command, env):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0)

    validator._run = fake_run
    validator._timestamp = lambda: "20260621-074500"
    monkeypatch.setattr(
        validator,
        "_compatible_platform_tags",
        lambda: ["manylinux_2_28_x86_64", "linux_x86_64"],
    )
    monkeypatch.setattr(
        validator,
        "validation_host_context",
        lambda base_python: {
            "controller_python": {
                "executable": sys.executable,
                "version": "3.12.4",
                "sysconfig_platform": "linux-x86_64",
                "machine": "x86_64",
                "compatible_platform_tag_count": 2,
                "compatible_platform_tags_sample": [
                    "manylinux_2_28_x86_64",
                    "linux_x86_64",
                ],
            },
            "base_python": {
                "requested": base_python,
                "resolved_executable": "/opt/python/cp312/bin/python",
                "exists": True,
                "matches_controller": False,
                "tag_probe": {
                    "attempted": True,
                    "cache_tag": "cpython-312",
                    "compatible_platform_tags": [
                        "manylinux_2_17_x86_64",
                        "linux_x86_64",
                    ],
                    "compatible_platform_tags_sample": [
                        "manylinux_2_17_x86_64",
                        "linux_x86_64",
                    ],
                    "compatible_platform_tag_count": 2,
                },
            },
        },
    )

    exit_code = validator.main(
        [
            "--wheelhouse",
            str(wheelhouse),
            "--work-dir",
            str(tmp_path),
            "--python",
            "/custom/interpreter",
            "--require-primary-sagelite-wheel-python-tag",
            "--require-primary-sagelite-wheel-abi-tag",
            "--require-primary-sagelite-wheel-compatible-platform-tag",
        ]
    )

    assert exit_code == 0
    assert len(commands) == 5
    metadata = json.loads(
        (tmp_path / "validation-20260621-074500" / "install-metadata.json").read_text()
    )
    summary = (
        tmp_path / "validation-20260621-074500" / "validation-summary.md"
    ).read_text(encoding="utf-8")
    contract = metadata["validation_contract"]
    assert contract["expected_python_tag"] == "cp312"
    assert contract["compatible_platform_tag_source"] == "base-python-probe"
    assert contract["compatible_platform_tag_count"] == 2
    assert contract["compatible_platform_tags_sample"] == [
        "manylinux_2_17_x86_64",
        "linux_x86_64",
    ]
    assert contract["primary_sagelite_wheel_compatibility"][0][
        "matched_platform_tags"
    ] == ["manylinux_2_17_x86_64"]
    assert metadata["status"] == "passed"
    assert metadata["preflight_error"] is None
    assert (
        f"- `{wheel.name}` "
        "(python: cp312; abi: cp312; platform: manylinux_2_17_x86_64)"
    ) in summary
    assert "- Compatible platform tag source: `base-python-probe`" in summary


def test_requested_python_wheel_tag_uses_base_python_probe_cache_tag():
    validator = _load_validator()

    assert (
        validator._requested_python_wheel_tag(
            "/custom/interpreter",
            {
                "base_python": {
                    "matches_controller": False,
                    "tag_probe": {"cache_tag": "cpython-313"},
                },
            },
        )
        == "cp313"
    )


def test_summary_renders_base_python_probe_details(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    summary_dir = tmp_path / "validation"
    summary_dir.mkdir()

    validator.write_validation_summary(
        summary_dir,
        label="base-probe",
        package="sagelite[all-needed-extras]",
        install_dir=tmp_path / "install",
        wheelhouses=[wheelhouse],
        status="failed",
        exit_code=2,
        host_context={
            "controller_python": {
                "executable": "/controller/python",
                "version": "3.12.4",
                "sysconfig_platform": "linux-x86_64",
                "compatible_platform_tag_count": 2,
            },
            "base_python": {
                "requested": "/custom/interpreter",
                "resolved_executable": "/custom/interpreter",
                "tag_probe": {
                    "attempted": True,
                    "python_version": "3.13.1",
                    "cache_tag": "cpython-313",
                    "sysconfig_platform": "linux-x86_64",
                    "packaging_tags_available": True,
                    "compatible_platform_tag_count": 2,
                    "compatible_tags_sample": [
                        "cp313-cp313-manylinux_2_28_x86_64",
                        "cp313-cp313-linux_x86_64",
                    ],
                },
            },
        },
    )

    summary = (summary_dir / "validation-summary.md").read_text(encoding="utf-8")
    assert "- Base Python probe version: `3.13.1`" in summary
    assert "- Base Python probe cache tag: `cpython-313`" in summary
    assert "- Base Python probe platform: `linux-x86_64`" in summary
    assert (
        "- Base Python compatible tag sample: "
        "`cp313-cp313-manylinux_2_28_x86_64`, `cp313-cp313-linux_x86_64`"
    ) in summary
