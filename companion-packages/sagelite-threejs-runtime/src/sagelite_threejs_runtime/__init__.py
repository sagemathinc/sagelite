from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def threejs_sage_path() -> str:
    """
    Return the bundled ``threejs-sage`` runtime directory.
    """
    return os.fspath(files(__package__).joinpath("data", "threejs-sage"))


def threejs_min_js_path() -> str:
    """
    Return the bundled ``three.min.js`` path for Sage's required version.
    """
    root = files(__package__).joinpath("data", "threejs-sage")
    version = root.joinpath("version").read_text(encoding="utf-8").strip()
    return os.fspath(root.joinpath(version, "three.min.js"))


__all__ = ["sage_data_path", "threejs_min_js_path", "threejs_sage_path"]
