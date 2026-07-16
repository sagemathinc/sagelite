from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:  # pragma: no cover - wheel is a build requirement
    _bdist_wheel = None


sys.path.insert(0, os.fspath(Path(__file__).parent / "src"))
from sagelite_meataxe.tables import FIELD_SIZES, table_errors, table_name  # noqa: E402


def _has_required_tables(directory: Path) -> bool:
    return not table_errors(directory)


def _candidate_table_dirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_MEATAXE_DIR", "MTXLIB"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_SHARE"):
        dirs.append(Path(os.environ["SAGE_SHARE"]) / "meataxe")
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "meataxe")
    dirs.extend([Path("/usr/share/meataxe"), Path("/usr/local/share/meataxe")])
    return dirs


def _candidate_zcv_commands() -> list[Path]:
    commands = []
    for variable in ("SAGELITE_MEATAXE_ZCV", "ZCV"):
        if os.environ.get(variable):
            commands.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        commands.append(Path(os.environ["SAGE_LOCAL"]) / "bin" / "zcv")
    path_zcv = shutil.which("zcv")
    if path_zcv:
        commands.append(Path(path_zcv))
    return commands


def _find_table_dir() -> Path | None:
    for directory in _candidate_table_dirs():
        if directory.is_dir() and _has_required_tables(directory):
            return directory.resolve()
    return None


def _find_zcv() -> Path | None:
    for command in _candidate_zcv_commands():
        if command.is_file() and os.access(command, os.X_OK):
            return command.resolve()
    return None


def _generate_tables(target: Path, zcv: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        input_file = Path(tmp) / "empty-matrix.txt"
        for field_size in FIELD_SIZES:
            input_file.write_text(f"matrix field={field_size} rows=0 cols=0\n")
            subprocess.run(
                [os.fspath(zcv), os.fspath(input_file), os.devnull],
                cwd=target,
                check=True,
            )


class build_py(_build_py):
    def run(self):
        target = Path(self.build_lib) / "sagelite_meataxe" / "data" / "meataxe"
        shutil.rmtree(target, ignore_errors=True)

        source = _find_table_dir()
        if source is not None:
            shutil.copytree(source, target)
        else:
            zcv = _find_zcv()
            if zcv is None:
                searched_dirs = "\n  ".join(
                    os.fspath(path) for path in _candidate_table_dirs()
                )
                searched_zcv = "\n  ".join(
                    os.fspath(path) for path in _candidate_zcv_commands()
                )
                raise RuntimeError(
                    "could not find MeatAxe multiplication tables or zcv. "
                    "Set SAGELITE_MEATAXE_DIR to a generated table directory "
                    "or SAGELITE_MEATAXE_ZCV to the Sage-built zcv executable.\n"
                    f"Searched table directories:\n  {searched_dirs}\n"
                    f"Searched zcv commands:\n  {searched_zcv}"
                )
            _generate_tables(target, zcv)

        if not _has_required_tables(target):
            errors = table_errors(target)
            raise RuntimeError(
                "MeatAxe table directory is invalid: "
                + "; ".join(errors[:5])
                + (" ..." if len(errors) > 5 else "")
            )

        super().run()


cmdclass = {"build_py": build_py}

if _bdist_wheel is not None:

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            super().finalize_options()
            plat_name = os.environ.get("SAGELITE_MEATAXE_RUNTIME_PLAT_NAME")
            if plat_name:
                self.root_is_pure = True
                self.python_tag = "py3"
                self.plat_name = plat_name
                self.plat_name_supplied = True
            else:
                self.root_is_pure = False

    cmdclass["bdist_wheel"] = bdist_wheel


setup(cmdclass=cmdclass)
