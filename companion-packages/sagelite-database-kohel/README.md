# sagelite-database-kohel

Optional Kohel modular and Hilbert polynomial database companion package for
`sagelite`.

The `sagelite` wheels include Sage's Kohel database interfaces, but not the
database payload. Installing this package in the same Python environment
contributes the bundled `kohel` data directory through Sage's
`sagemath.data_paths` entry point mechanism.

This package contains the Sage `database_kohel` SPKG payload, including the
`PolMod` modular polynomial tables and `PolHeeg` Hilbert class polynomial
tables.
