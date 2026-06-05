# sagelite-database-jones-numfield

Optional Jones number field database companion package for `sagelite`.

The `sagelite` wheels include Sage's Jones database interface, but not the
database payload. Installing this package in the same Python environment
contributes the bundled `jones` data directory through Sage's
`sagemath.data_paths` entry point mechanism.

This package contains the `jones.sobj` payload from Sage's
`database_jones_numfield` SPKG.
