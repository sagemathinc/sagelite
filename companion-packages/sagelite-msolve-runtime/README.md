# sagelite-msolve-runtime

Optional msolve executable companion package for `sagelite`.

Some Sage polynomial system solving doctests and interfaces call the standalone
`msolve` program. The `sagelite` wheel does not include executable files from
Sage's build prefix, so installing this package in the same Python environment
provides a relocatable `msolve` command backed by a Sage-built binary.

Build this package from a system or Sage prefix that already has msolve
installed:

```bash
SAGELITE_MSOLVE_BINDIR=/path/to/bin python -m build companion-packages/sagelite-msolve-runtime
```

If `SAGELITE_MSOLVE_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the
same Sage prefix used to build the corresponding `sagelite` wheel.
