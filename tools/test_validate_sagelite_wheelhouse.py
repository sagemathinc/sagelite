from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_validator():
    path = ROOT / "tools" / "validate-sagelite-wheelhouse.py"
    spec = importlib.util.spec_from_file_location("validate_sagelite_wheelhouse", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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
    assert metadata["wheelhouse_inventory"][
        "contains_raw_linux_primary_sagelite_wheel"
    ] is False
    assert metadata["wheelhouse_inventory"][
        "contains_companion_sagelite_wheels"
    ] is True
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
    }
    assert host["controller_python"]["executable"] == sys.executable
    assert host["controller_python"]["cache_tag"]
    assert host["controller_python"]["sysconfig_platform"]
    assert [
        file["name"]
        for file in metadata["wheelhouse_inventory"]["primary_sagelite_wheels"]
    ] == [repaired_wheel.name]
    assert metadata["status"] == "passed"
    assert metadata["exit_code"] == 0
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
    assert "# Sagelite wheelhouse validation: cibw-proof" in summary
    assert "- Status: `passed`" in summary
    assert "- Exit code: `0`" in summary
    assert "- Base Python: `/opt/python/cp312/bin/python`" in summary
    assert "- Resolved base Python: `None`" in summary
    assert "- Controller Python:" in summary
    assert (
        f"- `{repaired_wheel.name}` "
        "(python: cp312; abi: cp312; platform: manylinux_2_28_x86_64)"
    ) in summary
    assert "- Companion sagelite wheels:" in summary
    assert "- `sagelite_gap_runtime-10.9-py3-none-any.whl`" in summary
    assert "- Contains companion sagelite wheels: `True`" in summary
    assert "- Contains all-needed-extra sagelite wheels: `False`" in summary
    assert "- Companion sagelite package count: `1`" in summary
    assert "- Missing all-needed-extra sagelite package count: `28`" in summary
    assert "`sagelite-maxima-runtime`" in summary
    assert "- Contains repaired primary sagelite wheel: `True`" in summary
    assert "## Native Wheel Catalog" in summary
    assert "- Required Meson options:" in summary
    assert "`brial`" in summary
    assert "- Required native import modules: `19`" in summary
    assert "`libntl`" in summary
    assert "### 5. run installed doctest validation: passed" in summary
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
    assert (
        f"- `{raw_wheel.name}` "
        "(python: cp312; abi: cp312; platform: linux_x86_64)"
    ) in summary
    assert "- Contains repaired primary sagelite wheel: `False`" in summary
    assert "- Contains raw Linux primary sagelite wheel: `True`" in summary
    assert "## Native Wheel Catalog" in summary
    assert "## Preflight Error" in summary
    assert "repaired sagelite wheel is required" in summary


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


def test_inventory_records_complete_all_needed_extra_companion_coverage(tmp_path):
    validator = _load_validator()
    wheelhouse = tmp_path / "wheelhouse"
    wheelhouse.mkdir()
    (
        wheelhouse / "sagelite-10.9.post1-cp312-cp312-manylinux_2_28_x86_64.whl"
    ).write_text("")
    expected_packages = validator._all_needed_extra_sagelite_packages()
    for package in expected_packages:
        wheel_name = package.replace("-", "_") + "-10.9-py3-none-any.whl"
        (wheelhouse / wheel_name).write_text("")

    inventory = validator.wheelhouse_inventory([wheelhouse])

    assert inventory["contains_all_needed_extra_sagelite_wheels"] is True
    assert inventory["all_needed_extra_sagelite_packages"] == expected_packages
    assert inventory["companion_sagelite_package_names"] == expected_packages
    assert inventory["missing_all_needed_extra_sagelite_packages"] == []
    assert inventory["duplicate_companion_sagelite_package_names"] == []


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
