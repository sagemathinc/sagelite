import importlib.util
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TABLES_PATH = (
    ROOT
    / "companion-packages"
    / "sagelite-meataxe-runtime"
    / "src"
    / "sagelite_meataxe"
    / "tables.py"
)


def _load_tables_module():
    spec = importlib.util.spec_from_file_location("sagelite_meataxe_tables", TABLES_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _write_table(path: Path, *, field_size: int = 9, version: int = 6) -> None:
    tables = _load_tables_module()
    payload = bytearray(tables.TABLE_SIZE)
    payload[:20] = struct.pack("<5I", 3, 3, field_size, 2, version)
    path.write_bytes(payload)


def test_table_validator_accepts_shared_meataxe_1_0_2_format(tmp_path):
    tables = _load_tables_module()
    table = tmp_path / "p009.zzz"
    _write_table(table)

    assert tables.validate_table(table, 9) is None
    assert tables.table_errors(tmp_path, (9,)) == []


def test_table_validator_rejects_synthetic_text_fixture(tmp_path):
    tables = _load_tables_module()
    table = tmp_path / "p009.zzz"
    table.write_text("synthetic table for GF(9)\n")

    assert "has size 26" in tables.validate_table(table, 9)


def test_table_validator_rejects_wrong_field_and_format(tmp_path):
    tables = _load_tables_module()
    table = tmp_path / "p009.zzz"
    _write_table(table, field_size=25)
    assert "declares GF(25)" in tables.validate_table(table, 9)

    _write_table(table, version=5)
    assert "uses table format 5" in tables.validate_table(table, 9)


def test_companion_ci_generates_real_tables_with_pinned_zcv():
    workflow = (ROOT / ".github" / "workflows" / "companion-packages.yml").read_text()
    block = workflow.split(
        'if [ "${{ matrix.name }}" = "sagelite-meataxe-runtime" ]; then', 1
    )[1].split(
        'if [ "${{ matrix.name }}" = "sagelite-kenzo-runtime" ]; then', 1
    )[0]

    assert "sage-package download meataxe" in block
    assert "SAGELITE_MEATAXE_ZCV" in block
    assert "synthetic table" not in block
