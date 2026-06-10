# sagelite-tides-runtime

Optional TIDES library companion package for `sagelite`.

Sage's TIDES desolvers generate C code and compile it against the `libTIDES`
static library and headers. The base `sagelite` wheel does not provide a Sage
runtime prefix containing those files. Installing this companion package makes
the redistributable TIDES runtime files available from normal wheel package
data.

Build this package from a system or Sage prefix that already has TIDES
installed:

```bash
SAGELITE_TIDES_PREFIX=/path/to/prefix python -m build companion-packages/sagelite-tides-runtime
```

If `SAGELITE_TIDES_PREFIX` is not set, the build checks `SAGE_LOCAL` and common
system locations.
