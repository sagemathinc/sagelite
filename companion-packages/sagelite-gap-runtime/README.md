# sagelite-gap-runtime

Optional GAP runtime companion package for `sagelite`.

The `sagelite` wheels include the `libgap` shared library but do not include
GAP's runtime tree.  GAP needs files such as `lib/init.g` to initialize
correctly.  Installing this package in the same Python environment gives
`sagelite` a relocatable GAP root without requiring users to set
`GAP_ROOT_PATHS`.

This package is built by copying an existing GAP root into the wheel.  Set
`SAGELITE_GAP_ROOT` to the root that contains `lib/init.g`:

```bash
SAGELITE_GAP_ROOT=/path/to/gap python -m build companion-packages/sagelite-gap-runtime
```

If `SAGELITE_GAP_ROOT` is not set, the build also checks entries in
`GAP_ROOT_PATHS` and common system locations such as `/usr/share/gap`.

To test installation directly from GitHub on a machine with a compatible GAP
runtime installed:

```bash
pip install "git+https://github.com/sagemathinc/sagelite.git@develop#subdirectory=companion-packages/sagelite-gap-runtime"
```

For production wheels, build this package from the same Sage-built GAP prefix
used to build the corresponding `sagelite` wheel.
