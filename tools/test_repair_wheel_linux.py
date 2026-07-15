from pathlib import Path


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
    assert 'companion_wheels=("${companion_output_dir}"/*.whl)' in wrapper
    assert 'mv "${companion_wheels[@]}" "${output_dir}/"' in wrapper
    assert (
        "SAGELITE_COMPANION_WHEEL_DIR=/host/sagelite-companion-wheelhouse "
        "bash .github/workflows/repair-wheel-linux.sh {wheel} {dest_dir}"
    ) in workflow


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
