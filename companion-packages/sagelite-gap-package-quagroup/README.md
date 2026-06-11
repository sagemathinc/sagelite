# sagelite-gap-package-quagroup

Optional GAP QuaGroup package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `quagroup` package as package data so installed
`sagelite` environments can run doctests tagged `gap_package_quagroup` without
requiring a traditional Sage prefix.

Build this package on a machine with QuaGroup installed in a GAP root:

```bash
SAGELITE_GAP_QUAGROUP_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-quagroup
```

If `SAGELITE_GAP_QUAGROUP_ROOT` is not set, the build checks `GAP_ROOT_PATHS`
and common GAP roots such as `/usr/share/gap`.
