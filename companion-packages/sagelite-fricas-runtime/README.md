# sagelite-fricas-runtime

Optional FriCAS executable companion package for `sagelite`.

Sage's FriCAS interface shells out to the standalone `fricas` program. The
`sagelite` wheels include Sage's Python and extension runtime but do not bundle
this optional executable in the base wheel. Installing this package in the same
Python environment provides a relocatable `fricas` command.

This package is built by copying FriCAS from an existing Sage installation or
system package into wheel package data.

```bash
python -m build companion-packages/sagelite-fricas-runtime
```
