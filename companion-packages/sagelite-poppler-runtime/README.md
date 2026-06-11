# sagelite-poppler-runtime

Optional Poppler executable companion package for `sagelite`.

Sage's graphics conversion code can use the `pdftocairo` command when
converting PDF output to raster or vector formats. The `sagelite` wheel does
not bundle this executable in its core package. Installing this companion
package makes `pdftocairo` available through a standard Python entry point.

Build this package from a system or Sage prefix that already has Poppler tools
installed:

```bash
SAGELITE_POPPLER_BINDIR=/path/to/bin python -m build companion-packages/sagelite-poppler-runtime
```

If `SAGELITE_POPPLER_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the
same Sage prefix used to build the corresponding `sagelite` wheel.
