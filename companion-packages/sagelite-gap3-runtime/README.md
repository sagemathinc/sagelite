# sagelite-gap3-runtime

Optional GAP3 runtime companion package for `sagelite`.

The `sagelite` wheel does not bundle Sage's GAP3 installation. This companion
package packages a Sage-built GAP3 tree and exposes a `gap3` console script, so
doctests and features marked `optional - gap3` can run in installed-wheel
environments.

Build it from a Sage prefix that has `gap3` installed:

```bash
SAGELITE_GAP3_ROOT=/path/to/sage-local/gap3/latest/gap3 \
  python -m build companion-packages/sagelite-gap3-runtime
```

If `SAGELITE_GAP3_ROOT` is not set, the build checks `SAGE_LOCAL/gap3/latest/gap3`.
