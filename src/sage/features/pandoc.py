r"""
Feature for testing the presence of ``pandoc``
"""
# ****************************************************************************
#       Copyright (C) 2018 Thierry Monteil <sage!lma.metelu.net>
#                     2021 Matthias Koeppe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  https://www.gnu.org/licenses/
# ****************************************************************************

import os

from . import Executable, FeatureNotPresentError


class Pandoc(Executable):
    r"""
    A :class:`~sage.features.Feature` describing the presence of :ref:`pandoc <spkg_pandoc>`.

    EXAMPLES::

        sage: from sage.features.pandoc import Pandoc
        sage: Pandoc().is_present()  # optional - pandoc
        FeatureTestResult('pandoc', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.pandoc import Pandoc
            sage: isinstance(Pandoc(), Pandoc)
            True
        """
        Executable.__init__(self, "pandoc", executable='pandoc',
                            url='https://pandoc.org/')

    def absolute_filename(self) -> str:
        r"""
        Return the path to ``pandoc``.

        This first searches the system ``PATH`` and then accepts the
        executable bundled by the PyPI package ``pypandoc-binary``.

        TESTS::

            sage: from sage.features.pandoc import Pandoc
            sage: isinstance(Pandoc().absolute_filename(), str)  # optional - pandoc
            True
        """
        try:
            return super().absolute_filename()
        except FeatureNotPresentError:
            pass

        try:
            from pypandoc import get_pandoc_path
        except ImportError:
            get_pandoc_path = None

        if get_pandoc_path is not None:
            try:
                path = get_pandoc_path()
            except Exception:
                path = None
            if path and os.path.isfile(path) and os.access(path, os.X_OK):
                return os.fspath(path)

        raise FeatureNotPresentError(
            self,
            reason=(
                "Executable 'pandoc' not found on PATH, and pypandoc-binary "
                "did not provide a bundled pandoc executable."
            ),
        )


def all_features():
    return [Pandoc()]
