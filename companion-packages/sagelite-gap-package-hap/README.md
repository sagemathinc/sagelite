# sagelite-gap-package-hap

Optional GAP HAP package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `hap` and `hapcryst` packages as package data so installed
`sagelite` environments can run doctests tagged `gap_package_hap` without
requiring a traditional Sage prefix.

Build this package on a machine with HAP installed in a GAP root:

```bash
SAGELITE_GAP_HAP_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-hap
```

If `SAGELITE_GAP_HAP_ROOT` is not set, the build checks `GAP_ROOT_PATHS` and
common GAP roots such as `/usr/share/gap`.
