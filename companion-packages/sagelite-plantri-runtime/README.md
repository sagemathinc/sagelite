# sagelite-plantri-runtime

Optional plantri executable companion package for `sagelite`.

Sage's graph generator doctests use the `plantri` command for planar graph,
triangulation, and quadrangulation generation. The `sagelite` wheel does not
bundle this executable in its core package. Installing this companion package
makes `plantri` available through a standard Python entry point.

Build this package from a system or Sage prefix that already has plantri
installed:

```bash
SAGELITE_PLANTRI_BINDIR=/path/to/bin python -m build companion-packages/sagelite-plantri-runtime
```

If `SAGELITE_PLANTRI_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the
same Sage prefix used to build the corresponding `sagelite` wheel.
