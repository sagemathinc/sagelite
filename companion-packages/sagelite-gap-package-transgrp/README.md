# sagelite-gap-package-transgrp

Optional GAP TransGrp package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `transgrp` package as package data so installed
`sagelite` environments can run doctests and constructors using transitive
group libraries without requiring a traditional Sage prefix.

Build this package on a machine with TransGrp installed in a GAP root:

```bash
SAGELITE_GAP_TRANSGRP_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-transgrp
```

If `SAGELITE_GAP_TRANSGRP_ROOT` is not set, the build checks `GAP_ROOT_PATHS`
and common GAP roots such as `/usr/share/gap`.
