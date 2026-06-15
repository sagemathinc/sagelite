# sagelite-sirocco-runtime

Optional SIROCCO library companion package for `sagelite`.

Sage's `sage.libs.sirocco` extension links against `libsirocco` when that
optional extension is built. The base `sagelite` wheel does not provide a Sage
runtime prefix containing those library and header files. Installing this
companion package makes the redistributable SIROCCO runtime files available
from normal wheel package data.

Build this package from a system or Sage prefix that already has SIROCCO
installed:

```bash
SAGELITE_SIROCCO_PREFIX=/path/to/prefix python -m build companion-packages/sagelite-sirocco-runtime
```

If `SAGELITE_SIROCCO_PREFIX` is not set, the build checks `SAGE_LOCAL` and
common system locations.
