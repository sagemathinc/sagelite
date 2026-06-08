# sagelite-frobby-runtime

Optional Frobby executable companion package for `sagelite`.

Sage's monomial-ideal interface shells out to the standalone `frobby`
program. The `sagelite` wheels include Sage's Python and extension runtime but
do not bundle this optional executable in the base wheel. Installing this
package in the same Python environment provides a relocatable `frobby` command.

This package is built by copying `frobby` from an existing Sage installation or
system package into wheel package data.

```bash
python -m build companion-packages/sagelite-frobby-runtime
```
