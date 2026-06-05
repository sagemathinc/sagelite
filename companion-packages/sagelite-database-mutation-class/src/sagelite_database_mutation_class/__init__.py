from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def cluster_algebra_quiver_data_path() -> str:
    """
    Return the bundled cluster algebra quiver database directory.
    """
    return os.fspath(files(__package__).joinpath("data", "cluster_algebra_quiver"))


def mutation_classes_path(n: int) -> str:
    """
    Return the bundled mutation class data file for rank ``n``.
    """
    return os.fspath(
        files(__package__).joinpath(
            "data", "cluster_algebra_quiver", f"mutation_classes_{n}.dig6"
        )
    )


__all__ = [
    "cluster_algebra_quiver_data_path",
    "mutation_classes_path",
    "sage_data_path",
]
