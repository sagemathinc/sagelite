# sagelite-ecl-runtime

Optional ECL executable companion package for `sagelite`.

The `sagelite` wheels include Sage's ECL-linked extension modules, but not a
standalone `ecl` command from a Sage build prefix. Installing this package in
the same Python environment provides relocatable `ecl` and `ecl-config`
commands for command-line doctests and build helpers that expect ECL tooling.

This package is built by copying ECL from an existing prefix. Set
`SAGELITE_ECL_PREFIX` to the prefix containing `bin/ecl`, `bin/ecl-config`,
`include/ecl`, and `lib/ecl-*`:

```bash
SAGELITE_ECL_PREFIX=/path/to/sage-local \
python -m build companion-packages/sagelite-ecl-runtime
```

If `SAGELITE_ECL_PREFIX` is not set, the build checks `SAGE_LOCAL` and common
system prefixes. For production wheels, build this package from the same Sage
prefix used to build the corresponding `sagelite` wheel.
