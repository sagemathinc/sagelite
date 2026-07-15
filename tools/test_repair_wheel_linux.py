import os
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]


def test_linux_cibuildwheel_stages_companions_outside_repair_destination():
    repair = (ROOT / ".github/workflows/repair-wheel-linux.sh").read_text()
    wrapper = (ROOT / ".github/workflows/cibw-build-wheel-linux.sh").read_text()
    workflow = (ROOT / ".github/workflows/release.yml").read_text()

    assert 'companion_dest_dir="${SAGELITE_COMPANION_WHEEL_DIR:-}"' in repair
    assert 'primary_dest_dir="$dest_dir"' in repair
    assert 'if [ "$companion_dest_dir" = "$dest_dir" ]' in repair
    assert repair.index(
        'auditwheel repair --plat "$AUDITWHEEL_PLAT" -w "$dest_dir"'
    ) < repair.index('dest_dir="$companion_dest_dir"')
    maxima_builder = repair.split("build_maxima_runtime_companion() {", 1)[1].split(
        "build_meataxe_runtime_companion() {", 1
    )[0]
    assert 'find "$primary_dest_dir"' in maxima_builder
    assert 'repaired sagelite wheel not found in $primary_dest_dir' in maxima_builder
    assert 'companion_output_dir="$(pwd)/sagelite-companion-wheelhouse"' in wrapper
    assert 'companion_container_dir="/host${companion_output_dir}"' in wrapper
    assert 'repair_command="${CIBW_REPAIR_WHEEL_COMMAND_LINUX:-}"' in wrapper
    assert '"$repair_command" != *"$companion_output_marker"*' in wrapper
    assert (
        'CIBW_REPAIR_WHEEL_COMMAND_LINUX="${repair_command//'
        '$companion_output_marker/$companion_container_dir}"'
    ) in wrapper
    assert 'companion_wheels=("${companion_output_dir}"/*.whl)' in wrapper
    assert 'mv "${companion_wheels[@]}" "${output_dir}/"' in wrapper
    assert (
        "SAGELITE_COMPANION_WHEEL_DIR=__SAGELITE_HOST_COMPANION_WHEEL_DIR__ "
        "bash .github/workflows/repair-wheel-linux.sh {wheel} {dest_dir}"
    ) in workflow
    assert "/host/sagelite-companion-wheelhouse" not in workflow


def test_linux_cibuildwheel_maps_companion_stage_into_host_mount(tmp_path):
    wrapper = ROOT / ".github/workflows/cibw-build-wheel-linux.sh"
    fake_python = tmp_path / "fake-python"
    fake_python.write_text(
        "#!/bin/sh\n"
        "printf '%s\\n' \"$CIBW_REPAIR_WHEEL_COMMAND_LINUX\" > repair-command.txt\n"
        "touch sagelite-companion-wheelhouse/companion.whl\n"
    )
    fake_python.chmod(0o755)
    output_dir = tmp_path / "wheelhouse"
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    env = os.environ.copy()
    env["CIBW_REPAIR_WHEEL_COMMAND_LINUX"] = (
        "SAGELITE_COMPANION_WHEEL_DIR=__SAGELITE_HOST_COMPANION_WHEEL_DIR__ "
        "bash repair.sh {wheel} {dest_dir}"
    )

    subprocess.run(
        ["bash", wrapper, fake_python, output_dir, source_dir],
        cwd=tmp_path,
        env=env,
        check=True,
    )

    repair_command = (tmp_path / "repair-command.txt").read_text().strip()
    assert (
        f"SAGELITE_COMPANION_WHEEL_DIR=/host{tmp_path}/"
        "sagelite-companion-wheelhouse"
    ) in repair_command
    assert (output_dir / "companion.whl").is_file()
    assert not (tmp_path / "sagelite-companion-wheelhouse").exists()


def test_repair_wheel_linux_preserves_cython_source_sidecars():
    script = (ROOT / ".github" / "workflows" / "repair-wheel-linux.sh").read_text()

    assert "pruned-wheel" not in script
    assert "wheel unpack" not in script
    assert "wheel pack" not in script
    assert "-name '*.pyx'" not in script
    assert "-name '*.pxd'" not in script
    assert "-name '*.pxi'" not in script
    assert 'repaired_input="$tmpdir/${raw_wheel##*/}"' in script


def test_repair_wheel_linux_injects_native_headers_before_auditwheel():
    script = (ROOT / ".github" / "workflows" / "repair-wheel-linux.sh").read_text()
    header_injector = script.split("inject_native_include_headers() {", 1)[1].split(
        'if [ -z "${AUDITWHEEL_PLAT:-}" ]', 1
    )[0]

    assert "inject_native_include_headers()" in script
    assert 'local include_dir="$prefix/include"' in script
    assert 'prefix = "sage/include/"' in script
    assert "cp312-cp312" not in header_injector
    assert 'inject_native_include_headers "$repaired_input"' in script
    assert script.index('inject_native_include_headers "$repaired_input"') < script.rindex(
        'auditwheel repair --plat "$AUDITWHEEL_PLAT"'
    )


def test_repair_wheel_linux_pins_build_frontend():
    script = (ROOT / ".github" / "workflows" / "repair-wheel-linux.sh").read_text()

    install_lines = [
        line
        for line in script.splitlines()
        if "pip install --upgrade" in line and "setuptools wheel" in line
    ]
    assert install_lines
    assert all("'build==1.2.2.post1'" in line for line in install_lines)
    assert "    'build==1.2.2.post1' meson-python" in script

    frontend = script.split("prepare_repair_build_frontend() {", 1)[1].split(
        "build_companion_wheel() {", 1
    )[0]
    assert "--ignore-installed" in frontend
    assert "--no-deps" in frontend
    assert "'build==1.2.2.post1'" in frontend
    assert '"$python_bin" -m build --version' in frontend
    assert script.index("prepare_repair_build_frontend\n") < script.index(
        "build_pplpy_wheel\n"
    )


def test_repair_wheel_linux_keeps_selected_python_when_prefix_leads_path():
    script = (ROOT / ".github" / "workflows" / "repair-wheel-linux.sh").read_text()

    assert 'python_bin="$(command -v "${PYTHON:-python3}")"' in script
    assert 'PATH="$prefix/bin:$PATH"' in script
