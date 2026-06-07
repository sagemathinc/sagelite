# sagelite-sympow-runtime

Optional SYMPOW executable companion package for `sagelite`.

Sage's elliptic-curve L-series interfaces can call the standalone `sympow`
program for analytic ranks and modular degrees. The `sagelite` wheels include
Sage's Python and extension modules, but not executable files from Sage's build
prefix, so installing this package in the same Python environment provides a
relocatable `sympow` command.

This package is built by copying `sympow` from an existing Sage prefix. Set
`SAGELITE_SYMPOW_BINDIR` to the directory containing `sympow`:

```bash
SAGELITE_SYMPOW_BINDIR=/path/to/sage-local/bin \
python -m build companion-packages/sagelite-sympow-runtime
```

If `SAGELITE_SYMPOW_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. If the build prefix has SYMPOW data files outside the
executable's own layout, set `SAGELITE_SYMPOW_DATAFILES` to that directory.
For production wheels, build this package from the same Sage prefix used to
build the corresponding `sagelite` wheel.
