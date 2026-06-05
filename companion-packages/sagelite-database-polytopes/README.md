# sagelite-database-polytopes

Optional reflexive polytope database companion package for `sagelite`.

The `sagelite` wheels include Sage's reflexive polytope database interfaces, but
not the database payload. Installing this package in the same Python environment
contributes the bundled `reflexive_polytopes` data directory through Sage's
`sagemath.data_paths` entry point mechanism.

This package contains the standard Sage `polytopes_db` SPKG payload for
2-dimensional and 3-dimensional reflexive polytopes. It does not contain the
separate 4-dimensional `polytopes_db_4d` payload.
