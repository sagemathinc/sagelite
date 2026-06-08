# sagelite-planarity-runtime

Optional planarity executable companion package for `sagelite`.

Sage builds the `planarity` command and `libplanarity` library for
planarity-related graph algorithms. Some optional Sage runtimes, including GAP
package integrations, can call this command as an external executable. The
`sagelite` core wheel does not bundle it directly. Installing this companion
package makes `planarity` available through a standard Python entry point.

Build this package from a system or Sage prefix that already has planarity
installed:

```bash
SAGELITE_PLANARITY_BINDIR=/path/to/bin python -m build companion-packages/sagelite-planarity-runtime
```

If `SAGELITE_PLANARITY_BINDIR` is not set, the build checks `SAGE_LOCAL/bin`
and common system locations. For production wheels, build this package from the
same Sage prefix used to build the corresponding `sagelite` wheel.
