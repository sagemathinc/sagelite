# sagelite-meataxe-runtime

Optional MeatAxe table companion package for `sagelite`.

Sage's MeatAxe extension links against the SharedMeatAxe library, but that
library expects finite-field multiplication tables in `MTXLIB`. Binary
`sagelite` wheels do not include Sage's build-prefix `share/meataxe` directory,
so installing this package in the same Python environment provides a
relocatable table directory.

This package is built by copying the generated MeatAxe table directory from an
existing Sage prefix:

```bash
SAGELITE_MEATAXE_DIR=/path/to/sage-local/share/meataxe \
python -m build companion-packages/sagelite-meataxe-runtime
```

If the table directory is not available but the `zcv` executable is, the build
can generate the tables:

```bash
SAGELITE_MEATAXE_ZCV=/path/to/sage-local/bin/zcv \
python -m build companion-packages/sagelite-meataxe-runtime
```

For production wheels, build this package from the same Sage prefix used to
build the corresponding `sagelite` wheel.
