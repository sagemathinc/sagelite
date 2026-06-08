from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def mathjax_dir() -> str:
    """
    Return the bundled MathJax runtime directory.
    """
    return os.fspath(files(__package__).joinpath("data", "mathjax"))


def tex_chtml_js_path() -> str:
    """
    Return the bundled ``tex-chtml.js`` path.
    """
    return os.fspath(files(__package__).joinpath("data", "mathjax", "tex-chtml.js"))


__all__ = ["mathjax_dir", "sage_data_path", "tex_chtml_js_path"]
