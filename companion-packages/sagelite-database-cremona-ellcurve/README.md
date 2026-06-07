# sagelite-database-cremona-ellcurve

Optional full Cremona elliptic-curve database companion package for `sagelite`.

The `sagelite` wheel does not bundle John Cremona's full elliptic-curve
database. This companion package carries `cremona.db` as wheel package data and
registers the bundled data directory through Sage's `sagemath.data_paths` entry
point mechanism.

No manual `SAGE_DATA_PATH` configuration is required after installation.

Build the wheel from an existing Sage data installation by pointing at the
database file:

```sh
SAGELITE_CREMONA_ELLCURVE_DB=/path/to/cremona.db \
  python -m build companion-packages/sagelite-database-cremona-ellcurve
```

If `SAGELITE_CREMONA_ELLCURVE_DB` is not set, the build checks
`CREMONA_LARGE_DATA_DIR`, `SAGE_SHARE/cremona/cremona.db`, and
`SAGE_LOCAL/share/cremona/cremona.db`.
