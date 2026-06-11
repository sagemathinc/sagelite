# sagelite-database-sloane

Optional Sloane/OEIS local database companion package for `sagelite`.

The `sagelite` wheel does not bundle the local Sloane Encyclopedia database.
This companion package carries `sloane-oeis.bz2` and `sloane-names.bz2` as
wheel package data and registers the bundled data directory through Sage's
`sagemath.data_paths` entry point mechanism.

No manual `SAGE_DATA_PATH` configuration is required after installation.

Build the wheel from downloaded OEIS data files:

```sh
SAGELITE_SLOANE_STRIPPED_GZ=/path/to/stripped.gz \
SAGELITE_SLOANE_NAMES_GZ=/path/to/names.gz \
  python -m build companion-packages/sagelite-database-sloane
```

If those variables are not set, the build checks `SAGELITE_SLOANE_DATA_DIR`,
`DOT_SAGE/db/sloane`, and the package's bundled sdist data directory for
`sloane-oeis.bz2` and `sloane-names.bz2`.
