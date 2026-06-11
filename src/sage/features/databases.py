r"""
Features for testing the presence of various databases
"""

# *****************************************************************************
#       Copyright (C) 2016      Julian Rüth
#                     2018-2019 Jeroen Demeyer
#                     2018      Timo Kaufmann
#                     2020-2022 Matthias Koeppe
#                     2020-2022 Sebastian Oehms
#                     2021      Kwankyu Lee
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  https://www.gnu.org/licenses/
# *****************************************************************************

from sage.env import sage_data_paths
from sage.features import PythonModule, StaticFile
from sage.features.join_feature import JoinFeature


def _search_path_with_registered_data(configured, name):
    """
    Return configured data directories plus registered companion-wheel paths.
    """
    if configured is None:
        paths = []
    elif isinstance(configured, (str, bytes)):
        paths = [configured]
    else:
        paths = list(configured)

    paths = [path for path in paths if path]
    paths.extend(sage_data_paths(name))
    return tuple(paths)


class DatabaseCremona(StaticFile):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of :ref:`John Cremona's
    database of elliptic curves <spkg_database_cremona_ellcurve>`.

    INPUT:

    - ``name`` -- either ``'cremona'`` (the default) for the full large
      database or ``'cremona_mini'`` for the small database

    EXAMPLES::

        sage: from sage.features.databases import DatabaseCremona
        sage: DatabaseCremona('cremona_mini', type='standard').is_present()
        FeatureTestResult('database_cremona_mini_ellcurve', True)
        sage: DatabaseCremona().is_present()                                    # optional - database_cremona_ellcurve
        FeatureTestResult('database_cremona_ellcurve', True)
    """

    def __init__(
        self, name="cremona", spkg="database_cremona_ellcurve", type="optional"
    ):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseCremona
            sage: isinstance(DatabaseCremona(), DatabaseCremona)
            True
        """
        from sage.env import CREMONA_LARGE_DATA_DIR, CREMONA_MINI_DATA_DIR

        CREMONA_DATA_DIRS = [CREMONA_MINI_DATA_DIR, CREMONA_LARGE_DATA_DIR]
        search_path = _search_path_with_registered_data(CREMONA_DATA_DIRS, "cremona")

        spkg = "database_cremona_ellcurve"
        spkg_type = "optional"
        if name == "cremona_mini":
            spkg = "elliptic_curves"
            spkg_type = "standard"

        StaticFile.__init__(
            self,
            f"database_{name}_ellcurve",
            filename=f"{name}.db",
            search_path=search_path,
            spkg=spkg,
            type=spkg_type,
            url="https://github.com/JohnCremona/ecdata",
            description="Cremona's database of elliptic curves",
        )


class DatabaseEllcurves(StaticFile):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of
    William Stein's database of interesting curves.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseEllcurves
        sage: bool(DatabaseEllcurves().is_present())  # optional - database_ellcurves
        True
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseEllcurves
            sage: isinstance(DatabaseEllcurves(), DatabaseEllcurves)
            True
        """
        from sage.env import ELLCURVE_DATA_DIR

        search_path = _search_path_with_registered_data(ELLCURVE_DATA_DIR, "ellcurves")

        StaticFile.__init__(
            self,
            "database_ellcurves",
            filename="rank0",
            search_path=search_path,
            spkg="elliptic_curves",
            type="standard",
            description="William Stein's database of interesting curve",
        )


class DatabaseGraphs(StaticFile):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of
    the graphs database.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseGraphs
        sage: bool(DatabaseGraphs().is_present())  # optional - database_graphs
        True
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseGraphs
            sage: isinstance(DatabaseGraphs(), DatabaseGraphs)
            True
        """
        from sage.env import GRAPHS_DATA_DIR

        search_path = _search_path_with_registered_data(GRAPHS_DATA_DIR, "graphs")

        StaticFile.__init__(
            self,
            "database_graphs",
            filename="graphs.db",
            search_path=search_path,
            spkg="graphs",
            type="standard",
            description="A database of graphs",
        )


class DatabaseJones(StaticFile):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of
    :ref:`John Jones's tables of number fields <spkg_database_jones_numfield>`.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseJones
        sage: bool(DatabaseJones().is_present())  # optional - database_jones_numfield
        True
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseJones
            sage: isinstance(DatabaseJones(), DatabaseJones)
            True
        """
        StaticFile.__init__(
            self,
            "database_jones_numfield",
            filename="jones.sobj",
            search_path=tuple(sage_data_paths("jones")),
            spkg="database_jones_numfield",
            description="John Jones's tables of number fields",
        )


class DatabaseKnotInfo(PythonModule):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of the
    :ref:`package providing the KnotInfo and LinkInfo databases <spkg_database_knotinfo>`.

    The homes of these databases are the
    web-pages `KnotInfo <https://knotinfo.org/>`__ and
    `LinkInfo <https://link-info-repo.onrender.com/>`__.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseKnotInfo
        sage: DatabaseKnotInfo().is_present()  # optional - database_knotinfo
        FeatureTestResult('database_knotinfo', True)
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseKnotInfo
            sage: isinstance(DatabaseKnotInfo(), DatabaseKnotInfo)
            True
        """
        PythonModule.__init__(self, "database_knotinfo", spkg="database_knotinfo")


