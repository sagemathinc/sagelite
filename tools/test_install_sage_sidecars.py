from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_installer():
    path = Path(__file__).with_name("install-sage-sidecars.py")
    spec = importlib.util.spec_from_file_location("install_sage_sidecars", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_install_sidecars_copies_sage_source_and_media_assets(tmp_path):
    installer = _load_installer()
    source = tmp_path / "source"
    target = tmp_path / "target"

    copied = [
        "module.pxd",
        "module.pyx",
        "helper.cpp",
        "data/table.json",
        "ext_data/graphs/graph_plot_js.html",
        "ext_data/notebook-ipython/kernel.json.in",
        "ext_data/nodoctest",
        "ext_data/nbconvert/rst_sage.tpl",
        "ext_data/pari/dokchitser/computel.gp.template",
        "ext_data/pari/dokchitser/ex-bsw",
        "ext_data/pari/dokchitser/testall",
        "ext_data/singular/function_field/core.lib",
        "ext_data/doctest/invalid/syntax_error.tachyon",
        "ext_data/valgrind/sage.supp",
        "ext_data/threejs/animation.js",
        "ext_data/threejs/animation.css",
        "ext_data/notebook-ipython/logo.svg",
        "ext_data/notebook-ipython/logo-64x64.png",
        "graphs/generators/example.pickle.xz",
        "interfaces/fricas.spad",
        "interfaces/sage-maxima.lisp",
        "libs/gap/sage.gaprc",
        "misc/notes/bernoulli_mod_p.tex",
        "ext_data/magma/spec",
        "ext_data/mwrank/PRIMES",
        "repl/rich_output/example.gif",
        "repl/rich_output/example.pdf",
        "repl/rich_output/example_jmol.spt.zip",
        "repl/rich_output/example_wavefront_scene.mtl",
        "repl/rich_output/example_wavefront_scene.obj",
        "symbolic/ginac/README.md",
        "README",
    ]
    skipped = [
        "module.py",
        "build.ninja",
        "__pycache__/module.pyc",
    ]

    for relative in copied + skipped:
        path = source / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(relative)

    assert installer.install_sidecars(source, target) == len(copied)

    for relative in copied:
        assert (target / relative).read_text() == relative
    for relative in skipped:
        assert not (target / relative).exists()
