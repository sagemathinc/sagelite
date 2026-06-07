# sagelite-cddlib-runtime

Optional cddlib executable companion package for `sagelite`.

This package contains redistributable cddlib command-line tools as standard
Python wheel package data.  Installed `sagelite` wheels can use it to run cddlib
polyhedron doctests without requiring a separate Sage tree or system package.

Build the wheel from an environment where Sage-built cddlib executables are
available.  By default the build checks `SAGE_LOCAL/bin`, `/usr/bin`, and
`/usr/local/bin`; set `SAGELITE_CDDLIB_BINDIR` to choose a specific directory.
