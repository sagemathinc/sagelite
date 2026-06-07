# sagelite-buckygen-runtime

Optional buckygen executable companion package for `sagelite`.

Some Sage graph-generation code calls the `buckygen` command-line tool. The
`sagelite` wheels do not include executable files from Sage's build prefix, so
installing this package in the same Python environment provides a relocatable
wrapper script for a Sage-built `buckygen` binary.

This package is built by copying `buckygen` from an existing Sage prefix. Set
`SAGELITE_BUCKYGEN_BINDIR` to the directory containing `buckygen`:

```bash
SAGELITE_BUCKYGEN_BINDIR=/path/to/sage-local/bin \
python -m build companion-packages/sagelite-buckygen-runtime
```

If `SAGELITE_BUCKYGEN_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the same
Sage prefix used to build the corresponding `sagelite` wheel.
