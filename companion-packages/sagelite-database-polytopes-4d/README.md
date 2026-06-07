# sagelite-database-polytopes-4d

Optional 4-dimensional reflexive polytope database companion package for
`sagelite`.

The `sagelite` wheels include Sage's reflexive polytope database interfaces,
but not the large 4-dimensional database payload. Installing this package in
the same Python environment contributes the bundled `reflexive_polytopes` data
directory through Sage's `sagemath.data_paths` entry point mechanism.

This package contains the optional Sage `polytopes_db_4d` SPKG payload,
including the `Hodge4d` database.
