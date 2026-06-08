# sagelite-csdp-runtime

Optional CSDP executable companion package for `sagelite`.

This package contains the redistributable CSDP `theta` command as standard
Python wheel package data. Installed `sagelite` wheels can use it to run CSDP
semidefinite programming doctests without requiring a separate Sage tree or
system package.

CSDP is distributed under the Common Public License 1.0, which Sage records as
not GPL-compatible. This companion package keeps that runtime in an explicit
optional wheel instead of bundling it into the core `sagelite` artifact.

Build the wheel from an environment where the Sage-built CSDP executable is
available. By default the build checks `SAGE_LOCAL/bin`, `/usr/bin`, and
`/usr/local/bin`; set `SAGELITE_CSDP_BINDIR` to choose a specific directory.
