# sagelite-gap-package-repsn

Optional GAP Repsn package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `repsn` package as package data so installed `sagelite`
environments can use representation-theory routines from the Sage
`gap_packages` SPKG without requiring a traditional Sage prefix.

Build this package on a machine with Repsn installed in a GAP root:

```bash
SAGELITE_GAP_REPSN_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-repsn
```

If `SAGELITE_GAP_REPSN_ROOT` is not set, the build checks `GAP_ROOT_PATHS` and
common GAP roots such as `/usr/share/gap`.
