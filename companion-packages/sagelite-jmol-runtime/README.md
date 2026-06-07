# sagelite-jmol-runtime

Optional Jmol runtime-data companion package for `sagelite`.

This package contains Sage's `jmol` Java runtime files, installed as a Python
wheel. Installing it makes Sage's `JmolData.jar` feature detection and related
`# needs jmol` doctests work without requiring a traditional
`SAGE_LOCAL/share/jmol` installation.

This package is built by copying a Sage-compatible Jmol data directory. Set
`SAGELITE_JMOL_DIR` to the directory containing `JmolData.jar`:

```bash
SAGELITE_JMOL_DIR=/path/to/sage-local/share/jmol \
python -m build companion-packages/sagelite-jmol-runtime
```

If `SAGELITE_JMOL_DIR` is not set, the build checks `JMOL_DIR`,
`SAGE_SHARE/jmol`, `SAGE_LOCAL/share/jmol`, the local Sage prefix, and common
system locations.
