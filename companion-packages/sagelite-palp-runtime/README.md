# sagelite-palp-runtime

Optional PALP executable companion package for `sagelite`.

Sage's lattice-polytope and toric-geometry doctests use the PALP command-line
programs `poly.x`, `class.x`, `nef.x`, and `cws.x`, including the
dimension-specific variants built by Sage. The `sagelite` wheel does not bundle
these executables in its core package. Installing this companion package makes
those commands available through standard Python entry points.

Build this package from a system or Sage prefix that already has PALP installed:

```bash
SAGELITE_PALP_BINDIR=/path/to/bin python -m build companion-packages/sagelite-palp-runtime
```

If `SAGELITE_PALP_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the
same Sage prefix used to build the corresponding `sagelite` wheel.
