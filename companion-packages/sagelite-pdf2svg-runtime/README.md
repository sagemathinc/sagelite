# sagelite-pdf2svg-runtime

Optional pdf2svg executable companion package for `sagelite`.

Sage's graphics and conversion code can use the `pdf2svg` command when
converting PDF output to SVG. The `sagelite` wheel does not bundle this
executable in its core package. Installing this companion package makes
`pdf2svg` available through a standard Python entry point.

Build this package from a system or Sage prefix that already has pdf2svg
installed:

```bash
SAGELITE_PDF2SVG_BINDIR=/path/to/bin python -m build companion-packages/sagelite-pdf2svg-runtime
```

If `SAGELITE_PDF2SVG_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the
same Sage prefix used to build the corresponding `sagelite` wheel.
