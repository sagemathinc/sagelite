# sagelite-mwrank-runtime

Optional mwrank executable companion package for `sagelite`.

Some Sage elliptic-curve interfaces and command-line tests use the `mwrank`
program from eclib. The `sagelite` wheels include Sage's Python and extension
modules, but not executable files from Sage's build prefix, so installing this
package in the same Python environment provides a relocatable `mwrank` command.

This package is built by copying `mwrank` from an existing Sage prefix. Set
`SAGELITE_MWRANK_BINDIR` to the directory containing `mwrank`:

```bash
SAGELITE_MWRANK_BINDIR=/path/to/sage-local/bin \
python -m build companion-packages/sagelite-mwrank-runtime
```

If `SAGELITE_MWRANK_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the
same Sage prefix used to build the corresponding `sagelite` wheel.
