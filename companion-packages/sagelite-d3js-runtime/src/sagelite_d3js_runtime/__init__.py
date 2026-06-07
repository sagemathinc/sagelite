from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def d3js_path() -> str:
    """
    Return the bundled D3.js runtime directory.
    """
    return os.fspath(files(__package__).joinpath("data", "d3js"))


def d3_min_js_path() -> str:
    """
    Return the bundled ``d3.min.js`` path.
    """
    return os.fspath(files(__package__).joinpath("data", "d3js", "d3.min.js"))


__all__ = ["d3_min_js_path", "d3js_path", "sage_data_path"]
