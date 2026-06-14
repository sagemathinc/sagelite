# sagelite-pari-data

Companion data wheel for `sagelite` that provides PARI data directories such
as `galdata`, `elldata`, `seadata`, `galpol`, and `nftables`, together with
Sage's redistributable PARI helper scripts.

Set `SAGELITE_PARI_DATA_DIR` to a PARI data root containing `galdata`,
`elldata`, `seadata`, and `galpol`. If that root does not already contain
`nftables`, set `SAGELITE_PARI_NFTABLES_TARBALL` to Sage's `pari_nftables`
tarball so the wheel can include the complete advertised payload.

When this package is installed in the same environment as `sagelite`,
`sage.libs.pari` points PARI's `datadir` default at the bundled data directory.
No manual PARI configuration is required.

To test installation directly from GitHub, use:

```bash
pip install "git+https://github.com/sagemathinc/sagelite.git@develop#subdirectory=companion-packages/sagelite-pari-data"
```
