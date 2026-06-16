from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _load_indexer():
    path = ROOT / "tools" / "build-sagelite-wheel-index.py"
    spec = importlib.util.spec_from_file_location("build_sagelite_wheel_index", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_build_index_groups_wheels_by_normalized_project_name(tmp_path):
    indexer = _load_indexer()
    wheels = tmp_path / "wheels"
    simple = tmp_path / "simple"
    wheels.mkdir()

    core = wheels / "sagelite-10.9.post2-cp314-cp314-manylinux_2_28_x86_64.whl"
    companion = (
        wheels
        / "sagelite_gap_runtime-10.9.post2-py3-none-manylinux_2_28_x86_64.whl"
    )
    core.write_bytes(b"core wheel")
    companion.write_bytes(b"gap wheel")

    projects = indexer.build_index(wheels, simple)

    assert sorted(projects) == ["sagelite", "sagelite-gap-runtime"]
    assert '<a href="sagelite/">' in (simple / "index.html").read_text()

    project_page = (simple / "sagelite-gap-runtime" / "index.html").read_text()
    assert "sagelite_gap_runtime-10.9.post2-py3-none" in project_page
    assert "../../wheels/sagelite_gap_runtime-" in project_page
    assert "#sha256=" in project_page


def test_build_index_can_link_to_external_wheel_base_url(tmp_path):
    indexer = _load_indexer()
    wheels = tmp_path / "wheels"
    simple = tmp_path / "simple"
    wheels.mkdir()

    wheel = wheels / "sagelite_cunningham_tables-10.9-py3-none-any.whl"
    wheel.write_bytes(b"cunningham")

    indexer.build_index(
        wheels,
        simple,
        "https://pub.example.test/sagelite/wheels/",
    )

    project_page = (simple / "sagelite-cunningham-tables" / "index.html").read_text()
    assert (
        "https://pub.example.test/sagelite/wheels/"
        "sagelite_cunningham_tables-10.9-py3-none-any.whl#sha256="
        in project_page
    )
    assert "../../wheels/" not in project_page


def test_build_index_removes_stale_output(tmp_path):
    indexer = _load_indexer()
    wheels = tmp_path / "wheels"
    simple = tmp_path / "simple"
    wheels.mkdir()
    (simple / "stale-project").mkdir(parents=True)
    (simple / "stale-project" / "index.html").write_text("stale", encoding="utf-8")

    wheel = wheels / "sagelite-10.9.post2-cp312-cp312-linux_x86_64.whl"
    wheel.write_bytes(b"core")

    indexer.build_index(wheels, simple)

    assert not (simple / "stale-project").exists()
    assert (simple / "sagelite" / "index.html").exists()


def test_build_index_rejects_empty_wheel_directory(tmp_path):
    indexer = _load_indexer()
    wheels = tmp_path / "wheels"
    wheels.mkdir()

    with pytest.raises(SystemExit, match="no wheels found"):
        indexer.build_index(wheels, tmp_path / "simple")
