# sagelite-pari-runtime

Optional PARI/GP executable companion package for `sagelite`.

This package is built from a Sage or system PARI/GP installation and bundles
the `gp`, `gphelp`, and `tex2mail` commands with the runtime libraries needed
to execute them from an installed `sagelite` wheel.

Build from a Sage prefix by pointing `SAGELITE_PARI_BINDIR` at the directory
containing `gp`:

```bash
SAGELITE_PARI_BINDIR=/path/to/sage-local/bin \
python -m build --wheel companion-packages/sagelite-pari-runtime
```

If `SAGELITE_PARI_BINDIR` is not set, the build checks `SAGE_LOCAL/bin` and
common system locations.
