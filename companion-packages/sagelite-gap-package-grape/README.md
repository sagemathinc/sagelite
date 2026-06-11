# sagelite-gap-package-grape

Optional GAP GRAPE package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `grape` package as package data so installed `sagelite`
environments can run doctests and graph constructors tagged
`gap_package_grape` without requiring a traditional Sage prefix.

Build this package on a machine with GRAPE installed in a GAP root:

```bash
SAGELITE_GAP_GRAPE_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-grape
```

If `SAGELITE_GAP_GRAPE_ROOT` is not set, the build checks `GAP_ROOT_PATHS` and
common GAP roots such as `/usr/share/gap`.
