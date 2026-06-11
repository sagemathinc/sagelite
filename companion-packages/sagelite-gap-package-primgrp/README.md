# sagelite-gap-package-primgrp

Optional GAP PrimGrp package companion wheel for `sagelite`.

The `sagelite-gap-runtime` wheel supplies the GAP core runtime. This companion
wheel supplies GAP's `primgrp` package as package data so installed `sagelite`
environments can run doctests and primitive-group computations tagged
`gap_package_primgrp` without requiring a traditional Sage prefix.

Build this package on a machine with PrimGrp installed in a GAP root:

```bash
SAGELITE_GAP_PRIMGRP_ROOT=/usr/share/gap python -m build companion-packages/sagelite-gap-package-primgrp
```

If `SAGELITE_GAP_PRIMGRP_ROOT` is not set, the build checks `GAP_ROOT_PATHS` and
common GAP roots such as `/usr/share/gap`.
