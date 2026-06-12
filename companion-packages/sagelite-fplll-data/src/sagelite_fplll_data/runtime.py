from __future__ import annotations

from pathlib import Path


def strategies_dir() -> Path:
    return Path(__file__).resolve().parent / "data" / "strategies"


def default_strategy() -> Path:
    return strategies_dir() / "default.json"
