# sagelite-qepcad-runtime

Optional QEPCAD executable companion package for `sagelite`.

This package contains the redistributable Sage-built QEPCAD runtime layout as
standard Python wheel package data. Installed `sagelite` wheels can use it for
the `sage.interfaces.qepcad` optional doctests without requiring a full
`SAGE_LOCAL` tree.

QEPCAD is distributed under the ISC license.

Build the wheel from an environment where the Sage-built QEPCAD package is
installed. By default the build checks `SAGELITE_QEPCAD_ROOT`, `QEPCAD_ROOT`,
`SAGE_LOCAL`, `/usr`, and `/usr/local`; set `SAGELITE_QEPCAD_ROOT` to choose a
specific root.

```bash
SAGELITE_QEPCAD_ROOT=/path/to/sage/local \
  python -m build companion-packages/sagelite-qepcad-runtime
```
