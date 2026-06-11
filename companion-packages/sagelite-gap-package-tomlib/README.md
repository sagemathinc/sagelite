# sagelite-gap-package-tomlib

Optional GAP TomLib package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `tomlib` package as package data so installed `sagelite`
environments can run doctests and table-of-marks computations tagged
`gap_package_tomlib` without requiring a traditional Sage prefix.

Build this package on a machine with TomLib installed in a GAP root:

```bash
SAGELITE_GAP_TOMLIB_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-tomlib
```

If `SAGELITE_GAP_TOMLIB_ROOT` is not set, the build checks `GAP_ROOT_PATHS` and
common GAP roots such as `/usr/share/gap`.