class DatabaseMatroids(PythonModule):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of
    :ref:`Yoshitake Matsumoto's Database of Matroids <spkg_matroid_database>`.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseMatroids
        sage: DatabaseMatroids().is_present()                                           # optional - matroid_database
        FeatureTestResult('matroid_database', True)

    REFERENCES:

    [Mat2012]_
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseMatroids
            sage: isinstance(DatabaseMatroids(), DatabaseMatroids)
            True
        """
        PythonModule.__init__(self, "matroid_database", spkg="matroid_database")


class DatabaseCubicHecke(PythonModule):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of the
    :ref:`Cubic Hecke algebra database package <spkg_database_cubic_hecke>`.

    The home of this database is the
    web-page `Cubic Hecke algebra on 4 strands <http://www.lamfa.u-picardie.fr/marin/representationH4-en.html>`__
    of Ivan Marin.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseCubicHecke
        sage: DatabaseCubicHecke().is_present()  # optional - database_cubic_hecke
        FeatureTestResult('database_cubic_hecke', True)
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseCubicHecke
            sage: isinstance(DatabaseCubicHecke(), DatabaseCubicHecke)
            True
        """
        PythonModule.__init__(self, "database_cubic_hecke", spkg="database_cubic_hecke")


class DatabaseCunninghamTables(StaticFile):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of
    :ref:`Cunningham tables <spkg_cunningham_tables>`.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseCunninghamTables
        sage: DatabaseCunninghamTables().is_present()  # optional - cunningham_tables
        FeatureTestResult('cunningham_tables', True)
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseCunninghamTables
            sage: isinstance(DatabaseCunninghamTables(), DatabaseCunninghamTables)
            True
        """
        StaticFile.__init__(
            self,
            "cunningham_tables",
            filename="cunningham_prime_factors.sobj",
            search_path=tuple(sage_data_paths("cunningham_tables")),
            spkg="cunningham_tables",
            description="Cunningham tables",
        )


class DatabaseKohel(StaticFile):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of
    :ref:`David Kohel's modular-polynomial databases <spkg_database_kohel>`.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseKohel
        sage: DatabaseKohel().is_present()  # optional - database_kohel
        FeatureTestResult('database_kohel', True)
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseKohel
            sage: isinstance(DatabaseKohel(), DatabaseKohel)
            True
        """
        StaticFile.__init__(
            self,
            "database_kohel",
            filename="PolMod/Cls/pol.001.dbz",
            search_path=tuple(sage_data_paths("kohel")),
            spkg="database_kohel",
            description="Kohel modular-polynomial databases",
        )


class DatabaseMutationClass(StaticFile):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of the
    cluster-algebra quiver mutation-class database.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseMutationClass
        sage: DatabaseMutationClass().is_present()  # optional - database_mutation_class
        FeatureTestResult('database_mutation_class', True)
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseMutationClass
            sage: isinstance(DatabaseMutationClass(), DatabaseMutationClass)
            True
        """
        StaticFile.__init__(
            self,
            "database_mutation_class",
            filename="mutation_classes_2.dig6",
            search_path=tuple(sage_data_paths("cluster_algebra_quiver")),
            spkg="database_mutation_class",
            description="Cluster algebra quiver mutation classes",
        )


class DatabaseOdlyzkoZeta(StaticFile):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of
    :ref:`Odlyzko's zeta-zero database <spkg_database_odlyzko_zeta>`.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseOdlyzkoZeta
        sage: DatabaseOdlyzkoZeta().is_present()  # optional - database_odlyzko_zeta
        FeatureTestResult('database_odlyzko_zeta', True)
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseOdlyzkoZeta
            sage: isinstance(DatabaseOdlyzkoZeta(), DatabaseOdlyzkoZeta)
            True
        """
        StaticFile.__init__(
            self,
            "database_odlyzko_zeta",
            filename="zeros.sobj",
            search_path=tuple(sage_data_paths("odlyzko")),
            spkg="database_odlyzko_zeta",
            description="Odlyzko zeta-zero database",
        )


