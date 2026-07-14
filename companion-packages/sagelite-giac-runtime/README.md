# sagelite-giac-runtime

Optional GIAC executable companion package for `sagelite`.

Some Sage symbolic and interface doctests use the standalone `giac` command.
The base `sagelite` wheel does not bundle that executable, but installing this
package in the same Python environment provides a relocatable `giac` command.
The wheel also carries Giac's `aide_cas` database and points the executable to
it so Sage's command completion interface works outside the build prefix.

This package is built by copying `giac` and `share/giac/aide_cas` from an
existing Sage prefix. Set `SAGELITE_GIAC_BINDIR` and
`SAGELITE_GIAC_HELPFILE` if they are not on the default search paths.

```bash
python -m build companion-packages/sagelite-giac-runtime
```
