# sagelite-gap-package-guava

Optional GAP GUAVA package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `guava` package, along with its required `sonata`
dependency, as package data so installed `sagelite` environments can run
doctests and coding theory routines tagged
`gap_package_guava` without requiring a traditional Sage prefix.

Build this package on a machine with GUAVA installed in a GAP root:

```bash
SAGELITE_GAP_GUAVA_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-guava
```

If `SAGELITE_GAP_GUAVA_ROOT` is not set, the build checks `GAP_ROOT_PATHS` and
common GAP roots such as `/usr/share/gap`.
