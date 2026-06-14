from .runtime import pari_data_dir


def sage_data_path() -> str:
    """
    Return the root directory contributed to ``sage.env.sage_data_paths``.
    """
    return pari_data_dir()


__all__ = ["pari_data_dir", "sage_data_path"]
