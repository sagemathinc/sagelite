# sagelite-gfan-runtime

Optional gfan executable companion package for `sagelite`.

Some Sage polynomial and Groebner fan functionality calls gfan command-line
tools such as `gfan`, `gfan_bases`, and `gfan_weightvector`. The `sagelite`
wheels do not include executable files from Sage's build prefix, so installing
this package in the same Python environment provides relocatable wrapper
scripts for Sage-built gfan binaries.

This package is built by copying the gfan executable from an existing Sage
prefix. Set `SAGELITE_GFAN_BINDIR` to the directory containing `gfan`:

```bash
SAGELITE_GFAN_BINDIR=/path/to/sage-local/bin \
python -m build companion-packages/sagelite-gfan-runtime
```

If `SAGELITE_GFAN_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations. For production wheels, build this package from the
same Sage prefix used to build the corresponding `sagelite` wheel.
