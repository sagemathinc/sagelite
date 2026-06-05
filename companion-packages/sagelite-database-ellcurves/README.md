# sagelite-database-ellcurves

Optional elliptic curves database companion package for `sagelite`.

The `sagelite` wheels include Sage's elliptic curve database interfaces, but not
William Stein's database of interesting elliptic curves. Installing this package
in the same Python environment contributes the bundled `ellcurves` data
directory through Sage's `sagemath.data_paths` entry point mechanism.

This package contains the `ellcurves` part of Sage's standard `elliptic_curves`
SPKG. The mini Cremona SQLite database is packaged separately as
`sagelite-database-cremona-mini`.
