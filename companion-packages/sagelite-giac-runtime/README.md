# sagelite-giac-runtime

Optional GIAC executable companion package for `sagelite`.

Some Sage symbolic and interface doctests use the standalone `giac` command.
The base `sagelite` wheel does not bundle that executable, but installing this
package in the same Python environment provides a relocatable `giac` command.

This package is built by copying `giac` from an existing Sage prefix. Set
`SAGELITE_GIAC_BINDIR` if the executable is not on the default search path.

```bash
python -m build companion-packages/sagelite-giac-runtime
```
