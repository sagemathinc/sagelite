# sagelite-latte-runtime

Optional LattE integrale executable companion package for `sagelite`.

This package is intended for wheel builds of Sage where the core `sagelite`
wheel should not bundle every optional standalone executable.  It copies the
`count` and `integrate` programs, plus selected shared-library dependencies,
into package data and exposes them through standard console scripts.

Sage discovers the installed package lazily at runtime, so installing this
package enables features guarded by the `latte_int` optional tag without making
LattE a hard dependency of the base `sagelite` wheel.
