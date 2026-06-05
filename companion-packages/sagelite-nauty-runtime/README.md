# sagelite-nauty-runtime

Optional nauty executable companion package for `sagelite`.

Some Sage graph generators call nauty command-line tools such as `geng` and
`genposetg`. The `sagelite` wheels do not include executable files from Sage's
build prefix, so installing this package in the same Python environment provides
relocatable wrapper scripts for Sage-built nauty binaries.

This package is built by copying the nauty executables from an existing Sage
prefix. Set `SAGELITE_NAUTY_BINDIR` to the directory containing `geng` and
`genposetg`:

```bash
SAGELITE_NAUTY_BINDIR=/path/to/sage-local/bin \
python -m build companion-packages/sagelite-nauty-runtime
```

If `SAGELITE_NAUTY_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the same
Sage prefix used to build the corresponding `sagelite` wheel.
