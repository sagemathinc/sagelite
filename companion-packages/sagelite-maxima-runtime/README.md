# sagelite-maxima-runtime

Optional Maxima runtime companion package for `sagelite`.

The `sagelite` wheels include the ECL-linked Sage interface to Maxima, but the
Maxima executable image, Lisp image, ECL runtime support files, and share tree
are separate runtime assets. Installing this package in the same Python
environment gives `sagelite` relocatable `MAXIMA`, `MAXIMA_PREFIX`, and
`MAXIMA_FAS` values, plus the matching `MAXIMA_IMAGESDIR` and `ECLDIR`,
without requiring users to set them manually. It also installs a `maxima`
console script that runs the bundled Maxima executable.

This package is built by copying an existing Sage-built Maxima runtime. Set
`SAGELITE_MAXIMA_PREFIX` to the versioned Maxima share directory and
`SAGELITE_MAXIMA_FAS` to the matching `maxima.fas`. The runtime helper reports
the bundled install root containing `share/maxima/<version>` as
`MAXIMA_PREFIX`, matching Maxima's autotools layout. Production Linux wheels
should also set `SAGELITE_MAXIMA_IMAGESDIR`, `SAGELITE_MAXIMA_ECLDIR`, and
`SAGELITE_MAXIMA_LIBDIR` from the same Sage prefix. When building a companion
for a repaired `sagelite` wheel, set `SAGELITE_MAXIMA_ECL_SONAME` to the
auditwheel-renamed ECL SONAME from that wheel so library mode uses the already
loaded ECL runtime instead of loading a second copy. Also set
`SAGELITE_MAXIMA_ECL_LIBRARY` to the extracted ECL shared library from that
repaired `sagelite` wheel so the build can reject Maxima images that need
symbols unavailable in library mode. The build patches both `maxima.fas` and
copied ECL support images such as `cmp.fas`:

```bash
SAGELITE_MAXIMA_PREFIX=/path/to/share/maxima/5.47.0 \
SAGELITE_MAXIMA_FAS=/path/to/lib/ecl/maxima.fas \
SAGELITE_MAXIMA_IMAGESDIR=/path/to/lib/maxima/5.47.0 \
SAGELITE_MAXIMA_ECLDIR=/path/to/lib/ecl-24.5.10 \
SAGELITE_MAXIMA_LIBDIR=/path/to/lib \
SAGELITE_MAXIMA_ECL_SONAME=libecl-<auditwheel-hash>.so.24.5.10 \
SAGELITE_MAXIMA_ECL_LIBRARY=/path/to/extracted/libecl-<auditwheel-hash>.so.24.5.10 \
python -m build companion-packages/sagelite-maxima-runtime
```

The build rejects ECL-loaded images that still depend on a generic
`libecl.so` SONAME unless `SAGELITE_MAXIMA_ECL_SONAME` is set. For a local
test build that intentionally targets the system ECL package instead of a
repaired `sagelite` wheel, set `SAGELITE_MAXIMA_ALLOW_SYSTEM_ECL=1` explicitly.

If the variables are not set, the build checks common Sage and system
locations, including Debian/Ubuntu's `maxima-sage` layout. For production
wheels, build this package from the same Sage prefix used to build the
corresponding `sagelite` wheel.

The bundled ECL support directory also contains `maxima.fas` and a small
`maxima.asd` descriptor. This lets ECL resolve plain `(require 'maxima)` from
the companion `ECLDIR`, which is useful when Sage falls back to ECL's standard
module lookup instead of passing `MAXIMA_FAS` explicitly.
