import types

from sage.misc.sageinspect import sage_getfile_relative


def test_sage_getfile_relative_normalizes_installed_wheel_build_paths():
    module = types.ModuleType("sage.example")
    module.__doc__ = (
        "File: /scratch/sagelite-build/src/sage/example.pyx "
        "(starting at line 1)"
    )

    assert sage_getfile_relative(module) == "sage/example.pyx"


def test_sage_getfile_relative_keeps_non_sage_build_paths_absolute():
    module = types.ModuleType("not_sage.example")
    module.__doc__ = (
        "File: /scratch/sagelite-build/src/not_sage/example.pyx "
        "(starting at line 1)"
    )

    assert (
        sage_getfile_relative(module)
        == "/scratch/sagelite-build/src/not_sage/example.pyx"
    )
