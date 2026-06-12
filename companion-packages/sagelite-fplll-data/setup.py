from __future__ import annotations

import os
import shutil
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


def _candidate_strategy_dirs() -> list[Path]:
    dirs = []
    for variable in ("SAGELITE_FPLLL_STRATEGIES_DIR", "FPLLL_STRATEGIES_DIR"):
        if os.environ.get(variable):
            dirs.append(Path(os.environ[variable]))
    if os.environ.get("SAGE_LOCAL"):
        dirs.append(Path(os.environ["SAGE_LOCAL"]) / "share" / "fplll" / "strategies")
    dirs.extend(
        [
            Path("/usr/share/fplll/strategies"),
            Path("/usr/local/share/fplll/strategies"),
        ]
    )
    return dirs


def _find_strategy_dir() -> Path:
    for directory in _candidate_strategy_dirs():
        if (directory / "default.json").is_file():
            return directory.resolve()
    searched = "\n  ".join(os.fspath(path) for path in _candidate_strategy_dirs())
    raise RuntimeError(
        "could not find FPLLL strategy data containing default.json. "
        "Set SAGELITE_FPLLL_STRATEGIES_DIR to the Sage-built strategies directory.\n"
        f"Searched:\n  {searched}"
    )


class build_py(_build_py):
    def run(self):
        source = _find_strategy_dir()
        target = Path(self.build_lib) / "sagelite_fplll_data" / "data" / "strategies"
        shutil.rmtree(target, ignore_errors=True)
        target.mkdir(parents=True, exist_ok=True)

        for strategy in source.glob("*.json"):
            shutil.copy2(strategy, target / strategy.name)

        super().run()


setup(cmdclass={"build_py": build_py})
