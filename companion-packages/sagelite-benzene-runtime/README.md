# sagelite-benzene-runtime

Optional benzene executable companion package for `sagelite`.

Some Sage graph generator features call the standalone `benzene` program for
fusenes and benzenoids. The `sagelite` wheels include Sage's Python and
extension runtime but do not bundle this executable in the base wheel. Installing
this package in the same Python environment provides a relocatable `benzene`
command.

This package is built by copying `benzene` from an existing Sage installation or
system package into wheel package data.

```bash
python -m build companion-packages/sagelite-benzene-runtime
```
