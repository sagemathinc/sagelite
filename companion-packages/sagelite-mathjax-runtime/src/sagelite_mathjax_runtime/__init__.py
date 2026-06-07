from importlib.resources import files
import os


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


__all__ = ["mathjax_dir", "tex_chtml_js_path"]
