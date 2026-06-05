# sagelite-database-graphs

Optional graph database companion package for `sagelite`.

The `sagelite` wheels include Sage's graph database interfaces, but not the
graph database payload. Installing this package in the same Python environment
contributes the bundled `graphs` data directory through Sage's
`sagemath.data_paths` entry point mechanism.

This package includes the standard Sage graph database files from the `graphs`
SPKG:

- `graphs.db`
- `brouwer_srg_database.json`
- `isgci_sage.xml`
- `smallgraphs.txt`
