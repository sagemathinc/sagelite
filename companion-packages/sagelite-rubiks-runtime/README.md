# sagelite-rubiks-runtime

Optional Rubik solver executable companion package for `sagelite`.

Sage's Rubik's-cube functionality uses the command-line programs `cu2`,
`size222`, `optimal`, `mcube`, `dikcube`, and `cubex`. The `sagelite` wheel does
not bundle these optional executables in its core package. Installing this
companion package makes those commands available through standard Python entry
points.

Build this package from a system or Sage prefix that already has the Rubiks
programs installed:

```bash
SAGELITE_RUBIKS_BINDIR=/path/to/bin python -m build companion-packages/sagelite-rubiks-runtime
```

If `SAGELITE_RUBIKS_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the
same Sage prefix used to build the corresponding `sagelite` wheel.
