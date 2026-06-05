from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def kohel_data_path() -> str:
    """
    Return the bundled Kohel database directory.
    """
    return os.fspath(files(__package__).joinpath("data", "kohel"))


def modular_polynomial_path(model: str, level: int) -> str:
    """
    Return a bundled modular polynomial table path.
    """
    return os.fspath(
        files(__package__).joinpath(
            "data", "kohel", "PolMod", model, f"pol.{level:03d}.dbz"
        )
    )


def hilbert_class_polynomial_path(discriminant: int) -> str:
    """
    Return a bundled Hilbert class polynomial table path.
    """
    discriminant = abs(int(discriminant))
    lower = 5000 * ((discriminant - 1) // 5000) + 1
    upper = lower + 4999
    return os.fspath(
        files(__package__).joinpath(
            "data",
            "kohel",
            "PolHeeg",
            "Cls",
            f"{lower:07d}-{upper:07d}",
            f"pol.{discriminant:07d}.dbz",
        )
    )


__all__ = [
    "hilbert_class_polynomial_path",
    "kohel_data_path",
    "modular_polynomial_path",
    "sage_data_path",
]
