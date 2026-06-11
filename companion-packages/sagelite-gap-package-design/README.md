# sagelite-gap-package-design

Optional GAP DESIGN package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `design` package as package data so installed `sagelite`
environments can run doctests and graph constructors tagged
`gap_package_design` without requiring a traditional Sage prefix.

Build this package on a machine with DESIGN installed in a GAP root:

```bash
SAGELITE_GAP_DESIGN_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-design
```

If `SAGELITE_GAP_DESIGN_ROOT` is not set, the build checks `GAP_ROOT_PATHS` and
common GAP roots such as `/usr/share/gap`.
