import importlib
import importlib.metadata as metadata
import importlib.util
import os
import shutil
import sqlite3
import tempfile


def run_optional_sage_guava_smoke():
    if importlib.util.find_spec("sage.all") is None:
        print("skipping Sage GUAVA smoke: sage.all is not installed")
        return

    from sage.all import GF, codes
    from sage.libs.gap.libgap import libgap

    loaded = libgap.LoadPackage("guava")
    assert str(loaded).lower() == "true", loaded
    program_dirs = libgap.DirectoriesPackagePrograms("guava")
    print("guava_program_dirs=", program_dirs)

    distribution = codes.HammingCode(GF(2), 3).weight_distribution(
        algorithm="leon"
    )
    assert distribution == [1, 0, 0, 7, 7, 0, 0, 1]


module = importlib.import_module(os.environ["SAGELITE_COMPANION_IMPORT_NAME"])
if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-cunningham-tables":
    data_path = module.sage_data_path()
    tables_path = module.cunningham_tables_path()
    sobj_path = module.cunningham_prime_factors_path()
    print("data_path=", data_path)
    print("tables_path=", tables_path)
    print("sobj_path=", sobj_path)
    assert sobj_path.endswith("cunningham_prime_factors.sobj"), sobj_path
    assert os.path.exists(sobj_path)
    assert os.path.getsize(sobj_path) > 0
    assert any(ep.name == "cunningham_tables" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-runtime":
    runtime = importlib.import_module("sagelite_gap_runtime.runtime")
    gap_root = runtime.gap_root()
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root=", gap_root)
    print("gap_root_paths=", gap_root_paths)
    assert os.path.exists(os.path.join(gap_root, "lib", "init.g"))
    assert gap_root in gap_root_paths.split(";")
    os.environ["GAP_ROOT_PATHS"] = gap_root_paths
    import subprocess
    subprocess.run(
        ["gap", "-r", "-q", "--bare", "--nointeract"],
        input='LoadPackage("gapdoc");; NumberSmallGroups(16);; NrTransitiveGroups(5);;\\n',
        text=True,
        check=True,
    )
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-grape":
    runtime = importlib.import_module("sagelite_gap_package_grape.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("grape")
    )
    assert any(ep.name == "grape" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-gapdoc":
    runtime = importlib.import_module("sagelite_gap_package_gapdoc.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("gapdoc")
    )
    assert any(ep.name == "gapdoc" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-atlasrep":
    runtime = importlib.import_module("sagelite_gap_package_atlasrep.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("atlasrep")
    )
    assert any(ep.name == "atlasrep" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-ctbllib":
    runtime = importlib.import_module("sagelite_gap_package_ctbllib.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("ctbllib")
    )
    assert any(ep.name == "ctbllib" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-guava":
    runtime = importlib.import_module("sagelite_gap_package_guava.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("guava")
    )
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("sonata")
    )
    guava_dirs = [
        os.path.join(roots[0], "pkg", name)
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("guava")
    ]
    assert guava_dirs
    assert os.access(os.path.join(guava_dirs[0], "bin", "wtdist"), os.X_OK)
    assert any(ep.name == "guava" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    run_optional_sage_guava_smoke()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-hap":
    runtime = importlib.import_module("sagelite_gap_package_hap.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    for prefix in ("hap", "hapcryst"):
        assert any(
            os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
            for name in os.listdir(os.path.join(roots[0], "pkg"))
            if name.lower().startswith(prefix)
        )
    assert any(ep.name == "hap" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-polenta":
    runtime = importlib.import_module("sagelite_gap_package_polenta.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("polenta")
    )
    assert any(ep.name == "polenta" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-polycyclic":
    runtime = importlib.import_module("sagelite_gap_package_polycyclic.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    for prefix in ("alnuth", "autpgrp", "polycyclic"):
        assert any(
            os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
            for name in os.listdir(os.path.join(roots[0], "pkg"))
            if name.lower().startswith(prefix)
        )
    assert any(ep.name == "polycyclic" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-primgrp":
    runtime = importlib.import_module("sagelite_gap_package_primgrp.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("primgrp")
    )
    assert any(ep.name == "primgrp" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-qpa":
    runtime = importlib.import_module("sagelite_gap_package_qpa.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("qpa")
    )
    assert any(ep.name == "qpa" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-quagroup":
    runtime = importlib.import_module("sagelite_gap_package_quagroup.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("quagroup")
    )
    assert any(ep.name == "quagroup" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-repsn":
    runtime = importlib.import_module("sagelite_gap_package_repsn.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("repsn")
    )
    assert any(ep.name == "repsn" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-smallgrp":
    runtime = importlib.import_module("sagelite_gap_package_smallgrp.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("smallgrp")
    )
    assert any(ep.name == "smallgrp" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-tomlib":
    runtime = importlib.import_module("sagelite_gap_package_tomlib.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("tomlib")
    )
    assert any(ep.name == "tomlib" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-transgrp":
    runtime = importlib.import_module("sagelite_gap_package_transgrp.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    roots = gap_root_paths.split(";")
    assert roots
    assert os.path.exists(os.path.join(roots[0], "pkg"))
    assert any(
        os.path.exists(os.path.join(roots[0], "pkg", name, "PackageInfo.g"))
        for name in os.listdir(os.path.join(roots[0], "pkg"))
        if name.lower().startswith("transgrp")
    )
    assert any(ep.name == "transgrp" for ep in metadata.entry_points(group="sagemath.gap_root_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gfan-runtime":
    runtime = importlib.import_module("sagelite_gfan.runtime")
    gfan = runtime.executable_path("gfan")
    bases = runtime.executable_path("gfan_bases")
    print("gfan=", gfan)
    print("gfan_bases=", bases)
    assert gfan.exists()
    assert bases.exists()
    import shutil
    import subprocess
    assert shutil.which("gfan")
    assert shutil.which("gfan_bases")
    result = subprocess.run(
        ["gfan", "_version"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Gfan version:" in result.stdout
    subprocess.run(
        ["gfan_bases"],
        input="Q[x,y]{x^2-y-1,y^2-x*y-2/3}",
        text=True,
        capture_output=True,
        check=True,
    )
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-giac-runtime":
    runtime = importlib.import_module("sagelite_giac.runtime")
    giac = runtime.giac_command()
    print("giac=", giac)
    assert os.path.exists(giac)
    import shutil
    import subprocess
    assert shutil.which("giac")
    result = subprocess.run(
        ["giac", "--version"],
        text=True,
        capture_output=True,
    )
    assert "giac" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-4ti2-runtime":
    runtime = importlib.import_module("sagelite_four_ti_2.runtime")
    hilbert = runtime.executable_path("hilbert")
    zsolve = runtime.executable_path("zsolve")
    print("hilbert=", hilbert)
    print("zsolve=", zsolve)
    assert os.path.exists(hilbert)
    assert os.path.exists(zsolve)
    import shutil
    import subprocess
    assert shutil.which("hilbert")
    assert shutil.which("zsolve")
    subprocess.run(["hilbert", "-h"], check=True, capture_output=True, text=True)
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-cddlib-runtime":
    runtime = importlib.import_module("sagelite_cddlib.runtime")
    cddexec_gmp = runtime.executable_path("cddexec_gmp")
    cddexec = runtime.executable_path("cddexec")
    print("cddexec_gmp=", cddexec_gmp)
    print("cddexec=", cddexec)
    assert os.path.exists(cddexec_gmp)
    assert os.path.exists(cddexec)
    import shutil
    import subprocess
    assert shutil.which("cddexec_gmp")
    result = subprocess.run(
        ["cddexec_gmp", "--repall"],
        input=(
            "H-representation\n"
            "begin\n"
            " 3 3 rational\n"
            " 1 1 0\n"
            " 1 0 1\n"
            " 1 -1 -1\n"
            "end\n"
        ),
        text=True,
        capture_output=True,
        check=True,
    )
    assert "V-representation" in result.stdout
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-csdp-runtime":
    runtime = importlib.import_module("sagelite_csdp.runtime")
    theta = runtime.executable_path()
    print("theta=", theta)
    assert os.path.exists(theta)
    import shutil
    import subprocess
    assert shutil.which("theta")
    graph = "theta-smoke.graph"
    with open(graph, "w", encoding="utf-8") as handle:
        handle.write(
            "3\n"
            "3\n"
            "1 2\n"
            "2 3\n"
            "1 3\n"
        )
    result = subprocess.run(
        ["theta", graph],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "The Lovasz Theta Number" in result.stdout
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-dvipng-runtime":
    runtime = importlib.import_module("sagelite_dvipng.runtime")
    dvipng = runtime.executable_path()
    print("dvipng=", dvipng)
    assert dvipng.exists()
    import shutil
    import subprocess
    assert shutil.which("dvipng")
    result = subprocess.run(
        ["dvipng", "--version"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "dvipng" in result.stdout.lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-ecl-runtime":
    runtime = importlib.import_module("sagelite_ecl.runtime")
    ecl = runtime.ecl_command()
    ecl_config = runtime.ecl_config_command()
    print("ecl=", ecl)
    print("ecl-config=", ecl_config)
    assert os.path.exists(ecl)
    assert os.path.exists(ecl_config)
    import subprocess
    result = subprocess.run(
        [os.fspath(ecl_config), "--cflags", "--libs"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "-I" in result.stdout
    assert "-lecl" in result.stdout
    result = subprocess.run(
        [os.fspath(ecl), "--version"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "ECL" in result.stdout
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-benzene-runtime":
    runtime = importlib.import_module("sagelite_benzene.runtime")
    benzene = runtime.executable_path()
    print("benzene=", benzene)
    assert benzene.exists()
    import shutil
    import subprocess
    assert shutil.which("benzene")
    result = subprocess.run(
        ["benzene", "-h"],
        text=True,
        capture_output=True,
    )
    assert "benzene" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-buckygen-runtime":
    runtime = importlib.import_module("sagelite_buckygen.runtime")
    buckygen = runtime.executable_path()
    print("buckygen=", buckygen)
    assert buckygen.exists()
    import shutil
    import subprocess
    assert shutil.which("buckygen")
    result = subprocess.run(
        ["buckygen", "-h"],
        text=True,
        capture_output=True,
    )
    assert "buckygen" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-ecm-runtime":
    runtime = importlib.import_module("sagelite_ecm.runtime")
    ecm = runtime.ecm_command()
    print("ecm=", ecm)
    assert os.path.exists(ecm)
    import subprocess
    result = subprocess.run(
        [os.fspath(ecm), "-h"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Usage:" in result.stdout
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-frobby-runtime":
    runtime = importlib.import_module("sagelite_frobby.runtime")
    frobby = runtime.executable_path()
    print("frobby=", frobby)
    assert frobby.exists()
    import shutil
    import subprocess
    assert shutil.which("frobby")
    result = subprocess.run(
        ["frobby", "help"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "frobby" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-fricas-runtime":
    runtime = importlib.import_module("sagelite_fricas.runtime")
    fricas = runtime.executable_path()
    print("fricas=", fricas)
    assert fricas.exists()
    import shutil
    import subprocess
    assert shutil.which("fricas")
    result = subprocess.run(
        ["fricas", "--version"],
        text=True,
        capture_output=True,
    )
    assert "fricas" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-flatter-runtime":
    runtime = importlib.import_module("sagelite_flatter.runtime")
    flatter = runtime.executable_path()
    print("flatter=", flatter)
    assert flatter.exists()
    import shutil
    import subprocess
    assert shutil.which("flatter")
    result = subprocess.run(
        ["flatter", "-h"],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    assert "flatter" in (result.stdout + result.stderr).lower()
    result = subprocess.run(
        ["flatter"],
        input="[[1 0]\n[0 1]]\n",
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stderr
    rows = []
    for line in result.stdout.splitlines():
        entries = line.replace("[", "").replace("]", "").split()
        if len(entries) == 2:
            rows.append(tuple(map(int, entries)))
    assert sorted(rows) == [(0, 1), (1, 0)], result.stdout
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-fplll-data":
    runtime = importlib.import_module("sagelite_fplll_data.runtime")
    strategy = runtime.default_strategy()
    print("default_strategy=", strategy)
    assert strategy.exists()
    assert strategy.name == "default.json"
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-glucose-runtime":
    runtime = importlib.import_module("sagelite_glucose.runtime")
    glucose = runtime.executable_path("glucose")
    syrup = runtime.executable_path("glucose-syrup")
    print("glucose=", glucose)
    print("glucose-syrup=", syrup)
    assert glucose.exists()
    assert syrup.exists()
    import shutil
    import subprocess
    assert shutil.which("glucose")
    assert shutil.which("glucose-syrup")
    result = subprocess.run(
        ["glucose", "--help"],
        text=True,
        capture_output=True,
    )
    assert "usage" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-graphviz-runtime":
    runtime = importlib.import_module("sagelite_graphviz.runtime")
    dot = runtime.executable_path("dot")
    neato = runtime.executable_path("neato")
    twopi = runtime.executable_path("twopi")
    plugins = runtime.plugin_dir()
    print("dot=", dot)
    print("neato=", neato)
    print("twopi=", twopi)
    print("plugin_dir=", plugins)
    assert dot.exists()
    assert neato.exists()
    assert twopi.exists()
    assert any(path.name.startswith("config") for path in plugins.iterdir())
    import shutil
    import subprocess
    assert shutil.which("dot")
    for program in ("dot", "neato", "twopi"):
        result = subprocess.run(
            [program, "-V"],
            text=True,
            capture_output=True,
            check=True,
        )
        assert "graphviz version" in (result.stdout + result.stderr)
    result = subprocess.run(
        ["dot", "-Tdot"],
        input="graph { a -- b }",
        text=True,
        capture_output=True,
        check=True,
    )
    assert "a -- b" in result.stdout
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-imagemagick-runtime":
    runtime = importlib.import_module("sagelite_imagemagick.runtime")
    magick = runtime.executable_path("magick")
    convert = runtime.executable_path("convert")
    print("magick=", magick)
    print("convert=", convert)
    assert magick.exists()
    assert convert.exists()
    import shutil
    import subprocess
    assert shutil.which("magick")
    assert shutil.which("convert")
    result = subprocess.run(
        ["convert", "-version"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "imagemagick" in result.stdout.lower()
    with tempfile.TemporaryDirectory() as directory:
        ppm_path = os.path.join(directory, "input.ppm")
        png_path = os.path.join(directory, "intermediate.png")
        gif_path = os.path.join(directory, "output.gif")
        with open(ppm_path, "wb") as handle:
            handle.write(b"P6\n1 1\n255\n\xff\x00\x00")
        subprocess.run(
            ["convert", ppm_path, png_path],
            text=True,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["convert", png_path, gif_path],
            text=True,
            capture_output=True,
            check=True,
        )
        assert os.path.getsize(gif_path) > 0
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-info-runtime":
    runtime = importlib.import_module("sagelite_info.runtime")
    info = runtime.executable_path()
    info_dir = runtime.info_dir()
    print("info=", info)
    print("info_dir=", info_dir)
    assert info.exists()
    assert (info_dir / "singular.info").exists()
    import shutil
    import subprocess
    assert shutil.which("info")
    env = dict(os.environ)
    env["INFOPATH"] = str(info_dir)
    result = subprocess.run(
        ["info", "--node=groebner", "singular"],
        text=True,
        capture_output=True,
        check=True,
        env=env,
    )
    assert "Up: Functions" in result.stdout
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-kissat-runtime":
    runtime = importlib.import_module("sagelite_kissat.runtime")
    kissat = runtime.executable_path()
    print("kissat=", kissat)
    assert kissat.exists()
    import shutil
    import subprocess
    assert shutil.which("kissat")
    result = subprocess.run(
        ["kissat", "--help"],
        text=True,
        capture_output=True,
    )
    assert "usage" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-latte-runtime":
    runtime = importlib.import_module("sagelite_latte.runtime")
    count = runtime.executable_path("count")
    integrate = runtime.executable_path("integrate")
    print("count=", count)
    print("integrate=", integrate)
    assert count.exists()
    assert integrate.exists()
    import shutil
    import subprocess
    assert shutil.which("count")
    assert shutil.which("integrate")
    result = subprocess.run(
        ["count", "--help"],
        text=True,
        capture_output=True,
    )
    assert "latte" in (result.stdout + result.stderr).lower()
    result = subprocess.run(
        ["integrate", "--help"],
        text=True,
        capture_output=True,
    )
    assert "latte" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-mwrank-runtime":
    runtime = importlib.import_module("sagelite_mwrank.runtime")
    mwrank = runtime.mwrank_command()
    print("mwrank=", mwrank)
    assert os.path.exists(mwrank)
    import shutil
    import subprocess
    assert shutil.which("mwrank")
    result = subprocess.run(
        ["mwrank", "-v0", "-q"],
        input="0 0 0 0 1\n",
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Curve [0,0,0,0,1]" in result.stdout
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-msolve-runtime":
    runtime = importlib.import_module("sagelite_msolve.runtime")
    msolve = runtime.executable_path()
    print("msolve=", msolve)
    assert os.path.exists(msolve)
    import shutil
    import subprocess
    assert shutil.which("msolve")
    result = subprocess.run(
        ["msolve", "-h"],
        text=True,
        capture_output=True,
    )
    assert "msolve" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-lrslib-runtime":
    runtime = importlib.import_module("sagelite_lrslib.runtime")
    lrs = runtime.lrs_command()
    lrsnash = runtime.lrsnash_command()
    print("lrs=", lrs)
    print("lrsnash=", lrsnash)
    assert os.path.exists(lrs)
    assert os.path.exists(lrsnash)
    import shutil
    import subprocess
    assert shutil.which("lrs")
    assert shutil.which("lrsnash")
    result = subprocess.run(
        ["lrs"],
        input="V-representation\nbegin\n 1 1 rational\n 1 \nend\nvolume",
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Volume= 1" in result.stdout or "Volume=1" in result.stdout
    result = subprocess.run(
        ["lrsnash"],
        input="1 1\n \n 0\n \n 0\n",
        text=True,
        capture_output=True,
    )
    assert result.returncode in (0, 1)
    assert result.stdout or result.stderr
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-lcalc-runtime":
    runtime = importlib.import_module("sagelite_lcalc.runtime")
    lcalc = runtime.lcalc_command()
    print("lcalc=", lcalc)
    assert os.path.exists(lcalc)
    import shutil
    import subprocess
    assert shutil.which("lcalc")
    result = subprocess.run(
        ["lcalc", "--help"],
        text=True,
        capture_output=True,
    )
    assert "lcalc" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-meataxe-runtime":
    runtime = importlib.import_module("sagelite_meataxe.runtime")
    meataxe_dir = runtime.meataxe_dir()
    print("meataxe_dir=", meataxe_dir)
    assert os.path.exists(os.path.join(meataxe_dir, "p009.zzz"))
    assert os.path.exists(os.path.join(meataxe_dir, "p025.zzz"))
    assert os.path.exists(os.path.join(meataxe_dir, "p049.zzz"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-kenzo-runtime":
    runtime = importlib.import_module("sagelite_kenzo.runtime")
    fas = runtime.kenzo_fas()
    print("kenzo_fas=", fas)
    assert os.path.exists(fas)
    assert os.path.basename(fas) == "kenzo.fas"
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-maxima-runtime":
    runtime = importlib.import_module("sagelite_maxima.runtime")
    maxima = runtime.maxima_command()
    prefix = runtime.maxima_prefix()
    fas = runtime.maxima_fas()
    ecldir = runtime.ecl_dir()
    asd = os.path.join(ecldir.rstrip(os.sep), "maxima.asd")
    print("maxima=", maxima)
    print("maxima_prefix=", prefix)
    print("maxima_fas=", fas)
    print("ecldir=", ecldir)
    print("maxima_asd=", asd)
    assert os.path.isdir(os.path.join(prefix, "share", "maxima"))
    assert os.path.exists(fas)
    assert os.path.exists(asd)
    assert "prebuilt-system" in open(asd, encoding="utf-8").read()
    assert os.path.exists(os.path.join(ecldir, "sockets.fas"))
    if os.path.exists(maxima):
        import subprocess
        result = subprocess.run(
            [maxima, "--very-quiet", "--batch-string=2+3;"],
            text=True,
            capture_output=True,
            check=True,
        )
        assert "5" in result.stdout
    ecl = shutil.which("ecl")
    if ecl:
        import subprocess
        env = os.environ.copy()
        env["ECLDIR"] = ecldir
        # Do not prepend the copied runtime library here.  This
        # workflow explicitly validates the non-publishable
        # system-ECL build path used by local probes, where
        # sage.libs.ecl is already bound to the system libecl before
        # sagelite can adjust LD_LIBRARY_PATH.
        subprocess.run(
            [ecl, "-norc", "-eval", "(require 'maxima)", "-eval", "(quit)"],
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-nauty-runtime":
    runtime = importlib.import_module("sagelite_nauty.runtime")
    geng = runtime.executable_path("geng")
    genposetg = runtime.executable_path("genposetg")
    print("geng=", geng)
    print("genposetg=", genposetg)
    assert geng.exists()
    assert genposetg.exists()
    import shutil
    import subprocess
    assert shutil.which("geng")
    assert shutil.which("genposetg")
    subprocess.run(["geng", "-q", "3"], check=True, capture_output=True, text=True)
    subprocess.run(["genposetg", "-q", "3"], check=True, capture_output=True, text=True)
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-palp-runtime":
    runtime = importlib.import_module("sagelite_palp.runtime")
    poly = runtime.executable_path("poly.x")
    nef = runtime.executable_path("nef.x")
    print("poly.x=", poly)
    print("nef.x=", nef)
    assert poly.exists()
    assert nef.exists()
    import shutil
    import subprocess
    assert shutil.which("poly.x")
    assert shutil.which("nef.x")
    subprocess.run(["poly.x", "-h"], check=True, capture_output=True, text=True)
    subprocess.run(["nef.x", "-h"], check=True, capture_output=True, text=True)
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-planarity-runtime":
    runtime = importlib.import_module("sagelite_planarity.runtime")
    planarity = runtime.executable_path()
    print("planarity=", planarity)
    assert planarity.exists()
    import shutil
    import subprocess
    assert shutil.which("planarity")
    result = subprocess.run(
        ["planarity", "-h"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "Edge Addition Planarity Suite" in result.stdout
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-pdf2svg-runtime":
    runtime = importlib.import_module("sagelite_pdf2svg.runtime")
    pdf2svg = runtime.executable_path()
    print("pdf2svg=", pdf2svg)
    assert pdf2svg.exists()
    import shutil
    import subprocess
    assert shutil.which("pdf2svg")
    result = subprocess.run(
        ["pdf2svg"],
        text=True,
        capture_output=True,
    )
    assert result.returncode != 0
    assert "Usage:" in result.stdout or "Usage:" in result.stderr
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-plantri-runtime":
    runtime = importlib.import_module("sagelite_plantri.runtime")
    plantri = runtime.executable_path()
    print("plantri=", plantri)
    assert plantri.exists()
    import shutil
    import subprocess
    assert shutil.which("plantri")
    result = subprocess.run(
        ["plantri", "-help"],
        text=True,
        capture_output=True,
    )
    assert "plantri" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-poppler-runtime":
    runtime = importlib.import_module("sagelite_poppler.runtime")
    pdftocairo = runtime.executable_path()
    print("pdftocairo=", pdftocairo)
    assert pdftocairo.exists()
    import shutil
    import subprocess
    assert shutil.which("pdftocairo")
    result = subprocess.run(
        ["pdftocairo", "-h"],
        text=True,
        capture_output=True,
    )
    assert "pdftocairo" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-qepcad-runtime":
    runtime = importlib.import_module("sagelite_qepcad.runtime")
    root = runtime.root_dir()
    qepcad = runtime.executable_path()
    help_path = runtime.help_path()
    default_qepcadrc = runtime.default_qepcadrc_path()
    print("qepcad_root=", root)
    print("qepcad=", qepcad)
    print("qepcad_help=", help_path)
    print("default_qepcadrc=", default_qepcadrc)
    assert qepcad.exists()
    assert help_path.exists()
    assert default_qepcadrc.exists()
    import subprocess
    qepcad_env = os.environ.copy()
    qepcad_env["qe"] = os.fspath(root)
    result = subprocess.run(
        [os.fspath(qepcad)],
        input="",
        text=True,
        capture_output=True,
        timeout=30,
        env=qepcad_env,
    )
    output = result.stdout + result.stderr
    assert "Quantifier Elimination" in output
    assert "Enter an informal description" in output
    assert "bad_alloc" not in output
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-rubiks-runtime":
    runtime = importlib.import_module("sagelite_rubiks.runtime")
    cu2 = runtime.executable_path("cu2")
    size222 = runtime.executable_path("size222")
    print("cu2=", cu2)
    print("size222=", size222)
    assert cu2.exists()
    assert size222.exists()
    import shutil
    assert shutil.which("cu2")
    assert shutil.which("size222")
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-pari-data":
    runtime = importlib.import_module("sagelite_pari_data.runtime")
    data_dir = runtime.pari_data_dir()
    print("pari_data_dir=", data_dir)
    assert os.path.exists(os.path.join(data_dir, "elldata", "ell2.gz"))
    assert os.path.exists(os.path.join(data_dir, "galdata", "COS8_49_45"))
    assert os.path.exists(os.path.join(data_dir, "galpol", "README"))
    assert os.path.exists(os.path.join(data_dir, "seadata"))
    assert any(os.scandir(os.path.join(data_dir, "nftables")))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-singular-runtime":
    runtime = importlib.import_module("sagelite_singular_runtime.runtime")
    root_dir = runtime.singular_root_dir()
    default_dir = runtime.singular_default_dir()
    print("singular_root_dir=", root_dir)
    print("singular_default_dir=", default_dir)
    assert os.path.exists(os.path.join(root_dir, "share", "singular", "LIB", "standard.lib"))
    assert os.path.exists(os.path.join(default_dir, "LIB", "freegb.lib"))
    assert os.path.exists(os.path.join(default_dir, "factory", "gftables", "64"))
    assert any(
        "MOD/freealgebra.so" in os.path.join(path, filename)
        for path, _, filenames in os.walk(root_dir)
        for filename in filenames
    )
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-gap-package-design":
    runtime = importlib.import_module("sagelite_gap_package_design.runtime")
    gap_root_paths = runtime.gap_root_paths()
    print("gap_root_paths=", gap_root_paths)
    assert gap_root_paths
    pkg_dir = os.path.join(gap_root_paths, "pkg")
    assert os.path.exists(pkg_dir)
    assert any(name.lower().startswith("design") for name in os.listdir(pkg_dir))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-d3js-runtime":
    data_path = module.sage_data_path()
    d3js_path = module.d3js_path()
    d3_min_js = module.d3_min_js_path()
    print("data_path=", data_path)
    print("d3js_path=", d3js_path)
    print("d3_min_js=", d3_min_js)
    assert d3_min_js.endswith("d3.min.js"), d3_min_js
    assert os.path.exists(d3_min_js)
    assert os.path.getsize(d3_min_js) > 0
    assert any(ep.name == "d3js" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-jmol-runtime":
    data_path = module.sage_data_path()
    jmol_path = module.jmol_path()
    jmol_data_jar = module.jmol_data_jar_path()
    print("data_path=", data_path)
    print("jmol_path=", jmol_path)
    print("jmol_data_jar=", jmol_data_jar)
    assert jmol_data_jar.endswith("JmolData.jar"), jmol_data_jar
    assert os.path.exists(jmol_data_jar)
    assert os.path.getsize(jmol_data_jar) > 0
    assert any(ep.name == "jmol" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-sympow-runtime":
    runtime = importlib.import_module("sagelite_sympow.runtime")
    sympow = runtime.sympow_command()
    print("sympow=", sympow)
    assert os.path.exists(sympow)
    import shutil
    import subprocess
    assert shutil.which("sympow")
    result = subprocess.run(
        ["sympow", "-help"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "sympow" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-tachyon-runtime":
    runtime = importlib.import_module("sagelite_tachyon.runtime")
    tachyon = runtime.executable_path()
    print("tachyon=", tachyon)
    assert tachyon.exists()
    import shutil
    import subprocess
    assert shutil.which("tachyon")
    result = subprocess.run(
        ["tachyon", "-help"],
        text=True,
        capture_output=True,
    )
    assert "tachyon" in (result.stdout + result.stderr).lower()
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-tides-runtime":
    runtime = importlib.import_module("sagelite_tides.runtime")
    include_dir = runtime.include_dir()
    library_path = runtime.library_path()
    print("include_dir=", include_dir)
    print("library_path=", library_path)
    assert include_dir.exists()
    assert library_path.exists()
    assert (include_dir / "minc_tides.h").exists()
    assert library_path.name == "libTIDES.a"
    assert library_path.stat().st_size > 0
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-sirocco-runtime":
    runtime = importlib.import_module("sagelite_sirocco.runtime")
    include_dir = runtime.include_dir()
    library_path = runtime.library_path()
    print("include_dir=", include_dir)
    print("library_path=", library_path)
    assert include_dir.exists()
    assert library_path.exists()
    assert (include_dir / "sirocco.h").exists()
    assert library_path.name.startswith("libsirocco")
    assert library_path.stat().st_size > 0
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-topcom-runtime":
    runtime = importlib.import_module("sagelite_topcom.runtime")
    placing = runtime.executable_path("points2placingtriang")
    all_fine = runtime.executable_path("points2allfinetriangs")
    print("points2placingtriang=", placing)
    print("points2allfinetriangs=", all_fine)
    assert os.path.exists(placing)
    assert os.path.exists(all_fine)
    import shutil
    import subprocess
    assert shutil.which("points2placingtriang")
    result = subprocess.run(
        ["points2placingtriang"],
        input="[[0,0,0,1],[-2,0,0,1],[0,-2,0,1],[-2,-2,0,1],[0,0,-2,1]]X\nX\n",
        text=True,
        capture_output=True,
        check=True,
    )
    assert "{{0,1,2,4},{1,2,3,4}}" in result.stdout
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-graphs":
    data_path = module.sage_data_path()
    graphs_path = module.graphs_data_path()
    db_path = module.graphs_db_path()
    print("data_path=", data_path)
    print("graphs_path=", graphs_path)
    print("db_path=", db_path)
    assert db_path.endswith("graphs.db"), db_path
    assert os.path.exists(os.path.join(graphs_path, "brouwer_srg_database.json"))
    assert os.path.exists(os.path.join(graphs_path, "isgci_sage.xml"))
    assert os.path.exists(os.path.join(graphs_path, "smallgraphs.txt"))
    assert any(ep.name == "graphs" for ep in metadata.entry_points(group="sagemath.data_paths"))
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    assert cur.execute("select count(*) from graph_data").fetchone()[0] > 0
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-ellcurves":
    data_path = module.sage_data_path()
    ellcurves_path = module.ellcurves_data_path()
    rank0_path = module.rank_file_path(0)
    rank1_path = module.rank_file_path(1)
    print("data_path=", data_path)
    print("ellcurves_path=", ellcurves_path)
    print("rank0_path=", rank0_path)
    assert rank0_path.endswith("rank0"), rank0_path
    assert os.path.exists(rank0_path)
    assert os.path.exists(rank1_path)
    assert os.path.getsize(rank0_path) > 0
    assert os.path.getsize(rank1_path) > 0
    assert any(ep.name == "ellcurves" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-jones-numfield":
    data_path = module.sage_data_path()
    jones_path = module.jones_data_path()
    sobj_path = module.jones_sobj_path()
    print("data_path=", data_path)
    print("jones_path=", jones_path)
    print("sobj_path=", sobj_path)
    assert sobj_path.endswith("jones.sobj"), sobj_path
    assert os.path.exists(sobj_path)
    assert os.path.getsize(sobj_path) > 0
    assert any(ep.name == "jones" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-kohel":
    data_path = module.sage_data_path()
    kohel_path = module.kohel_data_path()
    cls_path = module.modular_polynomial_path("Cls", 29)
    atk_path = module.modular_polynomial_path("Atk", 2)
    hilbert_path = module.hilbert_class_polynomial_path(-23)
    print("data_path=", data_path)
    print("kohel_path=", kohel_path)
    print("cls_path=", cls_path)
    assert os.path.exists(cls_path)
    assert os.path.exists(atk_path)
    assert os.path.exists(hilbert_path)
    assert os.path.getsize(cls_path) > 0
    assert any(ep.name == "kohel" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-polytopes":
    data_path = module.sage_data_path()
    polytopes_path = module.reflexive_polytopes_path()
    print("data_path=", data_path)
    print("polytopes_path=", polytopes_path)
    assert os.path.isdir(os.path.join(polytopes_path, "Full2d"))
    assert os.path.isdir(os.path.join(polytopes_path, "Full3d"))
    assert os.path.exists(os.path.join(polytopes_path, "reflexive_polytopes_2d"))
    assert os.path.exists(os.path.join(polytopes_path, "reflexive_polytopes_3d"))
    assert any(ep.name == "reflexive_polytopes" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-polytopes-4d":
    data_path = module.sage_data_path()
    polytopes_path = module.reflexive_polytopes_path()
    hodge4d_path = module.hodge4d_path()
    print("data_path=", data_path)
    print("polytopes_path=", polytopes_path)
    print("hodge4d_path=", hodge4d_path)
    assert os.path.isdir(hodge4d_path)
    assert any(os.scandir(hodge4d_path))
    assert any(ep.name == "reflexive_polytopes" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-sloane":
    data_path = module.sage_data_path()
    sloane_path = module.sloane_data_path()
    oeis_path = module.sloane_oeis_path()
    names_path = module.sloane_names_path()
    print("data_path=", data_path)
    print("sloane_path=", sloane_path)
    print("oeis_path=", oeis_path)
    print("names_path=", names_path)
    assert oeis_path.endswith("sloane-oeis.bz2"), oeis_path
    assert names_path.endswith("sloane-names.bz2"), names_path
    assert os.path.exists(oeis_path)
    assert os.path.exists(names_path)
    assert os.path.getsize(oeis_path) > 0
    assert os.path.getsize(names_path) > 0
    assert any(ep.name == "sloane" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-mutation-class":
    data_path = module.sage_data_path()
    quiver_path = module.cluster_algebra_quiver_data_path()
    rank2_path = module.mutation_classes_path(2)
    print("data_path=", data_path)
    print("quiver_path=", quiver_path)
    print("rank2_path=", rank2_path)
    assert rank2_path.endswith("mutation_classes_2.dig6"), rank2_path
    assert os.path.exists(rank2_path)
    assert os.path.getsize(rank2_path) > 0
    assert any(ep.name == "cluster_algebra_quiver" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-symbolic-data":
    data_path = module.sage_data_path()
    symbolic_path = module.symbolic_data_path()
    resources_path = module.xml_resources_path()
    print("data_path=", data_path)
    print("symbolic_path=", symbolic_path)
    print("resources_path=", resources_path)
    assert os.path.isdir(os.path.join(resources_path, "INTPS"))
    assert os.path.isdir(os.path.join(resources_path, "GenPS"))
    assert os.path.exists(os.path.join(resources_path, "INTPS", "Katsura_3.xml"))
    assert os.path.exists(os.path.join(resources_path, "GenPS", "Curves.curve3_20.xml"))
    assert any(ep.name == "symbolic_data" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-odlyzko-zeta":
    data_path = module.sage_data_path()
    odlyzko_path = module.odlyzko_data_path()
    sobj_path = module.zeros_sobj_path()
    print("data_path=", data_path)
    print("odlyzko_path=", odlyzko_path)
    print("sobj_path=", sobj_path)
    assert sobj_path.endswith("zeros.sobj"), sobj_path
    assert os.path.exists(sobj_path)
    assert os.path.getsize(sobj_path) > 0
    assert any(ep.name == "odlyzko" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-stein-watkins-mini":
    data_path = module.sage_data_path()
    stein_watkins_path = module.stein_watkins_data_path()
    all0_path = module.all_data_path(0)
    all1_path = module.all_data_path(1)
    prime0_path = module.prime_data_path(0)
    print("data_path=", data_path)
    print("stein_watkins_path=", stein_watkins_path)
    print("all0_path=", all0_path)
    assert os.path.exists(all0_path)
    assert os.path.exists(all1_path)
    assert os.path.exists(prime0_path)
    assert os.path.getsize(all0_path) > 0
    assert any(ep.name == "stein_watkins" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-stein-watkins":
    data_path = module.sage_data_path()
    stein_watkins_path = module.stein_watkins_data_path()
    all0_path = module.all_data_path(0)
    prime0_path = module.prime_data_path(0)
    print("data_path=", data_path)
    print("stein_watkins_path=", stein_watkins_path)
    print("all0_path=", all0_path)
    print("prime0_path=", prime0_path)
    assert os.path.exists(all0_path)
    assert os.path.exists(prime0_path)
    assert os.path.getsize(all0_path) > 0
    assert any(ep.name == "stein_watkins" for ep in metadata.entry_points(group="sagemath.data_paths"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-cremona-mini":
    data_path = module.sage_data_path()
    db_path = module.cremona_mini_path()
    print("data_path=", data_path)
    print("db_path=", db_path)
    assert db_path.endswith("cremona_mini.db"), db_path
    assert any(ep.name == "cremona_mini" for ep in metadata.entry_points(group="sagemath.data_paths"))
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    assert cur.execute("select count(*) from t_class").fetchone()[0] > 0
    assert cur.execute("select count(*) from t_curve").fetchone()[0] > 0
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-database-cremona-ellcurve":
    data_path = module.sage_data_path()
    db_path = module.cremona_ellcurve_path()
    print("data_path=", data_path)
    print("db_path=", db_path)
    assert db_path.endswith("cremona.db"), db_path
    assert any(ep.name == "cremona" for ep in metadata.entry_points(group="sagemath.data_paths"))
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    assert cur.execute("select count(*) from t_class").fetchone()[0] > 0
    assert cur.execute("select count(*) from t_curve").fetchone()[0] > 0
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-mathjax-runtime":
    assert any(ep.name == "mathjax" for ep in metadata.entry_points(group="sagemath.data_paths"))
    mathjax_dir = module.mathjax_dir()
    tex_chtml = module.tex_chtml_js_path()
    print("mathjax_dir=", mathjax_dir)
    print("tex_chtml=", tex_chtml)
    assert mathjax_dir.endswith(os.path.join("data", "mathjax")), mathjax_dir
    assert tex_chtml.endswith(os.path.join("data", "mathjax", "tex-chtml.js")), tex_chtml
    assert os.path.exists(tex_chtml)
    assert os.path.exists(os.path.join(mathjax_dir, "loader.js"))
    raise SystemExit(0)

if os.environ["SAGELITE_COMPANION_NAME"] == "sagelite-threejs-runtime":
    assert any(ep.name == "threejs_sage" for ep in metadata.entry_points(group="sagemath.data_paths"))
    threejs_dir = module.threejs_sage_path()
    threejs_min = module.threejs_min_js_path()
    print("threejs_dir=", threejs_dir)
    print("threejs_min=", threejs_min)
    assert threejs_dir.endswith(os.path.join("data", "threejs-sage")), threejs_dir
    assert threejs_min.endswith("three.min.js"), threejs_min
    assert os.path.exists(threejs_min)
    raise SystemExit(0)

raise AssertionError("unhandled companion package")
