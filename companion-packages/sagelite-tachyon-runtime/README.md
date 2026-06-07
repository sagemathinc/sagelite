# sagelite-tachyon-runtime

Optional Tachyon executable companion package for `sagelite`.

Sage's 3D plotting and Tachyon interface doctests invoke the `tachyon`
raytracer as an external command. The `sagelite` wheel does not bundle this
executable in its core package. Installing this companion package makes
`tachyon` available through a standard Python entry point.

Build this package from a system or Sage prefix that already has Tachyon
installed:

```bash
SAGELITE_TACHYON_BINDIR=/path/to/bin python -m build companion-packages/sagelite-tachyon-runtime
```

If `SAGELITE_TACHYON_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the
same Sage prefix used to build the corresponding `sagelite` wheel.
