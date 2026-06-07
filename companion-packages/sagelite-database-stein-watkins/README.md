# sagelite-database-stein-watkins

Optional Stein-Watkins full database companion package for `sagelite`.

This package contains the full `database_stein_watkins` payload from SageMath,
installed as a Python wheel. Installing it makes Sage's
`database_stein_watkins` optional doctests and `SteinWatkinsAllData` /
`SteinWatkinsPrimeData` lookups available without making the huge database a
hard dependency of `sagelite`.

Build the wheel with a local copy of the database payload:

```sh
SAGELITE_STEIN_WATKINS_DIR=/path/to/stein_watkins \
  python -m build companion-packages/sagelite-database-stein-watkins
```

The build also searches `DATABASE_STEIN_WATKINS_DIR`,
`SAGE_SHARE/stein_watkins`, `SAGE_LOCAL/share/stein_watkins`, and
`local/share/stein_watkins`.
