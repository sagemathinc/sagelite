# sagelite-4ti2-runtime

Optional 4ti2 executable companion package for `sagelite`.

Some Sage lattice point and toric geometry functionality calls 4ti2 command-line
tools such as `hilbert`, `zsolve`, and `groebner`. The `sagelite` wheels do not
include executable files from Sage's build prefix, so installing this package in
the same Python environment provides relocatable wrapper scripts for Sage-built
4ti2 binaries.

This package is built by copying the 4ti2 executables from an existing Sage
prefix. Set `SAGELITE_4TI2_BINDIR` to the directory containing `hilbert` and
`zsolve`:

```bash
SAGELITE_4TI2_BINDIR=/path/to/sage-local/bin \
python -m build companion-packages/sagelite-4ti2-runtime
```

If `SAGELITE_4TI2_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the same
Sage prefix used to build the corresponding `sagelite` wheel.
