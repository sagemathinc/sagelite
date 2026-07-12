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

## Post12 coherent rebuild and gate

Committed source `2e9887be5df63851d6e5d747b0e886a2ea751404`
(`sagelite 10.9.post12`) bundles `libgomp` in the msolve companion and raises
its dependency floor to `10.9.post2`. The native exact-SHA run is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260711-214536-2e9887be5df
```

The build completed with exit code zero and produced this coherent set of
source-built repaired wheels:

```text
sagelite-10.9.post12-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=2fd18a87471b60ee3fc7319790902a5a068bf41176ce95e490ffe52f61af7ea6
size=227681950

sagelite_imagemagick_runtime-10.9.post2-py3-none-manylinux_2_28_aarch64.whl
sha256=6d12180f508b6b1b38fa9f3018e5367f4db359102e1cb1eaa00fc44a7820f0aa
size=21778153

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=4059cca2f788f7d9dd66b56af8a52125994a36dfe29783b1007d929f4e10e9e8
size=66578984

sagelite_msolve_runtime-10.9.post2-py3-none-manylinux_2_28_aarch64.whl
sha256=c95ba44172176a881ebabdb37f8ccd9448e41ab0395aa43e6ac4848ce8cf9be3
size=27423132
```

The strict repaired-wheelhouse gate installed
`sagelite[all-needed-extras]==10.9.post12` into a fresh venv using wheels only.
The install and `python -m pip check` passed. Every `sagelite-selftest` probe
passed, including the repaired ImageMagick, matching Maxima, and repaired
msolve runtimes. Packaged pytest reported 212 passed and 2 skipped.

The gate exited 1 because the installed doctest sweep found one failed module
out of 3,954. `sage.env.cython_aliases(required_modules=())` attempted to
probe the default optional LAPACK module with the Python `pkgconfig` package;
in the current minimal `python:3.13-slim-bookworm` validation image, the
`pkg-config` executable itself is absent, so `pkgconfig` raised `OSError`
rather than `PackageNotFoundError`. The reduced analysis classifies only this
`sage.env` runtime exception. Durable evidence is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260711-214536-2e9887be5df/validation/short-post12/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260711-214536-2e9887be5df/validation/short-post12/doctest-installed-linux-aarch64-cp313-post12-short-20260712-024820.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260711-214536-2e9887be5df/validation/short-post12/doctest-installed-linux-aarch64-cp313-post12-short-20260712-024820.selftest.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260711-214536-2e9887be5df/validation-short-command.log
```

The focused source correction treats an absent `pkg-config` command like a
missing package for optional modules and for the installed-runtime default
module set, while explicit required-module requests remain strict. It also
preserves the existing direct `-lz` fallback. The preview version advances to
`10.9.post13`; all 110 focused `src/sage/env_test.py` tests pass. A fresh
exact-SHA primary rebuild and clean short gate are required before this cell
can be marked full.

## Post13 exact-SHA rebuild and short gate

Committed source `23663717f78ed5c3ba34dbfb103f386c32177ea6`
(`sagelite 10.9.post13`) was rebuilt natively in the durable run:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-033749-23663717f78e
```

The repaired source-built wheel set is:

```text
sagelite-10.9.post13-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=6bee6ff8cb6c01f1408665772d9696b55150d73a32383d93b2a4a1165b582563

sagelite_imagemagick_runtime-10.9.post2-py3-none-manylinux_2_28_aarch64.whl
sha256=6d12180f508b6b1b38fa9f3018e5367f4db359102e1cb1eaa00fc44a7820f0aa

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=c1511938660c18ed6c22e16c0ed0d278252ed5cb9f582a5518e55a1b72eb8b98

sagelite_msolve_runtime-10.9.post2-py3-none-manylinux_2_28_aarch64.whl
sha256=c95ba44172176a881ebabdb37f8ccd9448e41ab0395aa43e6ac4848ce8cf9be3
```

The strict repaired-wheelhouse gate staged 177 wheels: one primary, 68
companions, and 108 third-party wheels, totaling 16,513,786,069 bytes. All
wheel filename, tag, dependency, and compatibility preflights passed. The
fresh wheel-only installation of `sagelite[all-needed-extras]==10.9.post13`,
`python -m pip check`, runtime manifest, and every `sagelite-selftest` probe
passed without adding `pkg-config` to the minimal validation image.

The installed `--optional=sage` short doctest sweep passed all 3,953 modules
with zero failed modules. Packaged pytest reported 213 passed and 2 skipped.
The authoritative artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-033749-23663717f78e/validation/short-post13/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-033749-23663717f78e/validation/short-post13/doctest-installed-linux-aarch64-cp313-post13-short-20260712-121820.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-033749-23663717f78e/validation/short-post13/doctest-installed-linux-aarch64-cp313-post13-short-20260712-121820.selftest.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-033749-23663717f78e/validation-short-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-033749-23663717f78e/validation-short-exit-code
```

The short-gate exit code is zero. A durable watcher started the fresh full
installed standard-suite validation from the same exact-SHA wheel contract at
`2026-07-12T13:11:48Z`; this cell remains below `full` until that process and
its reduced analysis both pass.

## Post13 full-run Graphviz failure

