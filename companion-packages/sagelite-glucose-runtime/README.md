# sagelite-glucose-runtime

Optional Glucose SAT solver executable companion package for `sagelite`.

Some Sage SAT solver doctests and interfaces call the standalone `glucose` and
`glucose-syrup` programs. The `sagelite` wheel does not include executable
files from Sage's build prefix, so installing this package in the same Python
environment provides relocatable console scripts backed by Sage-built binaries.

The nonparallel `glucose` executable is MIT-licensed. The parallel
`glucose-syrup` executable carries the same additional competition-use
restriction documented by Sage's `glucose` SPKG.

Build this package from a system or Sage prefix that already has Glucose
installed:

```bash
SAGELITE_GLUCOSE_BINDIR=/path/to/bin python -m build companion-packages/sagelite-glucose-runtime
```

If `SAGELITE_GLUCOSE_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the
same Sage prefix used to build the corresponding `sagelite` wheel.
