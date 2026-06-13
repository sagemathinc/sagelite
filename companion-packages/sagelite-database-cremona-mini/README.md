# sagelite-database-cremona-mini

Companion data wheel for `sagelite` that provides John Cremona's mini
elliptic-curve database.

When this package is installed in the same environment as `sagelite`, Sage
discovers the bundled data directory through the `sagemath.data_paths` entry
point group. No manual `SAGE_DATA_PATH` configuration is required.

The database payload is `cremona/cremona_mini.db`. Wheels install it both as
relocatable package data and under `share/cremona` for Sage builds that search a
standard data prefix.

To test installation directly from GitHub, use:

```bash
pip install "git+https://github.com/sagemathinc/sagelite.git@develop#subdirectory=companion-packages/sagelite-database-cremona-mini"
```

This requires a `sagelite` build that includes the companion data-path hook in
`sage.env.sage_data_paths()`.
