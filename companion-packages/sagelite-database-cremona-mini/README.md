# sagelite-database-cremona-mini

Companion data wheel for `sagelite` that provides John Cremona's mini
elliptic-curve database.

When this package is installed in the same environment as `sagelite`, Sage
discovers the bundled data directory through the `sagemath.data_paths` entry
point group. No manual `SAGE_DATA_PATH` configuration is required.

The database payload is `cremona/cremona_mini.db`.
