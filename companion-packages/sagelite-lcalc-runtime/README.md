# sagelite-lcalc-runtime

Optional lcalc executable companion package for `sagelite`.

Some Sage L-function features call Rubinstein's `lcalc` command. The
`sagelite` wheels include Sage's Python and extension modules, but not
executable files from Sage's build prefix, so installing this package in the
same Python environment provides a relocatable `lcalc` command.

This package is built by copying `lcalc` from an existing Sage prefix. Set
`SAGELITE_LCALC_BINDIR` to the directory containing the command:

```bash
SAGELITE_LCALC_BINDIR=/path/to/sage-local/bin \
python -m build companion-packages/sagelite-lcalc-runtime
```

If `SAGELITE_LCALC_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the
same Sage prefix used to build the corresponding `sagelite` wheel.
