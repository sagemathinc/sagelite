# sagelite-gap-package-gapdoc

Optional GAP GapDoc package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `GapDoc` package as package data so installed `sagelite`
environments can load GAP packages that depend on GapDoc without requiring a
traditional Sage prefix.

Build this package on a machine with GapDoc installed in a GAP root:

```bash
SAGELITE_GAP_GAPDOC_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-gapdoc
```

If `SAGELITE_GAP_GAPDOC_ROOT` is not set, the build checks `GAP_ROOT_PATHS` and
common GAP roots such as `/usr/share/gap`.
