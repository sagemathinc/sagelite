# sagelite-fplll-data

Optional FPLLL strategy data companion package for `sagelite`.

Sage can use `fpylll` for BKZ lattice reduction.  Some `fpylll` wheels contain
an absolute build-prefix path for FPLLL's BKZ strategy file, such as
`share/fplll/strategies/default.json`.  Installing this companion package gives
`sagelite` a relocatable copy of the redistributable strategy data.

Build this package from a system or Sage prefix that already has FPLLL
installed:

```bash
SAGELITE_FPLLL_STRATEGIES_DIR=/path/to/share/fplll/strategies python -m build companion-packages/sagelite-fplll-data
```

If `SAGELITE_FPLLL_STRATEGIES_DIR` is not set, the build checks `SAGE_LOCAL`
and common system locations.
