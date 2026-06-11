# sagelite-gap-package-atlasrep

Optional GAP AtlasRep package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `AtlasRep` package as package data so installed `sagelite`
environments can run doctests and constructors tagged `gap_package_atlasrep`
without requiring a traditional Sage prefix.

Build this package on a machine with AtlasRep installed in a GAP root:

```bash
SAGELITE_GAP_ATLASREP_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-atlasrep
```

If `SAGELITE_GAP_ATLASREP_ROOT` is not set, the build checks `GAP_ROOT_PATHS`
and common GAP roots such as `/usr/share/gap`.
