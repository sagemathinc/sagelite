# sagelite-graphviz-runtime

Optional Graphviz executable companion package for `sagelite`.

Sage uses the `dot`, `neato`, and `twopi` programs for graph layout features
and doctests marked `optional - graphviz`. The `sagelite` core wheel does not
bundle these external executables directly. Installing this companion package
makes them available through standard Python entry points and through Sage's
Graphviz feature detection.

Build this package from a system or prefix that already has Graphviz installed:

```bash
SAGELITE_GRAPHVIZ_BINDIR=/path/to/bin python -m build companion-packages/sagelite-graphviz-runtime
```

If `SAGELITE_GRAPHVIZ_BINDIR` is not set, the build checks `SAGE_LOCAL/bin`
and common system locations. For production wheels, build this package from the
same runtime environment used to validate the corresponding `sagelite` wheel.
