r"""
Feature for testing the presence of ``meataxe``
"""

# *****************************************************************************
#       Copyright (C) 2021 Matthias Koeppe
#                     2021 Kwankyu Lee
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# *****************************************************************************

import os

from . import FeatureTestResult, PythonModule, StaticFile
from .join_feature import JoinFeature


class MeatAxeTables(StaticFile):
    r"""
    A :class:`~sage.features.Feature` describing the presence of the MeatAxe
    multiplication tables.

    EXAMPLES::

        sage: from sage.features.meataxe import MeatAxeTables
        sage: isinstance(MeatAxeTables(), MeatAxeTables)
        True
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.meataxe import MeatAxeTables
            sage: isinstance(MeatAxeTables(), MeatAxeTables)
            True
        """
        from sage.env import MTXLIB

        StaticFile.__init__(self, 'meataxe_tables', filename='p009.zzz',
                            search_path=[MTXLIB] if MTXLIB else [],
                            spkg='meataxe')

    def _is_present(self):
        r"""
        Return whether the MeatAxe multiplication tables are usable.

        The Sage MeatAxe extension imports successfully without these runtime
        tables, but matrix operations over finite fields need them at runtime.
        """
        result = super()._is_present()
        if not result:
            return result

        table_dir = os.path.dirname(self.absolute_filename())
        required_tables = ('p002.zzz', 'p009.zzz', 'p025.zzz', 'p125.zzz', 'p251.zzz')
        missing = [
            table for table in required_tables
            if not os.path.isfile(os.path.join(table_dir, table))
        ]
        if missing:
            return FeatureTestResult(
                self, False,
                reason="MeatAxe table directory is incomplete; missing "
                + ", ".join(missing),
            )
        return result


class Meataxe(JoinFeature):
    r"""
    A :class:`~sage.features.Feature` describing the presence of the Sage modules
    that depend on the :ref:`meataxe <spkg_meataxe>` library.

    EXAMPLES::

        sage: from sage.features.meataxe import Meataxe
        sage: Meataxe().is_present()  # optional - meataxe
        FeatureTestResult('meataxe', True)
    """
    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.meataxe import Meataxe
            sage: isinstance(Meataxe(), Meataxe)
            True
        """
        JoinFeature.__init__(self, 'meataxe',
                             [PythonModule('sage.matrix.matrix_gfpn_dense',
                                           spkg='meataxe'),
                              MeatAxeTables()])


def all_features():
    return [Meataxe()]
