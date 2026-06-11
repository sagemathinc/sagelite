# sagelite-gap-package-polycyclic

Optional GAP Polycyclic package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `polycyclic` package, along with its required `alnuth` and
`autpgrp` dependencies, as package data so installed `sagelite` environments can
run doctests and group-theory routines tagged `gap_package_polycyclic` without
requiring a traditional Sage prefix.

Build this package on a machine with Polycyclic installed in a GAP root:

```bash
SAGELITE_GAP_POLYCYCLIC_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-polycyclic
```

If `SAGELITE_GAP_POLYCYCLIC_ROOT` is not set, the build checks
`GAP_ROOT_PATHS` and common GAP roots such as `/usr/share/gap`.