The durable full retry remained healthy and continued running under the native
aarch64 Docker container during the 2026-07-12 automation iteration. It
exposed deterministic `dot2tex`/Graphviz failures in
`sage.categories.loop_crystals` and `sage.combinat.posets.posets`. The
authoritative in-progress log is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-033749-23663717f78e/validation-full-command.log
```

Focused inspection showed that the Graphviz `post3` wheel archive recorded
every embedded wrapper and real executable with mode `0600`; pip consequently
installed `sagelite_graphviz/data/bin/dot` as non-executable. The generated
venv `dot` entry point was executable but failed with `PermissionError` when
it dispatched to that package-data wrapper. `sage.env` correctly declined to
add the non-executable companion directory to `PATH`, so `have_dot2tex()`
returned false and graph LaTeX behavior diverged from the installed optional
feature tags.

The focused source correction restores execute bits for both files during
Graphviz runtime discovery, raises the companion to `10.9.post4`, raises all
dependency floors, and advances Sagelite to `10.9.post14`. Its new mode
regression and focused companion metadata tests pass. The running `post13`
environment was not modified. A new exact-SHA primary/companion rebuild and
fresh strict gate are required; the current cell is not `full`.

The same in-progress sweep also emitted a resource-sensitive nested doctest
failure in `sage.doctest.forker` after a slow-test warning crossed the
five-second threshold. That is a separate failure class to reassess from the
completed reduced analysis or a focused rerun after the Graphviz iteration.

## Post14 rebuild start

The invalid `post13` full run completed its doctest phase with the known
Graphviz failures followed by cascading timeouts and resource failures. It
then stopped making progress during packaged pytest. The automation loop
terminated only that disposable Docker validation container; its durable
wrapper recorded exit code 137 and retained the log and validation artifacts.

The focused `post14` exact-SHA rebuild is running under a durable follow-on
process at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-142916-d691bc7cff61
```

Its metadata selects committed source
`d691bc7cff614078b7e62f6b4f128b003ea6feb6`, Sagelite `10.9.post14`, and the
native Linux `aarch64` CPython 3.13 CIBW contract. Before starting, the
follow-on removed only the superseded 41 GiB `post13` validation install; the
guest then had 119 GiB free, above the 100 GiB heavy-build threshold. At the
latest checkpoint the clean clone was still in progress, so wheel-build or
exact-checkout completion is not yet claimed. Top-level progress is in
`command.log`, and the durable wrappers will write `exit-code` and
`follow-on-exit-code`.

## Post14 build and corrected short-gate start

The exact-SHA native build completed with exit code zero and produced:

```text
sagelite-10.9.post14-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=da84ab601310bf0e7a9aa71752564294c5ec6d57c2a1db05c02f6dd13324d0d6
size=227682043

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=c74f07738d35774422b4e6bbb908d1c5f8e524cab641014ad7696e94342af4a6
size=66578984
```

The first validation watcher correctly rejected the inherited Graphviz
`post3` wheel against the primary's `>=10.9.post4` requirement. The focused
Graphviz wheel was then built from the same exact source checkout in the
native `manylinux_2_28_aarch64` image:

```text
sagelite_graphviz_runtime-10.9.post4-py3-none-manylinux_2_28_aarch64.whl
sha256=3e2542227a1fc84e0318f08371ac12ea6da9cfd3d2d7c1e7fe3774d127c8b6c8
size=20882212
```

A fresh `python:3.13-slim-bookworm` wheel-only smoke installed the companion,
restored the packaged `dot` execute bit, and generated SVG successfully with
`dot -Tsvg`. The corrected strict closure contains 177 wheels totaling
16,513,108,365 bytes and includes Graphviz `post4` rather than `post3`.

The durable strict short gate started at `2026-07-12T20:15:48Z` with the
required `--optional sage` setting. Its watcher PID is recorded in
`validation-retry-pid`, its controller log is `validation-follow.log`, and
the validator log is `validation-short-command.log`. It will start the full
installed sweep only after the fresh wheel-only short gate passes. This cell
remains below `full` while that validation is running.

## Post14 short-gate pass and full-run start

The corrected strict gate completed with exit code zero at
`2026-07-12T21:08:28Z`. It validated the exact-SHA 177-wheel closure totaling
16,513,108,365 bytes and identified by wheelhouse SHA256
`70ea3a99e49397a936f09c75d2c04f3f250f2556276c39bea9374935e7c486cf`.
The fresh wheel-only install of
`sagelite[all-needed-extras]==10.9.post14`, `python -m pip check`, runtime
manifest, and every `sagelite-selftest` probe passed, including the corrected
Graphviz runtime.

The installed `--optional=sage` short doctest sweep passed all 3,953 modules
with zero failed modules. Packaged pytest reported 213 passed and 2 skipped.
The authoritative short-gate artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-142916-d691bc7cff61/validation/short-post14/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-142916-d691bc7cff61/validation/short-post14/doctest-installed-linux-aarch64-cp313-post14-short-20260712-202021.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-142916-d691bc7cff61/validation/short-post14/doctest-installed-linux-aarch64-cp313-post14-short-20260712-202021.selftest.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-142916-d691bc7cff61/validation-short-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-142916-d691bc7cff61/validation-short-exit-code
```

The durable watcher started the full installed standard-suite run from the
same wheel contract at `2026-07-12T21:08:37Z`. Its validator log is
`validation-full-command.log`, and it will write `validation-full-exit-code`
when complete. This cell remains below `full` until both that exit code and
the completed reduced analysis pass.
