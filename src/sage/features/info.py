r"""
Feature for testing the presence of ``info``, from GNU Info
"""

import importlib.util
import os
import sys
from pathlib import Path

from . import Executable, FeatureNotPresentError


def _runtime_module():
    """
    Return the optional ``sagelite_info.runtime`` module from ``sys.path``.
    """
    for entry in sys.path:
        runtime_path = Path(entry, "sagelite_info", "runtime.py")
        if not runtime_path.is_file():
            continue
        spec = importlib.util.spec_from_file_location(
            "_sage_info_runtime", runtime_path
        )
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    return None


class Info(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of :ref:`info <spkg_info>`.

    EXAMPLES::

        sage: from sage.features.info import Info
        sage: Info()
        Feature('info')
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.info import Info
            sage: isinstance(Info(), Info)
            True
        """
        Executable.__init__(self, 'info', executable='info',
                            spkg='info', type='standard')

    def absolute_filename(self) -> str:
        r"""
        Return the ``info`` executable path.

        Normal Sage installations find ``info`` on ``PATH``. Wheel
        installations can also provide it through the optional
        ``sagelite-info-runtime`` companion package.
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError as error:
            original_error = error

        runtime = _runtime_module()
        if runtime is None:
            raise original_error

        executable = runtime.executable_path()
        if executable.is_file() and os.access(executable, os.X_OK):
            return os.fspath(executable)

        raise original_error


def all_features():
    return [Info()]
