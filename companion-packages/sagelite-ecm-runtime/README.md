# sagelite-ecm-runtime

Optional GMP-ECM executable companion package for `sagelite`.

The `sagelite` wheels include the GMP-ECM library used by
`sage.libs.libecm`, but some Sage interfaces call the `ecm` executable.
Installing this package in the same Python environment gives `sagelite` a
relocatable executable path without requiring users to set `SAGE_ECMBIN`.

This package is built by copying an existing `ecm` or `gmp-ecm` executable
into the wheel. Set `SAGELITE_ECM_BINDIR` to the directory containing the
executable:

```bash
SAGELITE_ECM_BINDIR=/path/to/bin python -m build companion-packages/sagelite-ecm-runtime
```

For production wheels, build this package from the same Sage-built prefix used
to build the corresponding `sagelite` wheel.
