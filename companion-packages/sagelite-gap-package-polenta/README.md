# sagelite-gap-package-polenta

Optional GAP Polenta package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `polenta` package as package data so installed `sagelite`
environments can run doctests tagged `gap_package_polenta` without requiring a
traditional Sage prefix.

Build this package on a machine with Polenta installed in a GAP root:

```bash
SAGELITE_GAP_POLENTA_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-polenta
```

If `SAGELITE_GAP_POLENTA_ROOT` is not set, the build checks `GAP_ROOT_PATHS`
and common GAP roots such as `/usr/share/gap`.
