from __future__ import annotations

import gzip
import os
import pickle
import re
import shutil
import zlib
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.sdist import sdist as _sdist


EXTRA_FACTORS = [
    3,
    5,
    17,
    257,
    641,
    65537,
    274177,
    319489,
    974849,
    2424833,
    6700417,
    45592577,
    6487031809,
    67280421310721,
    1238926361552897,
    59649589127497217,
    167988556341760475137,
    5704689200685129054721,
    3560841906445833920513,
    4659775785220018543264560743076778192897,
    7455602825647884208337395736200454918783366342657,
    93461639715357977769163558199606896584051237541638188580280321,
    741640062627530801524787141901937474059940781097519023905821316144415759504705008092818711693940737,
    130439874405488189727484768796509903946608530841611892186895295776832416251471863574140227977573104895898783928842923844831149032913798729088601617946094119449010595906710130531906171018354491609619193912488538116080712299672322806217820753127014424577,
    173462447179147555430258970864309778377421844723664084649347019061363579192879108857591038330408837177983810868451546421940712978306134189864280826014542758708589243873685563973118948869399158545506611147420216132557017260564139394366945793220968665108959685482705388072645828554151936401912464931182546092879815733057795573358504982279280090942872567591518912118622751714319229788100979251036035496917279912663527358783236647193154777091427745377038294584918917590325110939381322486044298573971650711059244462177542540706913047034664643603491382441723306598834177,
]


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _candidate_main_gz_files() -> list[Path]:
    files = []
    if os.environ.get("SAGELITE_CUNNINGHAM_MAIN_GZ"):
        files.append(Path(os.environ["SAGELITE_CUNNINGHAM_MAIN_GZ"]))
    files.append(Path(__file__).resolve().parent / "src" / "sagelite_cunningham_tables" / "_main.gz")
    files.append(_project_root() / "build" / "pkgs" / "cunningham_tables" / "main.gz")
    return files


def _candidate_precomputed_sobj_files() -> list[Path]:
    files = []
    if os.environ.get("SAGELITE_CUNNINGHAM_FACTORS_SOBJ"):
        files.append(Path(os.environ["SAGELITE_CUNNINGHAM_FACTORS_SOBJ"]))
    files.append(
        Path(__file__).resolve().parent
        / "src"
        / "sagelite_cunningham_tables"
        / "data"
        / "cunningham_tables"
        / "cunningham_prime_factors.sobj"
    )
    files.append(
        _project_root()
        / "build"
        / "pkgs"
        / "cunningham_tables"
        / "cunningham_prime_factors.sobj"
    )
    return files


def _find_precomputed_sobj() -> Path | None:
    for path in _candidate_precomputed_sobj_files():
        if path.is_file():
            return path.resolve()
    return None


def _find_main_gz() -> Path:
    for path in _candidate_main_gz_files():
        if path.is_file():
            return path.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_main_gz_files())
    raise RuntimeError(
        "could not find Cunningham main.gz. Set SAGELITE_CUNNINGHAM_MAIN_GZ.\n"
        f"Searched:\n  {searched}"
    )


def _parse_factors(main_gz: Path) -> list[int]:
    factors: set[int] = set(EXTRA_FACTORS)
    with gzip.open(main_gz, "rt", encoding="ascii") as handle:
        for line in handle:
            _, _, factorization = line.partition(") ")
            factors.update(int(value) for value in re.findall(r"[ .]([0-9]+)", factorization))
    return sorted(factors)


def _write_sobj(path: Path, factors: list[int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(zlib.compress(pickle.dumps(factors, protocol=2)))


def _copy_or_build_sobj(target: Path) -> None:
    precomputed_sobj = _find_precomputed_sobj()
    target.parent.mkdir(parents=True, exist_ok=True)
    if precomputed_sobj is not None:
        shutil.copy2(precomputed_sobj, target)
        return
    _write_sobj(target, _parse_factors(_find_main_gz()))


class build_py(_build_py):
    def run(self):
        super().run()

        target = (
            Path(self.build_lib)
            / "sagelite_cunningham_tables"
            / "data"
            / "cunningham_tables"
        )
        shutil.rmtree(target, ignore_errors=True)
        _copy_or_build_sobj(target / "cunningham_prime_factors.sobj")


class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        precomputed_sobj = _find_precomputed_sobj()
        if precomputed_sobj is not None:
            target = (
                Path(base_dir)
                / "src"
                / "sagelite_cunningham_tables"
                / "data"
                / "cunningham_tables"
                / "cunningham_prime_factors.sobj"
            )
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(precomputed_sobj, target)
            return

        main_gz_target = (
            Path(base_dir) / "src" / "sagelite_cunningham_tables" / "_main.gz"
        )
        main_gz_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(_find_main_gz(), main_gz_target)


setup(cmdclass={"build_py": build_py, "sdist": sdist})
