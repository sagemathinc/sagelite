# sagelite-topcom-runtime

Optional TOPCOM executable companion package for `sagelite`.

Some Sage triangulation functionality calls TOPCOM command-line tools such as
`points2placingtriang` and `points2allfinetriangs`. The `sagelite` wheels do
not include executable files from Sage's build prefix, so installing this
package in the same Python environment provides relocatable wrapper scripts for
Sage-built TOPCOM binaries.

This package is built by copying the TOPCOM executables from an existing Sage
prefix. Set `SAGELITE_TOPCOM_BINDIR` to the directory containing
`points2placingtriang` and `points2allfinetriangs`:

```bash
SAGELITE_TOPCOM_BINDIR=/path/to/sage-local/bin \
python -m build companion-packages/sagelite-topcom-runtime
```

If `SAGELITE_TOPCOM_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the same
Sage prefix used to build the corresponding `sagelite` wheel.
