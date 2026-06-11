# sagelite-gap-package-ctbllib

Optional GAP CtblLib package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `ctbllib` package as package data so installed `sagelite`
environments can run doctests and character-table computations tagged
`gap_package_ctbllib` without requiring a traditional Sage prefix.

Build this package on a machine with CtblLib installed in a GAP root:

```bash
SAGELITE_GAP_CTBLLIB_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-ctbllib
```

If `SAGELITE_GAP_CTBLLIB_ROOT` is not set, the build checks `GAP_ROOT_PATHS` and
common GAP roots such as `/usr/share/gap`.