class DatabaseReflexivePolytopes(StaticFile):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of the
    :ref:`PALP databases of reflexive three-dimensional <spkg_polytopes_db>`
    and :ref:`four-dimensional lattice polytopes <spkg_polytopes_db_4d>`.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseReflexivePolytopes
        sage: bool(DatabaseReflexivePolytopes().is_present())                   # optional - polytopes_db
        True
        sage: bool(DatabaseReflexivePolytopes('polytopes_db_4d').is_present())  # optional - polytopes_db_4d
        True
    """

    def __init__(self, name="polytopes_db"):
        """
        TESTS::

            sage: from sage.features.databases import DatabaseReflexivePolytopes
            sage: isinstance(DatabaseReflexivePolytopes(), DatabaseReflexivePolytopes)
            True
            sage: DatabaseReflexivePolytopes().filename
            'Full3d'
            sage: DatabaseReflexivePolytopes('polytopes_db_4d').filename
            'Hodge4d'
        """
        from sage.env import POLYTOPE_DATA_DIR

        search_path = _search_path_with_registered_data(
            POLYTOPE_DATA_DIR, "reflexive_polytopes"
        )

        dirname = "Full3d"
        if name == "polytopes_db_4d":
            dirname = "Hodge4d"

        StaticFile.__init__(self, name, filename=dirname, search_path=search_path)


class DatabaseSymbolicData(StaticFile):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of
    :ref:`SymbolicData <spkg_database_symbolic_data>`.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseSymbolicData
        sage: DatabaseSymbolicData().is_present()  # optional - database_symbolic_data
        FeatureTestResult('database_symbolic_data', True)
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseSymbolicData
            sage: isinstance(DatabaseSymbolicData(), DatabaseSymbolicData)
            True
        """
        StaticFile.__init__(
            self,
            "database_symbolic_data",
            filename="Data/XMLResources/INTPS",
            search_path=tuple(sage_data_paths("symbolic_data")),
            spkg="database_symbolic_data",
            description="SymbolicData benchmark database",
        )


class DatabaseSteinWatkinsMini(JoinFeature):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of the
    small Stein-Watkins elliptic-curve database.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseSteinWatkinsMini
        sage: DatabaseSteinWatkinsMini().is_present()  # optional - database_stein_watkins_mini
        FeatureTestResult('database_stein_watkins_mini', True)
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseSteinWatkinsMini
            sage: isinstance(DatabaseSteinWatkinsMini(), DatabaseSteinWatkinsMini)
            True
        """
        search_path = tuple(sage_data_paths("stein_watkins"))
        files = [
            StaticFile(
                "database_stein_watkins_mini_all_000",
                filename="a.000.bz2",
                search_path=search_path,
                spkg="database_stein_watkins_mini",
                description="Stein-Watkins mini all-conductor table a.000",
            ),
            StaticFile(
                "database_stein_watkins_mini_all_001",
                filename="a.001.bz2",
                search_path=search_path,
                spkg="database_stein_watkins_mini",
                description="Stein-Watkins mini all-conductor table a.001",
            ),
            StaticFile(
                "database_stein_watkins_mini_prime_00",
                filename="p.00.bz2",
                search_path=search_path,
                spkg="database_stein_watkins_mini",
                description="Stein-Watkins mini prime-conductor table p.00",
            ),
        ]
        JoinFeature.__init__(
            self,
            "database_stein_watkins_mini",
            files,
            spkg="database_stein_watkins_mini",
            description="Stein-Watkins mini elliptic-curve database",
            type="optional",
        )


class DatabaseSteinWatkins(StaticFile):
    r"""
    A :class:`~sage.features.Feature` which describes the presence of the
    full Stein-Watkins elliptic-curve database.

    EXAMPLES::

        sage: from sage.features.databases import DatabaseSteinWatkins
        sage: DatabaseSteinWatkins().is_present()  # optional - database_stein_watkins
        FeatureTestResult('database_stein_watkins', True)
    """

    def __init__(self):
        r"""
        TESTS::

            sage: from sage.features.databases import DatabaseSteinWatkins
            sage: isinstance(DatabaseSteinWatkins(), DatabaseSteinWatkins)
            True
        """
        StaticFile.__init__(
            self,
            "database_stein_watkins",
            filename="a.002.bz2",
            search_path=tuple(sage_data_paths("stein_watkins")),
            spkg="database_stein_watkins",
            description="Stein-Watkins full elliptic-curve database",
        )


def all_features():
    return [
        PythonModule("conway_polynomials", spkg="conway_polynomials", type="standard"),
        DatabaseCremona(),
        DatabaseCremona("cremona_mini", type="standard"),
        DatabaseEllcurves(),
        DatabaseGraphs(),
        DatabaseJones(),
        DatabaseKnotInfo(),
        DatabaseMatroids(),
        DatabaseCubicHecke(),
        DatabaseCunninghamTables(),
        DatabaseKohel(),
        DatabaseMutationClass(),
        DatabaseOdlyzkoZeta(),
        DatabaseReflexivePolytopes(),
        DatabaseReflexivePolytopes("polytopes_db_4d"),
        DatabaseSymbolicData(),
        DatabaseSteinWatkinsMini(),
        DatabaseSteinWatkins(),
    ]
