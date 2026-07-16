import os
from importlib.resources import files

from .tables import table_errors


def meataxe_dir() -> str:
    """
    Return the bundled MeatAxe multiplication-table directory.
    """
    directory = os.fspath(files(__package__).joinpath("data", "meataxe"))
    errors = table_errors(directory)
    if errors:
        raise RuntimeError(
            "bundled MeatAxe table directory is invalid: "
            + "; ".join(errors[:5])
            + (" ..." if len(errors) > 5 else "")
        )
    return directory


__all__ = ["meataxe_dir"]
