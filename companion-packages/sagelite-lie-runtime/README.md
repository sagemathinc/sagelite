# sagelite-lie-runtime

Optional LiE runtime companion package for `sagelite`.

Sage's LiE interface shells out to the `lie` command and reads LiE's `INFO.*`
help files from `LIE_INFO_DIR`. Binary `sagelite` wheels do not include the
traditional `SAGE_LOCAL/bin/lie` and `SAGE_LOCAL/lib/LiE` installation, so
installing this package in the same Python environment provides a relocatable
command and info directory.

Build this package from a Sage prefix that already has LiE installed:

```bash
SAGELITE_LIE_BINDIR=/path/to/sage-local/bin \
SAGELITE_LIE_INFO_DIR=/path/to/sage-local/lib/LiE \
python -m build companion-packages/sagelite-lie-runtime
```

If the variables are not set, the build checks `SAGE_LOCAL/bin`,
`SAGE_LOCAL/lib/LiE`, and common system locations. For production wheels, build
this package from the same Sage prefix used to build the corresponding
`sagelite` wheel.
