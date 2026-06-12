# sagelite-imagemagick-runtime

Optional ImageMagick runtime companion package for `sagelite`.

This package supplies relocatable `magick` and `convert` commands for installed
wheel environments that do not have ImageMagick on `PATH`.  It is intended for
Sage features and doctests that render or convert images through ImageMagick.

Build from a Sage or system installation with:

```sh
SAGELITE_IMAGEMAGICK_BINDIR=/path/to/bin python -m build --wheel
```
