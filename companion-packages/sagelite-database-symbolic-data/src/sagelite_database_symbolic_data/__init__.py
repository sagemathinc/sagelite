from importlib.resources import files
import os


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return os.fspath(files(__package__).joinpath("data"))


def symbolic_data_path() -> str:
    """
    Return the bundled SymbolicData database directory.
    """
    return os.fspath(files(__package__).joinpath("data", "symbolic_data"))


def xml_resources_path() -> str:
    """
    Return the bundled SymbolicData XML resources directory.
    """
    return os.fspath(
        files(__package__).joinpath("data", "symbolic_data", "Data", "XMLResources")
    )


__all__ = ["sage_data_path", "symbolic_data_path", "xml_resources_path"]
