# sagelite-pari-data

Companion data wheel for `sagelite` that provides PARI data directories such
as `galdata`, `elldata`, `seadata`, `galpol`, and `nftables` when they are
available in the Sage-built PARI prefix.

When this package is installed in the same environment as `sagelite`,
`sage.libs.pari` points PARI's `datadir` default at the bundled data directory.
No manual PARI configuration is required.

To test installation directly from GitHub, use:

```bash
pip install "git+https://github.com/sagemathinc/sagelite.git@develop#subdirectory=companion-packages/sagelite-pari-data"
```

