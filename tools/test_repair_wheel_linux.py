from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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
    assert script.index('inject_native_include_headers "$repaired_input"') < script.index(
        'auditwheel repair --plat "$AUDITWHEEL_PLAT"'
    )
