# Sagelite Linux aarch64 CPython 3.13 Validation

This report records the native Linux aarch64 CPython 3.13 iteration started
from committed source `0701265d12d8bbb55a3df941744eac6810bb2a93`
(`sagelite 10.9.post10`). The build and validation environment was the
`sagelite-linux-arm64` Lima VM on `m1`, which reported Linux `aarch64` and ran
Docker as `linux/arm64`.

The durable run root is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260711-004636-0701265d12d
```

## Build result

The repaired primary wheel built successfully:

```text
sagelite-10.9.post10-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=2f2d36e3f250af5abcb4078ff4b168d04ca622d3201142642b2ee5a7255ccc78
size=227681879
```

The top-level build log and durable exit code are `command.log` and
`exit-code` in the run root. The build exit code is zero.

Binary-only dependency resolution initially found two missing wheels. Native
repaired CPython 3.13 aarch64 wheels were built for `pycosat 0.6.6` and
`cysignals 1.12.6`. The latter matches the version used to compile the primary
wheel. A platform-independent `sagelite-database-polytopes-4d 10.9` wheel was
also built from the checksummed Sage SPKG:

```text
sagelite_database_polytopes_4d-10.9-py3-none-any.whl
sha256=c26737fe93da35eb604f4b3242631c237dbd51244b16bf97ffd60945e7f4e149
size=11603603373
```

The resulting per-cell `validation-wheelhouse` contains 179 wheels and has
`SHA256SUMS` plus `inventory.txt`. Binary-only closure completed with exit code
zero under `dependency-closure/`.

## Validation result

The strict repaired-wheelhouse run used:

```text
--package sagelite[all-needed-extras]==10.9.post10
--strict-repaired-wheelhouse-preflight
--optional sage
--short 600
--nthreads 8
```

The fresh wheel-only install and `python -m pip check` passed. Its artifacts
are under `validation/short-post10-2`, and the durable command log and exit code
are under `short-validation-2/`.

The first short gate failed because PyPI supplied `cysignals 1.12.5`, while
the primary wheel and vendored `cypari2` had compiled against `1.12.6` and
required the exported C function `_do_raise_exception`. Replacing it in the
focused failed venv with the repaired `1.12.6` wheel fixed Sage arithmetic,
`cypari2`, the required native imports, and the database probes.

That focused rerun exposed a separate Maxima runtime ABI mismatch. Loading
the public `sagelite-maxima-runtime 10.9.post14` `sockets.fas` into the ECL
runtime linked by this CPython 3.13 primary wheel aborts with an invalid-memory
access. The Maxima companion documentation requires building its ECL images
from the same Sage prefix as the corresponding primary wheel, but the Linux
repair helper built this companion only for CPython 3.12.

The follow-up source change removes that CPython 3.12-only guard, assigns
`sagelite 10.9.post11` and Maxima runtime `10.9.post15`, and raises all Maxima
runtime dependency floors. A fresh CPython 3.13 primary/companion rebuild is
required before the short gate can be rerun. No public artifacts were
published in this iteration.

The first exact-SHA `post11` rebuild attempt is preserved at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260711-153620-633637de44f
```

It exited before wheel creation because the persistent compiled prefix's
cached `config.status` still embedded `vers_sagelib = 10.9.post10`. Replaying
that file made `make` request `sagelib-10.9.post10` from the `post11` source,
which `sage-spkg` correctly rejected. The Linux before-all helper now compares
the cached configuration's embedded Sage version with `VERSION.txt` and
reconfigures when they differ. This preserves reusable compiled dependencies
without carrying release-version metadata into the next preview build.

## Post11 rebuild and short-gate result

The corrected exact-SHA rebuild from committed source
`07a8f627683c4ca7229c626a75c8a75d1bb13178` completed at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260711-162439-07a8f627683c
```

It produced these repaired wheels with build exit code zero:

```text
sagelite-10.9.post11-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=4adfddd72adb13628a11ecd745458092241c6fa211961427d3dddfaccf56850b
size=227681874

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=d0b05e3f8af81eb3ddfa5f944b9bbedabebacdb5a5965e66a2704b334b00f4fc
size=66578984
```

The strict repaired-wheelhouse short run staged 177 wheels totaling
16,502,009,111 bytes. A fresh wheel-only install of
`sagelite[all-needed-extras]==10.9.post11` and `python -m pip check` passed.
The matching Maxima `post15` runtime passed the selftest probe. The installed
standard doctest run reported all 3,953 modules passed with zero failed
modules, and the packaged pytest run reported 212 passed and 2 skipped.

The validator nevertheless exited 1 because `sagelite-selftest` found two
other companion-runtime defects: the ImageMagick `post1` wheel could not load
its PNG coder dependencies, and the msolve executable help output was not
recognized. The durable artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260711-162439-07a8f627683c/validation/short-post11/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260711-162439-07a8f627683c/validation/short-post11/doctest-installed-linux-aarch64-cp313-post11-short-20260711-203137.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260711-162439-07a8f627683c/validation/short-post11/doctest-installed-linux-aarch64-cp313-post11-short-20260711-203137.selftest.log
```

## ImageMagick companion fix

Commit `8c540d167ab0f7e6b4ab69c57f9615e5ba4f0e06` adds the missing global
ImageMagick configuration, discovers Debian multiarch module directories, and
bundles the transitive library closure of coder and filter modules. It raises
the companion to `10.9.post2` and adds a PPM-to-PNG-to-GIF regression smoke.
The native aarch64 wheel build and fresh standalone smoke passed at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-imagemagick-20260711-212222-8c540d167ab0
```

The wheel is:

```text
sagelite_imagemagick_runtime-10.9.post2-py3-none-manylinux_2_28_aarch64.whl
sha256=6d12180f508b6b1b38fa9f3018e5367f4db359102e1cb1eaa00fc44a7820f0aa
size=21778153
```

Replacing only ImageMagick `post1` with this wheel in the preserved installed
environment made the exact `_check_imagemagick_runtime` selftest probe pass.
That focused modified-venv rerun is regression evidence, not final acceptance.
The next iteration should address the independent msolve probe and then create
one fresh, coherent exact-SHA primary/companion wheelhouse before rerunning the
short gate.
