import os
from importlib.resources import files


def _package_dirs(root, prefix: str):
    pkg = root.joinpath("pkg")
    if not pkg.is_dir():
        return []
    return [
        path
        for path in pkg.iterdir()
        if path.name.lower().startswith(prefix)
        and path.joinpath("PackageInfo.g").is_file()
    ]


def _has_executable_wtdist(package_dir) -> bool:
    wtdist = package_dir.joinpath("bin", "wtdist")
    return wtdist.is_file() and os.access(os.fspath(wtdist), os.X_OK)


def gap_root_paths() -> str:
    """
    Return the GAP package root contributed by this companion wheel.
    """
    root = files(__package__).joinpath("data", "gaproot")
    guava_dirs = _package_dirs(root, "guava")
    sonata_dirs = _package_dirs(root, "sonata")
    if guava_dirs and sonata_dirs and any(
        _has_executable_wtdist(package_dir) for package_dir in guava_dirs
    ):
        return os.fspath(root)
    return ""


__all__ = ["gap_root_paths"]
