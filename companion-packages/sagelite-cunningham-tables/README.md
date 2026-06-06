# sagelite-cunningham-tables

Optional Cunningham tables companion package for `sagelite`.

This package contains the `cunningham_tables` payload from SageMath 10.9,
installed as a Python wheel. Installing it makes Sage's
`cunningham_tables` optional doctests and `cunningham_prime_factors()`
available without making the data a hard dependency of `sagelite`.

To build manually from a Sage source checkout:

```sh
python -m build companion-packages/sagelite-cunningham-tables
```

Set `SAGELITE_CUNNINGHAM_MAIN_GZ` to override the source `main.gz` file.
