# sagelite-kenzo-runtime

Optional Kenzo ECL image companion package for `sagelite`.

Sage's Kenzo interface loads a compiled ECL image, `kenzo.fas`. Binary
`sagelite` wheels do not include Sage's build-prefix `lib/ecl/kenzo.fas`, so
installing this package in the same Python environment provides a relocatable
image path.

Build this package by copying the generated Kenzo image from an existing Sage
prefix:

```bash
SAGELITE_KENZO_FAS=/path/to/sage-local/lib/ecl/kenzo.fas \
python -m build companion-packages/sagelite-kenzo-runtime
```

If `SAGELITE_KENZO_FAS` is not set, the build checks `KENZO_FAS`,
`SAGE_LOCAL/lib/ecl/kenzo.fas`, and common system ECL locations.

For production wheels, build this package from the same Sage prefix used to
build the corresponding `sagelite` wheel.
