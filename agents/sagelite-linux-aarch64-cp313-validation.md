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

## Post14 full-run Giac failure

The native `post14` full run remained healthy and active, but reproduced a
deterministic failure in `sage.calculus.calculus`: the bundled
`sagelite-giac-runtime 10.9` contains Giac 1.9.0.15p0, which leaves
`laplace(t^n, t, s)` as a formal unevaluated transform. The Sage doctest had
been changed upstream to require the computed
`s^(-n - 1)*gamma(n + 1)` result introduced by Giac 2.0.0.19. Sage's own Giac
SPKG recipe still selects 1.9.0.15p0, so this version split also affects a
Sage-distributed optional Giac build rather than being specific to aarch64.

Commit `65605f1570ba9523c86ea4b3292433e93e879ce5` makes the regression exact for
both runtime generations: Giac 1.9 must return the formal transform, while
newer Giac must return the computed expression. The focused assertion passed
inside the fresh `post14` wheel-only validation container against the actual
companion runtime. The change advances Sagelite to `10.9.post15`.

The in-progress `post14` full run is retained to collect its complete reduced
analysis, but it cannot certify the cell after this source change. A new
exact-SHA primary rebuild, strict short gate, and full run are required from
the `post15` commit. The current authoritative in-progress log remains:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-142916-d691bc7cff61/validation-full-command.log
```

## Post15 durable follow-on start

The canonical controller was clean and synchronized with `origin/develop` at
committed source `9f1fa2c9e5555e435cbd541f3bca878add8874ba`
(`sagelite 10.9.post15`). The public preview Sagelite project page still
listed only the existing `post8` and `post9` primaries; no local aarch64
CPython 3.13 artifact was assumed to be published.

At preflight, `m1` reported macOS `arm64` with 185 GiB free on
`/Volumes/sage`. Its Lima guest reported Linux `aarch64`; the guest had
105,359,421,440 bytes free while the retained `post14` full validation was
using its disposable install. The full-validation container and durable
wrapper were both alive, the validator log was growing, and the container was
actively using CPU. No duplicate validation or heavy build was started.

A durable exact-SHA follow-on is staged at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-215857-9f1fa2c9e55
```

Its build watcher PID is recorded in `follow-on-pid`, and its validation
watcher PID is recorded in `validation-watcher-pid`. The follow-on waits for
the existing `post14` full run to write its exit code, preserves its
wheelhouse, summaries, reduced analysis, metadata, and logs, and removes only
the completed run's disposable install. It then rechecks the 100 GiB heavy
build threshold before cloning and building the exact `post15` SHA. After a
successful build, the validation watcher assembles a fresh strict closure,
runs the required wheel-only `--optional sage --short 600` gate, and starts
the full gate only if the short gate passes. Top-level progress is in
`follow-on.log`, `command.log`, and `validation-follow.log`; the phase logs
and exit-code artifacts use the same names as the preceding exact-SHA runs.

At launch, the durable PIDs were alive and both watcher logs recorded their
start at `2026-07-12T22:00:49Z`. This cell remains below `full` until the new
wheel build, strict short gate, and complete reduced full analysis all pass.

## Post15 watcher recovery

The first two `post15` watcher processes appeared to have been reaped when
their launching SSH session ended. They left neither phase output nor
exit-code artifacts, and the `post14` full-validation container remained
healthy, so no build or validation work was duplicated. At
`2026-07-12T22:19:00Z`, the same preserved scripts were relaunched as
transient user-systemd services in the Lima guest:

```text
sagelite-post15-follow.service   MainPID=1252476
sagelite-post15-validate.service MainPID=1252514
```

The guest user has lingering enabled, and both services were active in their
own user-manager cgroups after the launching session exited. The follow-on is
still waiting for the invalidated `post14` sweep to finish; that Docker
container, its validator, and its doctest workers were active, and
`validation-full-command.log` was still growing. The guest had about 95 GiB
free while retaining the disposable `post14` install, below the heavy-build
threshold. The follow-on will remove only that install after the old validator
writes `validation-full-exit-code`, then recheck the 100 GiB threshold before
starting the exact-SHA `post15` build.

The public project page was also rechecked with a pip user agent and continued
to list seven `post8` and seven `post9` primary wheels; no `post15` artifact is
public. This recovery changes orchestration evidence only. The cell remains
below `full`.

A subsequent process-tree reconciliation found that the original watcher
shells had actually survived as PID-1 orphans, each waiting on a `sleep 60`
child. They had not reached any build or validation phase, but leaving them
alive would have allowed duplicate work after the `post14` exit-code artifact
appeared. The two orphan watcher trees were terminated at approximately
`2026-07-12T22:22Z`; the active `post14` validation container and the two
systemd-owned watcher processes were left untouched. A post-cleanup check
showed exactly the intended watcher pair, with main PIDs `1252476` and
`1252514`, both active under the guest user manager. The `post14` validator
was still running and its log was still advancing through the installed
doctest sweep. The guest had about 94 GiB free while retaining that disposable
install, and the macOS host had about 181 GiB free on `/Volumes/sage`.

The public `dev/manifest.json` was fetched again with a pip user agent and
contained 177 wheel entries. Its fourteen Sagelite primary entries were the
seven `post8` and seven `post9` wheels; there was still no public `post15`
primary. No publication was attempted.

The orphan termination traps had written `follow-on-exit-code`,
`follow-on-finished-at`, `validation-follow-exit-code`,
`validation-follow-finished-at`, and `disk-after-validation.txt` into the
shared `post15` run root after the systemd-owned replacements had started.
Those stale completion markers did not affect either replacement script: the
build watcher waits on the `post14` full-run exit code, and the validation
watcher waits on the new run's build `exit-code`. They could nevertheless
mislead a later reconciliation, so only those five orphan-written files were
removed. Both intended services remained active afterward. At approximately
`2026-07-12T22:31Z`, the `post14` validator and doctest workers were still
CPU-active, its validator log was still growing, the Linux guest had
100,509,392,896 bytes free, and `/Volumes/sage` had about 181 GiB free. The
public manifest still contained 177 wheels, fourteen Sagelite primaries, and
no `post15` primary.

## Post14 in-progress failure inventory

At approximately `2026-07-12T22:56Z`, the invalidated `post14` full sweep was
still healthy and advancing through `sage.rings`. Its validator, dispatcher,
and eight-worker doctest tree were CPU-active, the log was growing, and no
`validation-full-exit-code` existed. Exactly the intended two `post15`
user-systemd services remained active and waiting; no duplicate build or
validation container had started. The Linux guest had about 97 GiB free and
the macOS host had about 183 GiB free on `/Volumes/sage`, so the build watcher
correctly remained below the 100 GiB heavy-build threshold until it can remove
the completed `post14` install.

A provisional reduction of the still-growing log was saved on the controller
at:

```text
/scratch/sagelite-automation/reconcile-20260712-2256/post14-in-progress.analysis.md
/scratch/sagelite-automation/reconcile-20260712-2256/post14-in-progress.analysis.json
```

Because the doctest stats and final footer do not exist until the sweep
finishes, its nine current failed-module buckets are triage leads rather than
final counts. In addition to the already-fixed Giac Laplace result, the log
shows independent failures involving the `flatter` executable, fpylll strategy
data, compiler-dependent doctests in the minimal installed image, GAP3 and
Giac 1.9 protocol output, and the known resource-sensitive nested dispatcher
test. These are preserved for later coherent iterations; they do not broaden
or invalidate the current Giac-focused `post15` rebuild. The public manifest
still contained 177 wheels and the public Sagelite page still listed only the
seven `post8` and seven `post9` primaries.

## Post14 completion and post15 strict-gate start

The invalidated `post14` full sweep completed at `2026-07-12T23:35:55Z`
and wrote validator exit code 21. Its final reduced analysis reports 28 failed
modules out of 3,958: 13 performance/resource timeouts, 12
`core-supported` failures, two `optional-external` failures, and one
`optional-data` failure. The completed artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-142916-d691bc7cff61/validation/full-post14/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-142916-d691bc7cff61/validation/full-post14/doctest-installed-linux-aarch64-cp313-post14-full-20260712-211422.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-142916-d691bc7cff61/validation/full-post14/doctest-installed-linux-aarch64-cp313-post14-full-20260712-211422.analysis.json
```

The intended systemd-owned `post15` follow-on then removed only the completed
run's disposable install and built committed source
`9f1fa2c9e5555e435cbd541f3bca878add8874ba` successfully. The build finished
at `2026-07-13T04:13:27Z` and produced these repaired native wheels:

```text
sagelite-10.9.post15-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=a3a5ac0b6e3c7d8e334c16557ae39df59103b83cda0189e66e56a64166ca1b01
size=227682129

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=74d038b255f97e393888c03a023fa0d2be3783573650bd5a845feddda9c567f8
size=66578984
```

The exact checkout is clean and matches the recorded SHA. The validation
watcher assembled a strict closure of 177 wheels totaling 16,513,108,451
bytes; its `SHA256SUMS` file hashes to
`09f66a5c2b8f8cb43199456c04d7c9bd34a2bf1720288a07157eedc9e525cc00`.
A fresh `python:3.13-slim-bookworm` short gate started at
`2026-07-13T04:15:02Z` with the required wheel-only
`sagelite[all-needed-extras]==10.9.post15`, strict repaired-wheelhouse
preflight, `--optional sage`, `--short 600`, and eight threads. At the latest
checkpoint the container was alive, installing from the local wheelhouse, and
the guest had 123,775,545,344 bytes free. The same durable watcher will remove
the short install and start the full gate only if the short gate passes.

The authoritative new run root is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-215857-9f1fa2c9e55
```

The public `dev/manifest.json` remains unchanged at 177 wheel entries, and
the public Sagelite page still lists only seven `post8` and seven `post9`
primary wheels. No publication was attempted. The cell remains below `full`.

## Post15 strict-gate runtime checkpoint

The durable validation service remains active and owns the only `post15`
validation container. The exact remote checkout is clean at
`9f1fa2c9e5555e435cbd541f3bca878add8874ba`, and the completed build and
follow-on exit codes are both zero. No short- or full-validation exit code has
yet been written.

The strict preflight accepted all 177 staged wheels: one repaired primary, 68
companions, and 108 compatible third-party wheels totaling 16,513,108,451
bytes. The fresh wheel-only installation of
`sagelite[all-needed-extras]==10.9.post15` passed, as did `python -m pip
check`. The runtime manifest and summary completed, and every
`sagelite-selftest` probe passed, including Maxima, Graphviz, ImageMagick,
flatter, fpylll data, msolve, and the standard companion databases.

The installed `--optional=sage` short sweep began doctesting all 3,953 modules
with eight native arm64 workers and was still healthy and advancing at this
checkpoint. Its active command log is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-215857-9f1fa2c9e55/validation-short-command.log
```

The Linux guest reported 102,009,171,968 bytes free, above the 30 GiB
test-only threshold, and `/Volumes/sage` had about 182 GiB free. The public
manifest was rechecked and remained at 177 wheel entries with no public
`post15` primary. No duplicate work or publication was started. The cell
remains below `full` until the short gate and subsequent complete reduced full
analysis both pass.

## Post15 strict-gate pass and full-run start

The exact-SHA `post15` strict short gate completed with exit code zero at
`2026-07-13T05:07:16Z`. Its authoritative summary is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-215857-9f1fa2c9e55/validation/short-post15/validation-summary.md
```

The fresh wheel-only installation of
`sagelite[all-needed-extras]==10.9.post15`, `python -m pip check`, runtime
manifest, and every `sagelite-selftest` probe passed. The installed
`--optional=sage` sweep passed all 3,953 modules with zero failed modules, and
packaged pytest reported 213 passed and 2 skipped. The strict preflight
validated one repaired primary, 68 companion wheels, and 108 third-party
wheels, 177 wheels and 16,513,108,451 bytes in total. Its wheelhouse digest was
`17b9de665848c5fa74352f975f9cce5e9a00c388a16f5c003ba4933ed61006a2`.

The durable validation service removed the completed short install and
started a separate fresh full validation at `2026-07-13T05:07:21Z` with the
same exact-SHA wheel contract, strict repaired-wheelhouse preflight, explicit
`--optional sage`, and eight native aarch64 workers. Its active log is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-215857-9f1fa2c9e55/validation-full-command.log
```

At the transition, the full validation container was the only Sagelite
container, the user-systemd validation service remained active, and the Linux
guest had about 116 GiB free. The public manifest still contained 177 wheels,
14 `post8`/`post9` Sagelite primaries, and no public `post15` primary. No
publication was attempted. The cell remains below `full` until the complete
full sweep and reduced analysis pass.

## Post15 full-run early failures and flatter correction

The fresh `post15` full sweep confirmed that the preceding Giac expectation
change is incomplete. In `sage.calculus.calculus`, the Giac 1.9 branch refers
to `dummy_laplace`, which is not defined in the isolated doctest namespace;
the example raises `NameError` and its dependent comparison also fails. This
is the earliest real failure currently recorded in the still-running full log
and requires a separate focused source correction before another primary
rebuild.

An independent exact operation in the same untouched wheel-only container
also reproduced one of the completed `post14` failure classes. Both
`/run/install/full-post15/bin/flatter -h` and a two-by-two identity-matrix
input exited 127 because the packaged `flatter-real` could not load
`libgomp.so.1`. The previous companion smoke accepted the word `flatter` from
this loader error without checking the exit status.

Committed and pushed source
`50d9c58916a8faa14503e41ad5b1b424fec7f71d` allocates Sagelite
`10.9.post16` and flatter runtime `10.9.post1`, includes `libgomp` in the
companion runtime closure, raises every Sagelite dependency floor, and makes
the companion smoke require successful help and matrix operations. The
focused companion/dependency-floor tests report 5 passed, and Python syntax
and `git diff --check` validation passed. This is source-level regression
evidence only; the corrected companion wheel has not yet been built, so no
wheel or install claim is made.

At `2026-07-13T05:41:12Z`, the durable `post15` validation service and its
native aarch64 workers remained active, the guest had 101,949,771,776 bytes
free, and no full exit-code artifact existed. The public `dev/manifest.json`
still contained 177 wheels and fourteen `post8`/`post9` Sagelite primaries,
with no `post15` or `post16` primary. No publication was attempted. The next
iteration should correct the Giac doctest namespace failure, preserve the
completed `post15` reduced inventory, and only then start an exact-SHA rebuild
from the resulting coherent commit.

## Post16 Giac correction and durable follow-on

Committed and pushed source
`39fd8bb94c90c7249ff8d1f80a13d2ab9a93cc46` imports `dummy_laplace`
explicitly into the isolated doctest namespace. A focused probe in the
untouched `post15` wheel-only container used the bundled Giac 1.9 runtime and
confirmed that the actual and expected results are both the same formal
`laplace(t^n, t, s)` expression. Python compilation and `git diff --check`
also passed. The commit retains Sagelite `10.9.post16`, so it forms one
coherent source revision with the preceding flatter `post1` correction.

At preflight, `m1` reported macOS `arm64` and about 181 GiB free on
`/Volumes/sage`. Its Lima guest reported Linux `aarch64` with 101,358,800,896
bytes free. The only Sagelite container remained the active native `post15`
full validation, and its log continued to grow; no
`validation-full-exit-code` existed. The public manifest was unchanged at 177
wheel entries and fourteen `post8`/`post9` Sagelite primaries.

A durable exact-SHA follow-on is staged at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9
```

The guest user-systemd services `sagelite-post16-follow.service` and
`sagelite-post16-validate.service` were active after the controller SSH
session exited, with main PIDs `1388226` and `1388238`. The first service is
waiting for the `post15` full exit artifact. It will preserve that run's
wheelhouse, summaries, reduced analysis, metadata, and logs; remove only its
disposable install; recheck the 100 GiB heavy-build threshold; and then build
the exact pushed `post16` commit. The validation service will assemble a fresh
strict closure and run the required wheel-only `--optional sage` short and
full gates only after a successful build. Progress and terminal artifacts are
recorded in `follow-on.log`, `command.log`, `validation-follow.log`, and the
phase-specific exit-code files. No `post16` wheel, installation, or smoke
result is claimed yet.

## Post15 full inventory completion and post16 build start

The exact-SHA `post15` full validation finished at `2026-07-13T07:25:32Z`
with exit code 21 after 8,274 seconds. The authoritative artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-215857-9f1fa2c9e55/validation/full-post15/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-215857-9f1fa2c9e55/validation/full-post15/doctest-installed-linux-aarch64-cp313-post15-full-20260713-051221.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-215857-9f1fa2c9e55/validation/full-post15/doctest-installed-linux-aarch64-cp313-post15-full-20260713-051221.analysis.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-215857-9f1fa2c9e55/validation-full-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260712-215857-9f1fa2c9e55/validation-full-exit-code
```

The fresh strict wheel-only command installed
`sagelite[all-needed-extras]==10.9.post15` from the same 177-wheel contract as
the passing short gate, then ran the complete installed suite with
`--optional sage --full --nthreads 8`. Installation, `pip check`, the runtime
manifest, every selftest probe, and packaged pytest still passed. The complete
doctest reducer saw 3,958 modules and 24 failed modules: 14 core-supported,
seven timeout/performance, two optional-external, and one optional-data.

The selected `post16` corrections cover the Giac doctest namespace failure and
the flatter loader failures. The preserved inventory also identifies separate
future classes: four modules requiring `gcc` or `pkg-config` during runtime
doctests, two msolve modules receiving colon-terminated output, fpylll strategy
data or portability failures, Giac/FriCAS/GAP3 protocol differences, numerical
and interrupt-timing sensitivity, and seven module timeouts or aborts. These
classes are not treated as fixed by inference and will be triaged from the
fresh `post16` result.

The durable follow-on observed the full exit artifact, preserved the evidence,
removed only the disposable `post15` install, and started the clean exact-SHA
`post16` rebuild at `2026-07-13T07:26:35Z` from:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9
```

At `2026-07-13T07:32:35Z`, the checked-out source reported
`39fd8bb94c90c7249ff8d1f80a13d2ab9a93cc46`, the native CIBW aarch64
container was active, the build log continued to grow, the Linux guest had
119,699,353,600 bytes free, and `/Volumes/sage` had about 199 GiB free. The
validation watcher remained active and had not started early. The public
manifest still contained 177 wheels and fourteen `post8`/`post9` primaries,
with no `post15` or `post16` primary. No duplicate job or publication was
started, and no `post16` wheel or validation result is claimed yet.

## Post16 native build progress checkpoint

The recovered-session preflight at `2026-07-13T08:31:31Z` found the same two
intended guest user-systemd services active. The follow service still owned
the only CIBW build, and the validation service was waiting for the build
exit-code artifact; no validation container had started early. The source
checkout was clean at the exact committed SHA
`39fd8bb94c90c7249ff8d1f80a13d2ab9a93cc46` and reported
`10.9.post16` from `VERSION.txt`.

The sole build container reported native `aarch64` and was actively using its
CPUs. Its Sagelib package log had reached Cython source 365 of 1,794, with
live Cython workers providing forward-progress evidence even though the
top-level log was temporarily quiet while package output was redirected. No
build or validation exit-code artifact existed yet. The Linux guest had
118,274,359,296 bytes free, above the heavy-build threshold, and the outer
macOS host had about 197 GiB free on `/Volumes/sage`.

The public `dev/manifest.json` was fetched directly and still contained 177
wheel entries. Its fourteen Sagelite primary entries remain the seven
`post8` and seven `post9` wheels; no `post15` or `post16` primary is public.
No duplicate work or publication was started, and this checkpoint makes no
new wheel, install, smoke, or full-suite claim.

## Post16 native compilation checkpoint

The next scheduled reconciliation at `2026-07-13T09:02:21Z` found the same
two intended guest user-systemd services active with main PIDs `1388226` and
`1388238`. The follow service continued to own the only CIBW build, and the
validation watcher still had not started a container because no build
`exit-code` artifact existed. The exact source checkout remained clean at
`39fd8bb94c90c7249ff8d1f80a13d2ab9a93cc46` with version
`10.9.post16`.

The native `aarch64` build container was CPU-active and had advanced from
Cython generation into compiled extension target 643 of 1,794. Its Sagelib
package log was growing at the checkpoint. The Linux guest had about 110 GiB
free, the outer macOS host had about 197 GiB free on `/Volumes/sage`, and the
controller had about 103 GiB free on `/scratch`; all filesystems remained
above their applicable thresholds.

The public `dev/manifest.json` still contained 177 wheels and the Sagelite
project page still listed only the seven `post8` and seven `post9` primary
wheels. No duplicate build, validation, or publication was started. The cell
remains below `full`, and this checkpoint makes no wheel, install, smoke, or
full-suite claim.

## Post16 midpoint compilation checkpoint

The scheduled reconciliation at `2026-07-13T09:31:25Z` found the same two
intended guest user-systemd services active with main PIDs `1388226` and
`1388238`. The follow service still owned the only CIBW build container, and
the validation watcher was still correctly waiting for the build exit-code
artifact. No build or validation exit-code artifact existed. The exact source
checkout remained clean at
`39fd8bb94c90c7249ff8d1f80a13d2ab9a93cc46` and reported Sagelite
`10.9.post16`.

The native `aarch64` build was CPU-active and had reached compiled extension
target 946 of 1,794. Its Sagelib package log was growing and eight concurrent
compiler processes supplied additional forward-progress evidence. The Linux
guest had about 108 GiB free, the outer macOS host had about 195 GiB free on
`/Volumes/sage`, and the controller had about 103 GiB free on `/scratch`; all
filesystems remained above their applicable thresholds.

The directly fetched public `dev/manifest.json` still contained 177 wheels
and fourteen Sagelite primary wheels: seven `post8` and seven `post9`. No
`post15` or `post16` primary is public. No duplicate build, validation, or
publication was started. The cell remains below `full`, and this checkpoint
makes no new wheel, install, smoke, or full-suite claim.

## Post16 late compilation checkpoint

The scheduled reconciliation at `2026-07-13T10:01:42Z` found the same two
intended guest user-systemd services active. The follow service continued to
own the sole CIBW container, while the validation service remained correctly
blocked on the absent build exit-code artifact. No validation container had
started. The exact source checkout was clean at
`39fd8bb94c90c7249ff8d1f80a13d2ab9a93cc46` and still reported Sagelite
`10.9.post16`.

The native `aarch64` build had advanced to compiled extension target 1,353 of
1,794. Its Sagelib package log was growing at the checkpoint, the container
was CPU-active, and live compiler and linker processes supplied independent
forward-progress evidence. The Linux guest had 107 GiB free, and the outer
macOS host had 193 GiB free on `/Volumes/sage`; both remained above the
applicable build thresholds.

The public project page continued to list only the seven `post8` and seven
`post9` primary wheels, and the public manifest remained at 177 wheels. No
duplicate build, validation, or publication was started. The cell remains
below `full`, and this checkpoint makes no wheel, install, smoke, or
full-suite claim.

## Post16 wheel-construction checkpoint

The scheduled reconciliation at `2026-07-13T10:31:46Z` found the exact-SHA
native build still healthy. The same two intended guest user-systemd services
remained active: the follow service owned the only CIBW container, and the
validation service continued waiting for the absent build exit-code artifact.
The source checkout was clean at
`39fd8bb94c90c7249ff8d1f80a13d2ab9a93cc46` and reported Sagelite
`10.9.post16`.

The build had moved into its 1,795-target wheel-construction Ninja phase.
Although the top-level command log was buffered at the initial external Maxima
target during the checkpoint, the container was CPU-active and concurrent
Cython workers were compiling Sage matrix extensions while ECL/Maxima compiler
processes were also live. The Linux guest had 112,720,257,024 bytes free, the
outer macOS host had about 192 GiB free on `/Volumes/sage`, and the controller
had about 103 GiB free on `/scratch`.

The directly fetched public manifest still contained 177 wheels and fourteen
Sagelite primaries: the seven `post8` and seven `post9` wheels. No `post15` or
`post16` primary is public. No duplicate build, validation, or publication was
started. The cell remains below `full`, and this checkpoint makes no new
wheel, install, smoke, or full-suite claim.

## Post16 active wheel-build checkpoint

The scheduled reconciliation at `2026-07-13T11:01:09Z` found the same two
intended guest user-systemd services active with main PIDs `1388226` and
`1388238`. The follow service still owned the sole CIBW container, while the
validation watcher remained correctly blocked on the absent build exit-code
artifact. No validation container had started, and the run directory contained
no completed wheel yet. The source checkout remained clean at
`39fd8bb94c90c7249ff8d1f80a13d2ab9a93cc46` and reported Sagelite
`10.9.post16`.

The native `aarch64` container was heavily CPU-active. Its wheel-build Ninja
log contained 578 completed outputs and continued to grow while concurrent
Cython workers advanced through Sage schemes and sets extensions. The ECL
process compiling the bundled Maxima runtime also remained active. These
package-level processes supplied forward-progress evidence while the buffered
top-level command log still displayed the initial external Maxima target.

The Linux guest had 112,354,803,712 bytes free, the outer macOS host had about
192 GiB free on `/Volumes/sage`, and the controller had 110,488,498,176 bytes
free on `/scratch`; all remained above their applicable thresholds. The
directly fetched public manifest still contained 177 wheels and fourteen
Sagelite primaries, all from `post8` and `post9`, with no `post15` or `post16`
primary. No duplicate build, validation, or publication was started. The cell
remains below `full`, and this checkpoint makes no new wheel, install, smoke,
or full-suite claim.

## Post16 wheel-build progress checkpoint

The scheduled reconciliation at `2026-07-13T11:31:44Z` found the same two
intended guest user-systemd services active with main PIDs `1388226` and
`1388238`. The follow service continued to own the sole native aarch64 CIBW
container, and the validation service remained blocked on the absent build
exit-code artifact. No completed wheel or validation container existed. The
exact source checkout was clean at
`39fd8bb94c90c7249ff8d1f80a13d2ab9a93cc46` and reported Sagelite
`10.9.post16`.

The live wheel-build Ninja log had advanced from 578 to 932 completed output
records. Fourteen compiler or ECL processes were active, with recent completed
objects in the Sage matrix extensions and the bundled Maxima build still
running. The Linux guest had 112,098,607,104 bytes free, the outer macOS host
had about 191 GiB free on `/Volumes/sage`, and the controller had
110,488,498,176 bytes free on `/scratch`; all remained above their applicable
thresholds.

The directly fetched public `dev/manifest.json` still contained 177 wheels
and fourteen Sagelite primaries, all from `post8` and `post9`; no `post15` or
`post16` primary is public. No duplicate build, validation, or publication was
started. The cell remains below `full`, and this checkpoint makes no new
wheel, install, smoke, or full-suite claim.

## Post16 final wheel-construction checkpoint

The scheduled reconciliation at `2026-07-13T12:04:35Z` found the same two
intended guest user-systemd services active. The follow service continued to
own the only native aarch64 CIBW container, and the validation service still
waited for the absent build exit-code artifact. No completed wheel or
validation container existed. The exact source checkout remained clean at
`39fd8bb94c90c7249ff8d1f80a13d2ab9a93cc46` with Sagelite
`10.9.post16`.

The wheel-build Ninja log had advanced to 1,811 completed records. Sage's
extension compilation had cleared, including the large symbolic-expression
object; the remaining live child work was the bundled Maxima external project
generating its manual and index files. Those Perl processes were CPU-active,
and the Maxima build log continued to grow. The Linux guest had about 105 GiB
free, the outer macOS host had about 191 GiB free on `/Volumes/sage`, and both
the controller and `host` bulk filesystems had about 103 GiB free. All remained
above the applicable thresholds.

The public `dev/manifest.json` was fetched directly and still contained 177
wheels and fourteen Sagelite primaries, all from `post8` and `post9`; no
`post15` or `post16` primary is public. No duplicate build, validation, or
publication was started. The cell remains below `full`, and this checkpoint
makes no new wheel, install, smoke, or full-suite claim.

## Post16 wheel completion and corrected strict-gate retry

The exact-SHA native CIBW build completed successfully at
`2026-07-13T12:16:40Z`. Its clean source checkout remains at
`39fd8bb94c90c7249ff8d1f80a13d2ab9a93cc46` with Sagelite
`10.9.post16`. The build produced:

```text
sagelite-10.9.post16-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=c13515c47b7f9ac9110b753841dcac7de14fd5f0eaf9f30863fcdd34103b5e3a
size=227682159

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=2600203fae81624e6ac9fe71ca8514d89775272552fc1764fec002b74f233282
size=66578984
```

The first strict short attempt exited 2 before installation because its
inherited closure still contained
`sagelite_flatter_runtime-10.9-py3-none-manylinux_2_28_aarch64.whl`, while
the `post16` primary correctly requires `>=10.9.post1,<10.10`. Its summary
and command evidence were preserved as:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9/validation/short-post16-preflight1/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9/preflight1-validation-short-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9/preflight1-validation-short-exit-code
```

A focused native build used the exact committed companion package definition,
the cached manylinux 2.28 aarch64 build image, and the preceding manylinux
flatter payload. The resulting wheel is:

```text
sagelite_flatter_runtime-10.9.post1-py3-none-manylinux_2_28_aarch64.whl
sha256=944df1933cd835b6e3282b3a8dbf68158569730e90dfd29494becbeed32d198c
size=45086686
```

Its archive contains `libgomp.so.1`. Auditwheel found its external symbol set
compatible with manylinux 2.27 aarch64, which is within the advertised
manylinux 2.28 contract. A fresh `python:3.13-slim-bookworm` wheel-only smoke
passed import, help execution, and a two-dimensional unimodular lattice
reduction without inherited library paths. On aarch64 flatter returns the
identity basis with its rows permuted; the semantic smoke verifies the same
row set and determinant rather than imposing row order. Durable focused
artifacts are under:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9/flatter-post1-build
```

The corrected exact-SHA build inventory now contains the primary, Maxima, and
flatter wheels. A durable strict retry started at `2026-07-13T12:39:09Z`.
Its repaired wheelhouse preflight accepted 177 wheels: one primary, 68
companions, and 108 third-party wheels totaling 16,513,214,933 bytes, with
wheelhouse digest
`564efab23f48f6d5a6b7ff08383d279f499deffeef0316db2922733491217288`.
The fresh wheel-only installation of
`sagelite[all-needed-extras]==10.9.post16` was active at the checkpoint. The
retry is owned by `sagelite-post16-validate-retry1.service`; it will start the
full gate only after the short gate passes. No installation, short-suite, or
full-suite pass is claimed yet.

The directly fetched public manifest remains unchanged at 177 wheels and
fourteen `post8`/`post9` Sagelite primaries, with no public `post15` or
`post16` primary. No publication was attempted.

## Post16 strict-gate runtime checkpoint

The scheduled reconciliation at `2026-07-13T13:02:30Z` found the corrected
strict gate healthy under the sole
`sagelite-post16-validate-retry1.service`. The exact remote source checkout
remained clean at committed source
`39fd8bb94c90c7249ff8d1f80a13d2ab9a93cc46`, and the validation container
reported native Linux `aarch64`.

The fresh wheel-only installation of
`sagelite[all-needed-extras]==10.9.post16` completed successfully, and
`python -m pip check` reported no broken requirements. Runtime manifest and
summary collection completed, and every `sagelite-selftest` probe passed,
including the corrected flatter help and runtime operation probe. The
installed `--optional=sage` short sweep then started all 3,953 modules with
eight workers. At the checkpoint its log was growing, the dispatcher and
workers were CPU-active, and no validation exit-code artifact existed.

The Linux guest had 97,798,500,352 bytes free, above the test-only threshold;
the outer macOS host had about 178 GiB free on `/Volumes/sage`, and the
controller had 110,488,498,176 bytes free on `/scratch`. The public
`dev/manifest.json` still contained 177 wheels and fourteen Sagelite
primaries, all from `post8` and `post9`; no `post16` primary is public. No
duplicate work or publication was started. The cell remains below `full`
until the short gate and subsequent full reduced analysis complete.

## Post16 strict-gate pass and full-run start

The corrected exact-SHA strict short gate finished at
`2026-07-13T13:31:30Z` with exit code zero. Its authoritative summary is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9/validation/short-post16/validation-summary.md
```

The strict preflight accepted one repaired primary, 68 companion wheels, and
108 third-party wheels: 177 wheels totaling 16,513,214,933 bytes, with
wheelhouse digest
`564efab23f48f6d5a6b7ff08383d279f499deffeef0316db2922733491217288`.
The fresh wheel-only installation of
`sagelite[all-needed-extras]==10.9.post16`, `python -m pip check`, runtime
manifest, and every `sagelite-selftest` probe passed. The installed
`--optional=sage` short sweep passed all 3,953 modules with zero failed
modules, and packaged pytest reported 213 passed and 2 skipped.

The sole durable validation service removed the completed short install and
started a separate fresh full run from the same exact-SHA wheel contract at
`2026-07-13T13:31:36Z`. Its native Linux `aarch64` container invokes the
strict repaired-wheelhouse profile with explicit `--optional sage`, `--full`,
and eight workers. The active validator log is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9/validation-full-command.log
```

At handoff, `sagelite-post16-validate-retry1.service` remained active and
owned the only Sagelite validation container. The Linux guest had about 92
GiB free, the outer macOS host had 178 GiB free on `/Volumes/sage`, and the
controller had 103 GiB free on `/scratch`, all above their applicable
thresholds. The directly fetched public manifest still contained 177 wheels
and fourteen `post8`/`post9` Sagelite primaries, with no public `post15` or
`post16` primary. No publication was attempted. The cell remains below
`full` until the complete full sweep and reduced analysis pass.

## Post16 full result and post17 msolve iteration

The exact-SHA `post16` full validation finished at
`2026-07-13T15:49:34Z` with validator exit code 21 after 8,230 seconds. The
fresh strict 177-wheel command installed
`sagelite[all-needed-extras]==10.9.post16`, passed `pip check`, runtime
collection, every selftest probe, and packaged pytest with 213 passed and two
skipped. The full installed `--optional=sage` sweep completed 3,958 modules
and failed 21. Its reducer classified 10 `core-supported`, eight
`performance-only`, two `optional-external`, and one `optional-data` module.
The authoritative artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9/validation/full-post16/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9/validation/full-post16/doctest-installed-linux-aarch64-cp313-post16-full-20260713-133738.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9/validation/full-post16/doctest-installed-linux-aarch64-cp313-post16-full-20260713-133738.analysis.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9/validation-full-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260713-060447-39fd8bb94c9/validation-full-exit-code
```

The selected coherent failure class was the msolve parser diagnostic affecting
`sage.rings.polynomial.msolve` and
`sage.rings.polynomial.multi_polynomial_ideal`. The bundled runtime returned
valid Sage-readable list payloads followed by a single terminal colon. The
existing payload extractor retained that delimiter, so `sage_eval` raised a
syntax error for every Gröbner-basis and variety result.

Committed and pushed source
`3e6ff4288595e458add14482065345d67f63c36e` strips only that terminal
delimiter, adds one-line and multiline regression examples, and allocates
Sagelite `10.9.post17`. Local syntax, version-consistency, and focused payload
checks passed. An exact-SHA source checkout was then tested in a fresh native
Linux aarch64 container against the untouched installed `post16` runtime. The
bundled msolve successfully computed a finite-field Gröbner basis, a rational
Gröbner basis, and a rational variety through the corrected module. This is
focused regression evidence rather than wheel acceptance. Its durable
artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260713-232928-3e6ff4288595/focused-msolve.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260713-232928-3e6ff4288595/focused-msolve-exit-code
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260713-232928-3e6ff4288595/run-metadata.txt
```

After preserving the full `post16` summary, reduced analysis, wheelhouse, and
logs, the iteration removed only its 21 GiB disposable validation install.
The guest then had about 111 GiB free, above the 100 GiB heavy-build threshold.
Exactly one native exact-SHA rebuild and one gated validation watcher started
as the transient user services `sagelite-post17-build.service` and
`sagelite-post17-validate.service`. Their shared run root is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260713-232928-3e6ff4288595
```

The watcher will assemble a fresh strict closure and run wheel-only
`--optional sage` short and full gates only after the build succeeds. The
public manifest was rechecked with a pip user agent and still contained 177
wheels and fourteen `post8`/`post9` Sagelite primaries; no `post16` or
`post17` primary is public. No publication was attempted, no `post17` wheel is
claimed yet, and this cell remains below `full`.

## Post17 native wheel-build checkpoint

The scheduled reconciliation at `2026-07-14T00:02:03Z` found the same two
intended guest user-systemd services active. The build service owned the only
CIBW container, while the validation service remained correctly blocked on
the absent build exit-code artifact. No validation container had started and
no completed `post17` wheel existed. The exact source checkout was clean at
`3e6ff4288595e458add14482065345d67f63c36e` and reported Sagelite
`10.9.post17`.

The actual build environment reported native Linux `aarch64`. The build had
entered its 1,795-target wheel-construction phase and was actively completing
the bundled Maxima installation; live `make`, documentation generator, and
Ninja processes supplied forward-progress evidence. The Linux guest had
about 100 GiB free, the outer macOS host had about 187 GiB free on
`/Volumes/sage`, and the controller had about 103 GiB free on `/scratch`.
All remained above the applicable thresholds.

The public `dev/manifest.json` was fetched directly and remained unchanged at
177 wheels and fourteen Sagelite primaries, all from `post8` and `post9`.
No `post17` primary is public. No duplicate build, validation, or publication
was started. The cell remains below `full`, and this checkpoint makes no new
wheel, install, smoke, or full-suite claim.

## Post17 wheel result and post18 coordinate-order iteration

The exact-SHA native `post17` build completed with exit code zero and produced:

```text
sagelite-10.9.post17-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=95ef9227ad7525e9a36849e2d21a014e3fcccf53ba2f6b81c0f46c6d2d74fbae
size=227682225

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=cc338d27cd31432e9823fb3bd0ac809594ecb1465f578808a741dbcee8b7a7ec
size=66578984
```

The fresh strict short gate staged 177 wheels totaling 16,513,214,999 bytes,
with wheelhouse digest
`e02d7714056bdda28f1741f10e104335cc440139f09e63e76cbf4f60ee33febb`.
The wheel-only install of `sagelite[all-needed-extras]==10.9.post17`, `python
-m pip check`, runtime manifest, every selftest probe, and packaged pytest
(213 passed and two skipped) passed. The installed `--optional=sage` sweep
completed 3,954 modules but failed 11: nine `core-supported` and two
`optional-external`. Its authoritative artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260713-232928-3e6ff4288595/validation/short-post17/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260713-232928-3e6ff4288595/validation/short-post17/doctest-installed-linux-aarch64-cp313-post17-short-20260714-001005.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260713-232928-3e6ff4288595/validation/short-post17/doctest-installed-linux-aarch64-cp313-post17-short-20260714-001005.analysis.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260713-232928-3e6ff4288595/validation-short-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260713-232928-3e6ff4288595/validation-short-exit-code
```

The terminal-colon parser correction worked: msolve returned and parsed valid
varieties. Its 14 failing examples instead showed that this native runtime
lists variables as `y, x`; Sage retained that insertion order even though the
polynomial ring's canonical generator order is `x, y`. The other ten failed
modules belong to the independent compiler-tool, Giac, GAP3, fpylll, Qepcad,
and installed-path classes already visible in the `post16` inventory.

Committed and pushed source
`8c0f5c742d38ff40ca885d1d45e469280c0c252b` constructs each returned msolve
mapping in polynomial-ring generator order while retaining the runtime's
variable-to-coordinate association, and allocates Sagelite `10.9.post18`.
A focused native container mounted only the corrected module over the
untouched failed `post17` install. Rational, 100-bit real, and large
finite-field varieties all preserved their values and returned keys in ring
order. This is focused regression evidence, not wheel acceptance:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-post18-focused-20260714/focused-msolve-order.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-post18-focused-20260714/focused-msolve-order-exit-code
```

After preserving the failed gate's wheelhouse, summary, reduced analysis, and
logs, the iteration removed only its 21 GiB disposable install. The guest then
had about 109 GiB free. One exact-SHA build and one gated validation watcher
started as the transient user services `sagelite-post18-build.service` and
`sagelite-post18-validate.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-003540-8c0f5c742d3
```

The build service records exact source checkout verification before invoking
the native CPython 3.13 aarch64 CIBW contract. The validation service will
assemble a fresh strict closure and run wheel-only `--optional sage` short and
full gates only after build success. The public manifest remains unchanged at
177 wheels and fourteen `post8`/`post9` Sagelite primaries; no `post17` or
`post18` primary is public. No publication was attempted, no `post18` wheel is
claimed yet, and the cell remains below `full`.

## Post18 native wheel-build checkpoint

The scheduled reconciliation at `2026-07-14T01:02:14Z` found exactly the two
intended guest user-systemd services active. The build service owned the only
CIBW container, while the validation service remained correctly blocked on
the absent build exit-code artifact. No validation container or completed
`post18` wheel existed. The exact source checkout was clean at
`8c0f5c742d38ff40ca885d1d45e469280c0c252b` and reported Sagelite
`10.9.post18`; the actual build environment reported native Linux `aarch64`.

The wheel-construction phase was CPU-active across all eight guest CPUs,
compiling Sage matrix and numerical extensions while ECL compiled the bundled
Maxima runtime. A 20-second sample continued to report approximately 790%
container CPU usage, providing independent forward-progress evidence despite
the buffered top-level command log. The Linux guest had about 99 GiB free,
the outer macOS host had about 185 GiB free on `/Volumes/sage`, and the
controller had about 103 GiB free on `/scratch`. The build began above the
100 GiB heavy-build threshold, and the remaining filesystems stayed above
their applicable thresholds.

The directly fetched public `dev/manifest.json` still contained 177 wheel
entries and fourteen Sagelite primaries, all from `post8` and `post9`; no
`post17` or `post18` primary is public. No duplicate build, validation, or
publication was started. The cell remains below `full`, and this checkpoint
makes no new wheel, install, smoke, or full-suite claim.

## Post18 wheel result and post19 display-order iteration

The exact-SHA native `post18` build completed with exit code zero and
produced:

```text
sagelite-10.9.post18-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=736e708f8b5e37371a147f5ddf2e0a375a47e6f0409ec3c4ea170f61aaae89e7
size=227682377

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=4f0cb673c5e195244acbaf4c1496222735fdc8de4e348987a4dd7ea12a5794b7
size=66578984
```

The fresh strict short gate staged one primary, 68 companions, and 108
third-party wheels: 177 wheels totaling 16,513,215,151 bytes, with
wheelhouse digest
`68525ff9947c5b2be0a2bbba8015813b9e76a2c63a64c06124a3cecf270f14e3`.
The wheel-only install of
`sagelite[all-needed-extras]==10.9.post18`, `python -m pip check`, runtime
manifest, every selftest probe, and packaged pytest with 213 passed and two
skipped all passed. The installed `--optional=sage` sweep completed 3,954
modules but failed 12: ten `core-supported` and two `optional-external`.
Its authoritative artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-003540-8c0f5c742d3/validation/short-post18/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-003540-8c0f5c742d3/validation/short-post18/doctest-installed-linux-aarch64-cp313-post18-short-20260714-011315.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-003540-8c0f5c742d3/validation/short-post18/doctest-installed-linux-aarch64-cp313-post18-short-20260714-011315.analysis.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-003540-8c0f5c742d3/validation-short-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-003540-8c0f5c742d3/validation-short-exit-code
```

The `post18` msolve correction preserved every coordinate value and its
variable association, but the Sage doctest rich-output hook re-sorted
`KeyConvertingDict` keys by polynomial monomial comparison order. That
changed canonical `x, y` presentation back to `y, x`. Three explicitly
sorted finite-field checks and one complex-root check also retained
platform-sensitive solution ordering.

Committed and pushed `post19` source
`8f8586207b37010efd2d82e545cb23fa330c0f1e` makes the established
`KeyConvertingDict` pretty-print hook retain insertion order, keeps ordinary
doctest dictionaries deterministically sorted, and stabilizes the affected
msolve solution checks. An exact-commit native container overlaid only the
corrected pure-Python modules on the untouched `post18` installed wheel.
All 76 converting-dictionary tests and all 57 msolve tests passed. This is
focused regression evidence rather than wheel acceptance:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-post19-focused-20260714-8f8586207b3/focused-doctest.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-post19-focused-20260714-8f8586207b3/focused-doctest-exit-code
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-post19-focused-20260714-8f8586207b3/run-metadata.txt
```

After preserving the `post18` wheelhouse, validation summary, reduced
analysis, and logs, the iteration removed only its 21 GiB disposable failed
install through its owning validation container environment. The guest then
had 113,125,724,160 bytes free, above the 100 GiB heavy-build threshold.
Exactly one native rebuild and one gated watcher started as
`sagelite-post19-build.service` and `sagelite-post19-validate.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-014940-8f8586207b3
```

The services record exact source checkout verification before building and
will assemble a fresh strict closure and run wheel-only `--optional sage`
short and full gates only after build success. At the checkpoint the clean
source clone was in progress and the watcher was waiting. The public manifest
remained unchanged at 177 wheels and fourteen `post8`/`post9` Sagelite
primaries. No publication was attempted, no `post19` wheel is claimed yet,
and this cell remains below `full`.

## Post19 native wheel-build checkpoint

The scheduled reconciliation at `2026-07-14T02:01:42Z` found exactly the two
intended guest user-systemd services active. The build service owned the only
CIBW container, and the validation watcher remained correctly blocked on the
absent build exit-code artifact. No validation container or completed
`post19` wheel existed. The exact source checkout was clean at
`8f8586207b37010efd2d82e545cb23fa330c0f1e` and reported Sagelite
`10.9.post19`.

The actual manylinux build container reported Linux `aarch64`. It had reached
the Sagelite extension build and was using approximately 800% CPU across the
eight guest CPUs, with active GCC processes compiling matrix, geometry,
combinatorics, and data-structure extensions. This supplied forward-progress
evidence even though the buffered top-level command log did not grow during a
15-second sample. None of `exit-code`, `validation-short-exit-code`,
`validation-full-exit-code`, or `follow-on-exit-code` existed.

The Linux guest had 106,458,218,496 bytes free after starting above the
100 GiB heavy-build threshold. The outer macOS host had about 187 GiB free on
`/Volumes/sage`, and the controller had about 103 GiB free on `/scratch`.
The directly fetched public `dev/manifest.json` remained unchanged at 177
wheels and fourteen Sagelite primaries, all from `post8` and `post9`; no
`post19` primary is public. No duplicate build, validation, or publication
was started. The cell remains below `full`, and this checkpoint makes no new
wheel, install, smoke, or full-suite claim.

## Post19 wheel completion and strict-gate checkpoint

The exact-SHA native build completed with exit code zero and produced:

```text
sagelite-10.9.post19-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=ad8feb0fb8a8c66acd813568bb063cd9b3dba0ff3b0b67bfa1d3254ba726b899
size=227682587

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=dfe99433da28e83e7f7b7ee7adc0048c59ecb2539d79a554c3b52bc5aea9de48
size=66578984
```

The validation watcher assembled a fresh strict closure of one primary, 68
companions, and 108 third-party wheels: 177 wheels totaling 16,513,215,361
bytes. Its `SHA256SUMS` digest is
`4461265f420ca1d3e98ebabe64ae83ecd0b2e2c6add8b52aabf781b961ddf681`.
Every repaired-wheelhouse preflight passed. The fresh wheel-only installation
of `sagelite[all-needed-extras]==10.9.post19`, `python -m pip check`, runtime
manifest, and every `sagelite-selftest` probe also passed.

At `2026-07-14T02:33:05Z`, the installed `--optional=sage` short gate was
healthy and running all 3,953 modules across eight native aarch64 workers. It
had emitted only a slow-test warning and no failure, while the container used
approximately eight CPUs. The validation service remains the only active
automation-owned job for this target, and no duplicate was started. Its
durable artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-014940-8f8586207b3/validation-wheelhouse/SHA256SUMS
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-014940-8f8586207b3/validation/short-post19/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-014940-8f8586207b3/validation/short-post19/doctest-installed-linux-aarch64-cp313-post19-short-20260714-022718.selftest.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-014940-8f8586207b3/validation-short-command.log
```

The Linux guest had about 84 GiB free, the outer macOS host had about 170 GiB
free on `/Volumes/sage`, and the controller had about 103 GiB free on
`/scratch`. The public `dev/manifest.json` remained unchanged at 177 wheels
and fourteen Sagelite primaries, all from `post8` and `post9`; no `post19`
primary is public. No publication was attempted. The cell remains below
`full` until the short gate, its reduced analysis, and the gated full run all
complete successfully.

## Post19 short result and post20 display follow-up

The exact-SHA `post19` short gate finished with exit code one. Its fresh
wheel-only installation, `python -m pip check`, runtime manifest, every
`sagelite-selftest` probe, and packaged pytest with 213 passed and two skipped
all passed. Reduced analysis covered 3,954 modules and found 13 failed
modules: eleven `core-supported` and two `optional-external`. The actionable
buckets were five runtime exceptions, four output mismatches, two numeric
tolerance failures, one GAP3 runtime error, and one stale-build-path failure.
The authoritative failure artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-014940-8f8586207b3/validation/short-post19/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-014940-8f8586207b3/validation/short-post19/doctest-installed-linux-aarch64-cp313-post19-short-20260714-022718.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-014940-8f8586207b3/validation/short-post19/doctest-installed-linux-aarch64-cp313-post19-short-20260714-022718.analysis.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-014940-8f8586207b3/validation-short-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-msolve-20260714-014940-8f8586207b3/validation-short-exit-code
```

One coherent five-example class was the follow-through from the `post19`
`KeyConvertingDict` insertion-order change. The msolve numeric tolerance
marker was on a continuation line, which the doctest tolerance parser does
not inspect, while msolve-backed polynomial ideals and Boolean polynomial
sequences still expected the old sorted-key rendering. Exact committed and
pushed `post20` source
`87330f2482d5fd788cfb737c4a7c4f4f32c06301` moves the tolerance marker to
the parsed source line and aligns those expectations without changing values
or key associations. It retains the established finite-field solution sorter
after a `key=str` experiment changed the fragile randomized solver result.

Against the untouched installed `post19` runtime, pure-Python `post20`
overlays passed all 54 msolve, 986 multivariate ideal, and 314 Boolean
polynomial sequence doctests together. The 986-test ideal module also passed
three independent repeat runs. This is focused regression evidence, not
wheel acceptance:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post20-focused-20260714-working/focused-doctest-final.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post20-focused-20260714-working/focused-final-exit-code
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post20-focused-20260714-working/focused-ideal-repeat.log
```

After preserving the `post19` wheelhouse, validation summary, reduced
analysis, metadata, and logs, the iteration removed only its 21 GiB
disposable failed install. The guest then had 111,254,667,264 bytes free,
above the 100 GiB heavy-build threshold. The exact-SHA native rebuild and
gated short/full watcher started as `sagelite-post20-build.service` and
`sagelite-post20-validate.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-031029-87330f2482d
```

The clean source checkout exactly matched the recorded commit and reported
`10.9.post20`. The active CIBW container reported Linux `aarch64`, while the
watcher remained correctly blocked on the absent build exit artifact. The
public manifest remained at 177 wheels and fourteen `post8`/`post9` Sagelite
primaries. No publication was attempted, no `post20` wheel is claimed, and
the cell remains below `full`.

## Post20 native wheel-build checkpoint

The scheduled reconciliation at `2026-07-14T03:33:58Z` found exactly the two
intended guest user-systemd services active. The build service owned the sole
CIBW container, and the validation service remained correctly blocked on the
absent build exit-code artifact. No validation container or completed
`post20` wheel existed. The exact source checkout was clean at
`87330f2482d5fd788cfb737c4a7c4f4f32c06301` and reported Sagelite
`10.9.post20`; the actual build container reported native Linux `aarch64`.

The build had reached its 1,795-target wheel-construction phase. Its Ninja log
contained 872 records and continued to grow, while live GCC and ECL processes
used approximately all eight guest CPUs. The Linux guest had
100,021,075,968 bytes free after the build began above the 100 GiB heavy-build
threshold. The outer macOS host had about 180 GiB free on `/Volumes/sage`, and
the controller had about 103 GiB free on `/scratch`.

The directly fetched public `dev/manifest.json` remained unchanged at 177
wheel entries and fourteen Sagelite primaries, all from `post8` and `post9`.
No duplicate build, validation, or publication was started. The cell remains
below `full`, and this checkpoint makes no wheel, install, smoke, or
full-suite claim.

## Post20 wheel result and post21 Giac completion iteration

The exact-SHA native `post20` build completed with exit code zero and
produced:

```text
sagelite-10.9.post20-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=a56716f1ce9c06bc8b7159c171dfd905252b62541b16d7639522955df88c4c94
size=227682598

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=2e2d538fc12ec9f5d0dd5cf889002dc1e210d288c750d6cd0309527fa170f9ae
size=66578984
```

The fresh strict short gate staged one primary, 68 companions, and 108
third-party wheels: 177 wheels totaling 16,513,215,372 bytes. The SHA256SUMS
digest is `e2510c4c40a9dba6db4b7e5fb44d0b9c4385f22c0d9d8a7c565c076c8c2165a0`.
Its wheel-only installation of
`sagelite[all-needed-extras]==10.9.post20`, `python -m pip check`, runtime
manifest, every selftest probe, and packaged pytest with 213 passed and two
skipped all passed. The installed `--optional=sage` sweep completed 3,954
modules but failed ten: eight `core-supported` and two `optional-external`.
The `post20` msolve, polynomial-ideal, and Boolean-sequence display class is
absent. The authoritative failed-gate artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-031029-87330f2482d/validation/short-post20/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-031029-87330f2482d/validation/short-post20/doctest-installed-linux-aarch64-cp313-post20-short-20260714-034729.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-031029-87330f2482d/validation/short-post20/doctest-installed-linux-aarch64-cp313-post20-short-20260714-034729.analysis.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-031029-87330f2482d/validation-short-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-031029-87330f2482d/validation-short-exit-code
```

The selected coherent class was the six Giac command-completion mismatches.
Giac 1.9 reads its completion list from `share/giac/aide_cas`; the existing
companion relocated the executable and libraries but not that database, so
every completion query returned an empty list. Exact committed and pushed
source `396f11c604fd63438235c6bf825571bd7a8851c2` bundles the database, sets a
relative `XCAS_HELP` path in the companion wrapper, adds a real completion
selftest, allocates Sagelite `10.9.post21` and Giac runtime `10.9.post1`, and
raises both Giac dependency floors.

The exact-commit native companion wheel is:

```text
sagelite_giac_runtime-10.9.post1-py3-none-manylinux_2_28_aarch64.whl
sha256=98393e6bcf9e8079b7aad543deeb22d727896acbbfded9a5fd76e285b5880b0f
size=126275378
```

A fresh minimal CPython 3.13 container installed that exact wheel, found the
packaged 718,654-byte completion database, and retrieved `cas_setup` and
`case` from the bundled Giac without inherited Sage or library paths. Before
the exact rebuild, the same change was installed over the untouched failed
`post20` environment: all Giac interface doctests passed, 1,873 commands
were returned, and the new selftest probe passed. The exact companion and
focused artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-giac-post1-20260714-042000-396f11c604f/wheelhouse/SHA256SUMS
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-giac-post1-20260714-042000-396f11c604f/validation/focused-giac.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-giac-post1-20260714-042000-396f11c604f/validation/focused-giac-exit-code
```

After preserving the `post20` wheelhouse, summary, reduced analysis,
metadata, and logs, the iteration removed only its 21 GiB disposable failed
install. The guest then had 108,363,984,896 bytes free, above the 100 GiB
heavy-build threshold. Exactly one native `post21` build and one gated
validation watcher started as `sagelite-post21-build.service` and
`sagelite-post21-validate.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-042300-396f11c604f
```

Both services remained active after the launching SSH session exited. The
validator will add the exact Giac `post1` wheel to the new build output,
assemble a fresh strict closure, and run wheel-only `--optional sage` short
and full gates only after the primary build succeeds. The public manifest
remains unchanged at 177 wheels and fourteen `post8`/`post9` Sagelite
primaries. No publication was attempted, no `post21` primary is claimed, and
the cell remains below `full`.

## Post21 native wheel-build checkpoint

The scheduled reconciliation at `2026-07-14T04:31:56Z` found exactly the two
intended guest user-systemd services active. The build service owned the sole
CIBW container, and the validation service remained correctly blocked on the
absent build exit-code artifact. No validation container or completed
`post21` wheel existed. The exact source checkout was clean at
`396f11c604fd63438235c6bf825571bd7a8851c2` and reported Sagelite
`10.9.post21`; the actual manylinux build container reported native Linux
`aarch64`.

The build had reached the Sagelite extension-compilation phase. Its Ninja log
contained 710 records and continued to advance, while live GCC processes used
approximately all eight guest CPUs. This supplied forward-progress evidence
while the top-level command log was buffered after announcing the
`sagelib-10.9.post21` package build. None of `exit-code`,
`follow-on-exit-code`, `validation-short-exit-code`, or
`validation-full-exit-code` existed.

The Linux guest had 102,720,352,256 bytes free after the build began above the
100 GiB heavy-build threshold. The outer macOS host had about 183 GiB free on
`/Volumes/sage`, and both the controller and `host` bulk filesystems had about
103 GiB free. The directly fetched public `dev/manifest.json` remained
unchanged at 177 wheel entries and fourteen Sagelite primaries, all from
`post8` and `post9`; no `post21` primary is public. No duplicate build,
validation, or publication was started. The cell remains below `full`, and
this checkpoint makes no wheel, install, smoke, or full-suite claim.

## Post21 wheel completion and strict-gate start

The exact-SHA native build completed with exit code zero at approximately
`2026-07-14T04:55Z`. Its source checkout is clean at
`396f11c604fd63438235c6bf825571bd7a8851c2` with Sagelite
`10.9.post21`. The build produced:

```text
sagelite-10.9.post21-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=d01d31a37855dbd8ae4b85d794a5261c136ddf92e860045cd476b283935f6b72
size=227682709

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=9d0473b560a2e8924ded818217b7547d87dc4aabcadd2b1422e02675077bcc28
size=66578984
```

The validation watcher added the separately built exact-commit Giac `post1`
wheel and assembled a fresh strict closure of one primary, 68 companions,
and 108 third-party wheels. The 177 staged wheels total 16,513,416,841 bytes,
with wheelhouse digest
`393433ca7384df3275274f8d8641b57087ea9d57db419666ea359fa1bd63ca3d`.
Every repaired-wheelhouse filename, dependency, tag, ABI, architecture, and
version preflight passed.

The fresh native Linux aarch64 wheel-only installation of
`sagelite[all-needed-extras]==10.9.post21` and `python -m pip check` passed.
Runtime manifest and summary collection also completed, and every
`sagelite-selftest` probe passed, including the new Giac command-completion
probe. At `2026-07-14T05:04:31Z`, the installed
`--optional=sage --short 600` sweep was active across eight workers in the
only Sagelite container, using approximately all eight guest CPUs. The
durable `sagelite-post21-validate.service` will start a separate full sweep
only if that gate passes. Neither validation exit-code artifact exists yet,
so no short-suite or full-suite pass is claimed. The current artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-042300-396f11c604f/wheelhouse
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-042300-396f11c604f/validation-wheelhouse/SHA256SUMS
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-042300-396f11c604f/validation/short-post21/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-042300-396f11c604f/command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-042300-396f11c604f/validation-short-command.log
```

The Linux guest had 84,604,633,088 bytes free, above the 30 GiB test-only
threshold; `/Volumes/sage` had about 166 GiB free, and the controller and
`host` bulk filesystems each had about 103 GiB free. The public manifest was
fetched with a pip user agent and remained at 177 wheels and fourteen
`post8`/`post9` Sagelite primaries; no `post21` primary is public. No
duplicate work or publication was started, and the cell remains below
`full`.

## Post21 short failure and post22 compiler correction

The durable `post21` watcher finished without leaving an active service,
doctest process, or container. The native build exit code is zero, while the
strict short gate and its watcher both exited one. The fresh 177-wheel
preflight, wheel-only install of
`sagelite[all-needed-extras]==10.9.post21`, `python -m pip check`, runtime
manifest, every selftest probe, and packaged pytest with 213 passed and two
skipped all passed. The installed `--optional=sage --short 600` sweep tested
3,954 modules and failed ten. Its authoritative evidence is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-042300-396f11c604f/validation/short-post21/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-042300-396f11c604f/validation/short-post21/doctest-installed-linux-aarch64-cp313-post21-short-20260714-045904.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-042300-396f11c604f/validation/short-post21/doctest-installed-linux-aarch64-cp313-post21-short-20260714-045904.analysis.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-042300-396f11c604f/validation-short-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-042300-396f11c604f/validation-short-exit-code
```

The selected coherent class was the absent installed compiler toolchain and
`pkg-config` command. Four modules failed while dynamically compiling Cython
snippets because the clean `python:3.13-slim-bookworm` image has no `gcc`:
`sage.misc.session`, `sage.repl.ipython_tests`,
`sage.rings.polynomial.ore_polynomial_element`, and
`sage.rings.tate_algebra_ideal`. `sage.env` separately exposed an `OSError`
from the Python `pkgconfig` wrapper instead of its documented
`PackageNotFoundError` when the command itself was unavailable. The remaining
FriCAS, GAP3, fpylll, Qepcad, and polynomial-power failures are independent
classes and are not treated as fixed.

The `post22` source correction adds the official standalone `ziglang` wheel to
the `all-needed-extras` validation closure on the three target platforms.
Ad hoc Cython builds preserve explicit `CC` and `CXX`, prefer an available
interpreter-configured compiler, and otherwise use `zig cc` and `zig c++`.
Because the standalone Zig wheel does not include OpenMP headers, installed
Cython aliases omit inherited OpenMP flags only while that fallback is active;
the existing doctest then correctly exercises its documented serial path.
Explicit required `pkgconfig` lookups now translate an absent command into
`PackageNotFoundError`, while optional and installed-default probes remain
skippable.

A non-authoritative focused probe installed the exact
`ziglang-0.16.0-py3-none-manylinux_2_17_aarch64.manylinux2014_aarch64.musllinux_1_1_aarch64.whl`
in the preserved failed environment and mounted the corrected source modules
read-only. With no `CC`, `CXX`, Sage build paths, or system packages supplied,
all 970 examples in `sage.env` and the four compiler-dependent modules passed.
The new and existing environment unit tests reported 114 passed. Durable
focused artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post22-compiler-focused-20260714-053605-5f7ab60cd13/validation/focused-doctests-2.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post22-compiler-focused-20260714-053605-5f7ab60cd13/validation/focused-doctests-2-exit-code
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post22-compiler-focused-20260714-053605-5f7ab60cd13/validation/focused-pytest.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post22-compiler-focused-20260714-053605-5f7ab60cd13/validation/focused-pytest-exit-code
```

On the controller, Python compilation, dependency-marker parsing,
`git diff --check`, all 43 wheelhouse-validator and runtime-regression tests,
and the two relevant all-needed-extra metadata tests passed. The broader
companion metadata file still has eleven unrelated pre-existing failures from
stale generated egg metadata, the existing aarch64 Regina marker, and the
Maxima helper test namespace; none overlaps this change. Sagelite advances to
`10.9.post22`. This is focused source evidence only: an exact committed
`post22` wheel, fresh install, short gate, and full sweep remain required.

At reconciliation, the Linux guest reported native `aarch64` and about 79 GiB
free, above the 30 GiB test-only threshold but below the 100 GiB heavy-build
threshold. `/Volumes/sage` had about 166 GiB free. The public
`dev/manifest.json` remained unchanged at 177 wheel entries and fourteen
`post8`/`post9` Sagelite primaries. No publication was attempted, and the cell
remains below `full`.

## Post22 exact-SHA rebuild start

The next scheduled reconciliation found no active Sagelite service, process,
or container in the native Linux backend. The public `dev/manifest.json` still
contained 177 wheel entries and fourteen Sagelite primaries, all from `post8`
and `post9`; no local CPython 3.13 aarch64 primary was assumed public.

The completed failed `post21` run retained its strict wheelhouse, validation
summary, install metadata, reduced analysis, and logs. The iteration removed
only its 22,107,787,264-byte disposable validation install, plus disposable
source and focused-build trees from the superseded `post16` run and an exited
automation-owned `post12` container. The guest then had 108,451,287,040 bytes
free, above the 100 GiB heavy-build threshold.

Exactly one native build and one gated validation watcher started as the guest
user-systemd services `sagelite-post22-build.service` and
`sagelite-post22-validate.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-compiler-20260714-054623-2efaab7ea74e
```

The build records committed and pushed source
`2efaab7ea74e19c6169c3da8eca5e1b28cf9697c`, Sagelite `10.9.post22`, and the
native Linux `aarch64` CPython 3.13 CIBW contract. The validation watcher is
blocked on the build exit-code artifact. After a successful build it will
replace the inherited primary and matching rebuilt companions, add the pinned
compatible `ziglang 0.16.0` aarch64 wheel to the strict closure, and run fresh
wheel-only `--optional sage` short and full gates in sequence. Both services
remained active after their launching SSH session exited. No `post22` wheel,
install, smoke, or suite result is claimed yet, and no publication was
attempted.

## Post22 native wheel-build checkpoint

The scheduled reconciliation at `2026-07-14T06:01:45Z` found exactly the two
intended guest user-systemd services active. The build service owned the sole
CIBW container, while the validation watcher remained correctly blocked on
the absent build exit-code artifact. No validation container, completed wheel,
or validation exit-code artifact existed.

The source checkout was clean at the exact committed SHA
`2efaab7ea74e19c6169c3da8eca5e1b28cf9697c` and reported Sagelite
`10.9.post22`. The actual build container reported Linux `aarch64`. It had
reached the Sagelite extension-build phase, with native compiler processes
active across approximately all eight guest CPUs during a 15-second sample.
This supplied forward-progress evidence while the top-level command log was
buffered after announcing the `sagelib-10.9.post22` package build.

The Linux guest had about 94 GiB free after the build began above the 100 GiB
heavy-build threshold. The outer macOS host had about 181 GiB free on
`/Volumes/sage`, and the controller had about 103 GiB free on `/scratch`.
The directly fetched public `dev/manifest.json` remained unchanged at 177
wheel entries and fourteen Sagelite primaries, all from `post8` and `post9`;
no `post22` primary is public. No duplicate build, validation, or publication
was started. The cell remains below `full`, and this checkpoint makes no new
wheel, install, smoke, or full-suite claim.

## Post22 wheel completion and strict-gate runtime checkpoint

The exact-SHA native build completed with exit code zero at
`2026-07-14T06:20:20Z`. Its source checkout is clean at
`2efaab7ea74e19c6169c3da8eca5e1b28cf9697c` with Sagelite
`10.9.post22`. It produced:

```text
sagelite-10.9.post22-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=47c2fdb65f31416854cf8f9b13cb0691e814b2b37a1dcb4251855ed5f01a6c24
size=227683669

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=23d51565e76abeaaaac9d1a896bc13672612d041eb52ff87ab9113ecbdce5c60
size=66578984
```

The validation watcher added the compatible pinned
`ziglang 0.16.0` aarch64 wheel and assembled a fresh strict closure of one
primary, 68 companions, and 109 third-party wheels. The 178 staged wheels
total 16,608,425,913 bytes, with validator wheelhouse digest
`e892d24d54d66f2ccba7b0ba0d5c8cfe3cf501bf03b5e921e45fc5d19d4db985`
and `SHA256SUMS` file digest
`82bb1d0b3a0d9bf273595039fe0233f1e01033a1ae3f1ce4235b7d9121be3755`.
Every repaired-wheelhouse filename, dependency, tag, ABI, architecture, and
version preflight passed.

The fresh native Linux aarch64 wheel-only installation of
`sagelite[all-needed-extras]==10.9.post22` and `python -m pip check` passed.
Runtime manifest and summary collection completed, and every
`sagelite-selftest` probe passed. The installed `--optional=sage --short 600`
sweep then started all 3,953 modules with eight workers. The Zig fallback is
being invoked by installed Cython compilation, but the still-running sweep
has exposed that the general `sage.misc.cython` examples also require
packaged development headers such as `factory/factory.h`. This is a remaining
installed compiler-runtime closure issue rather than a successful short gate.
The log has also reproduced the independent GAP3 protocol, fpylll strategy
data, and QEPCAD runtime classes already present in the `post21` inventory.

At the checkpoint, `sagelite-post22-validate.service` was active and owned the
only Sagelite container, which reported native `aarch64` and sustained
multi-core progress. No short-validation exit code or reduced final analysis
existed. The Linux guest had 84,054,908,928 bytes free, above the 30 GiB
test-only threshold; `/Volumes/sage` had about 165 GiB free, and the
controller had about 103 GiB free on `/scratch`. The public
`dev/manifest.json` remained unchanged at 177 wheels and fourteen
`post8`/`post9` Sagelite primaries; no `post22` primary is public. No duplicate
work or publication was started, and this cell remains below `full`.

## Post22 short result and focused post23 header repair

The durable `post22` validation finished with short-gate and watcher exit code
one; no service, doctest process, or container remained active. The native
wheel build retained exit code zero, and the strict 178-wheel closure had
already passed every preflight, fresh wheel-only installation, `pip check`,
runtime-manifest, and selftest probe. The completed `--optional=sage --short
600` sweep failed five of 3,954 modules:

```text
sage.misc.cython
sage.modules.free_module_integer
sage.interfaces.qepcad
sage.interfaces.gap3
sage.rings.polynomial.polynomial_element
```

The authoritative summary and reduced analysis are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-compiler-20260714-054623-2efaab7ea74e/validation/short-post22/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-compiler-20260714-054623-2efaab7ea74e/validation/short-post22/doctest-installed-linux-aarch64-cp313-post22-short-20260714-062352.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-compiler-20260714-054623-2efaab7ea74e/validation/short-post22/doctest-installed-linux-aarch64-cp313-post22-short-20260714-062352.analysis.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-compiler-20260714-054623-2efaab7ea74e/validation-short-exit-code
```

The first coherent failure class was `sage.misc.cython`. The repaired
CPython 3.13 primary contained no `sage/include` files, so installed dynamic
compilation could not find headers such as `factory/factory.h`. The Linux
repair helper had limited native-header injection to a `cp312-cp312` wheel.
Commit `ce7c50b0765e6cdeef70657857704632f4b42919` removes that ABI guard,
adds a repair regression assertion, and advances Sagelite to `10.9.post23`.

A focused wheel copied the exact `post22` primary and injected the native
prefix headers using the corrected repair behavior. It contains 3,375
`sage/include` entries, including `factory/factory.h`, and has:

```text
sha256=f22692cd06cf45abd864ec202e5cc193fb2f64fc72c993ceee89d8a9cf349efa
size=236229724
```

A fresh `python:3.13-slim-bookworm` install of the complete package from the
modified primary and preserved strict closure succeeded, and `pip check`
passed. Restoring the headers removed the fatal missing-header failure but
exposed Zig 0.16's linker-time bundled-libc++ nullability warning flood as
unexpected doctest output. Zig's parallel internal build interleaves that
stderr and does not propagate ordinary driver warning controls. Commits
`f3b76fa55628533db3e3227a93d336739e289269` and
`9ca961f7c25822c658cc5f4b412e00a7439ccabb` therefore filter only messages
whose complete warning-category set is the known
`-Wnullability-completeness` diagnostic from bundled libc++, while preserving
compiler errors, other warning categories, and complete diagnostics from
other sources.

The final exact-source focused rerun used files whose checksums match committed
SHA `9ca961f7c25822c658cc5f4b412e00a7439ccabb`. The dependency check passed,
all 115 environment and Cython regression tests passed, and all 48 installed
`sage.misc.cython` doctests passed. Its durable evidence is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post23-headers-focused-20260714-070720-ce7c50b0765e/validation/header-inventory.txt
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post23-headers-focused-20260714-070720-ce7c50b0765e/validation/focused-post23-exact-6.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post23-headers-focused-20260714-070720-ce7c50b0765e/validation/focused-post23-exact-6-exit-code
```

This is focused evidence, not an accepted wheel or short-suite result. The
other four `post22` failure modules remain unresolved until the rebuilt wheel
reaches the authoritative short gate.

After preserving the `post22` wheelhouse and all final logs, the iteration
removed only named automation-owned disposable installs, source copies, and a
superseded duplicate validation wheelhouse. The Linux guest then had about
101 GiB free, meeting the 100 GiB heavy-build threshold. A durable native
`post23` build started as `sagelite-post23-build.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-073737-9ca961f7c25
```

It records the clean pushed source SHA
`9ca961f7c25822c658cc5f4b412e00a7439ccabb` and the native Linux aarch64
CPython 3.13 CIBW contract. At this checkpoint the service is active, its
exit-code artifact does not exist, and no `post23` wheel or authoritative
install result is claimed. The public `dev/manifest.json` remains unchanged
at 177 wheels and fourteen `post8`/`post9` Sagelite primaries. No publication
was attempted, and the cell remains below `full`.

## Post23 native build progress and validation watcher

The scheduled reconciliation at `2026-07-14T08:01:29Z` found the exact-SHA
native build healthy and still active. The source checkout is clean and
detached at `9ca961f7c25822c658cc5f4b412e00a7439ccabb`, reports Sagelite
`10.9.post23`, and the sole CIBW build container runs on Linux `aarch64`.
The build had reached the 1,795-target native extension phase and continued to
own active compiler processes; no build exit-code or completed `post23` wheel
existed at this checkpoint.

The iteration started exactly one durable guest user-systemd validation
watcher, `sagelite-post23-validate.service`. It waits for the build's
`exit-code` artifact and, only after a zero result, will assemble the strict
wheel closure and run fresh wheel-only `--optional sage` short and full gates
in sequence. No validation container was active while the build was still
running.

The Linux guest had about 90 GiB free during the build, after starting above
the required 100 GiB heavy-build threshold. `/Volumes/sage` had about 177 GiB
free, and controller `/scratch` had about 103 GiB free. The directly fetched
public `dev/manifest.json` remained at 177 wheel entries and fourteen Sagelite
primaries, all from `post8` and `post9`; no `post23` artifact is public. No
duplicate build or publication was started, and this cell remains below
`full`.

## Post23 short result and focused post24 FPLLL repair

The exact-SHA native `post23` build completed with exit code zero and produced:

```text
sagelite-10.9.post23-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=d09d2087339ff6cb902542c4386b0a7c2140d9a96a4eb775097e7c2f6180a8de
size=236405480

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=4cd3134e6fb17e12c45e4a65f4b26874b2ce844db3d437bd56c704902729bdcb
size=66578984
```

The validation watcher assembled a fresh strict closure of 178 wheels totaling
16,617,147,724 bytes. Its `SHA256SUMS` file has digest
`1204220946779b02dfea5b5e9f2acad67d9e852fcdd8465422ed8a9ac055db86`.
Every repaired-wheelhouse filename, dependency, tag, ABI, architecture, and
version preflight passed. The fresh wheel-only installation of
`sagelite[all-needed-extras]==10.9.post23`, `python -m pip check`, runtime
manifest, selftest, and packaged pytest all passed; pytest reported 215 passed
and two skipped.

The installed `--optional=sage --short 600` sweep nevertheless exited one. Its
reduced analysis covered 3,954 modules and found three failures:

```text
sage.modules.free_module_integer
sage.interfaces.qepcad
sage.interfaces.gap3
```

The authoritative artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-073737-9ca961f7c25/validation/short-post23/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-073737-9ca961f7c25/validation/short-post23/doctest-installed-linux-aarch64-cp313-post23-short-20260714-081505.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-073737-9ca961f7c25/validation/short-post23/doctest-installed-linux-aarch64-cp313-post23-short-20260714-081505.analysis.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-073737-9ca961f7c25/validation-short-exit-code
```

The selected coherent failure class was FPLLL strategy relocation. Sagelite
already redirected `fpylll.config` and the public `BKZ.DEFAULT_STRATEGY`
attribute to the packaged `sagelite-fplll-data` file. However,
`BKZ.EasyParam` reads a separate module-level value copied by the Cython
`fpylll.fplll.bkz_param` module during import. The stale private copy caused
`L.shortest_vector()` to raise `RuntimeError: Cannot open strategies file`,
and the subsequent virtual doctest observed the unmatched signal guard.

Committed and pushed source `bd7e96a663bc612dcebb1abab34a7cba796ed75b`
updates that private path copy alongside the public values, adds a regression
assertion, and advances Sagelite to `10.9.post24`. Seven focused environment
tests pass locally. A native focused probe mounted the exact committed
`env.py` over the otherwise untouched failed `post23` install. It verified all
three FPLLL path copies point to the existing companion strategy file,
constructed `BKZ.EasyParam`, and passed all 152 doctests in
`sage.modules.free_module_integer`. Its durable evidence is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post24-fplll-focused-20260714-083615-bd7e96a663b/run-metadata.txt
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post24-fplll-focused-20260714-083615-bd7e96a663b/validation/focused.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post24-fplll-focused-20260714-083615-bd7e96a663b/validation/focused-exit-code
```

This is focused evidence, not a repaired `post24` wheel or short-suite pass.
QEPCAD and GAP3 remain independent failure classes. After preserving the
failed wheelhouse and final validation artifacts, the iteration removed only
named disposable installs and superseded source trees. The guest then had
106,339,316 KiB free, above the 100 GiB heavy-build threshold.

Exactly one native `post24` build and one gated validation watcher started as
`sagelite-post24-build.service` and `sagelite-post24-validate.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-083918-bd7e96a663b
```

The build records exact pushed source
`bd7e96a663bc612dcebb1abab34a7cba796ed75b` and the native Linux aarch64
CPython 3.13 CIBW contract. The watcher waits for the build exit artifact and
will assemble a fresh strict closure, then run the short and full
`--optional=sage` gates in sequence after build success. No `post24` wheel,
install, smoke, short, or full result is claimed yet. The public manifest
remains at 177 wheels and fourteen `post8`/`post9` Sagelite primaries; no
publication was attempted, and this cell remains below `full`.

## Post24 native compilation checkpoint

The scheduled reconciliation at `2026-07-14T09:01:41Z` found exactly the two
intended guest user-systemd services active. The build service, main PID
`2249624`, owned the sole CIBW container, while the validation watcher, main
PID `2249985`, remained correctly blocked on the absent build exit-code
artifact. No validation container, completed `post24` wheel, or validation
exit-code artifact existed.

The exact source checkout was clean at committed SHA
`bd7e96a663bc612dcebb1abab34a7cba796ed75b`. The actual build environment
reported native Linux `aarch64` and had reached the Sagelite native-extension
compilation phase. Concurrent GCC and ECL processes used approximately all
eight guest CPUs, providing forward-progress evidence while the top-level
build log was buffered.

The Linux guest had about 91 GiB free after the build began above the 100 GiB
heavy-build threshold. The outer macOS host had about 178 GiB free on
`/Volumes/sage`, and the controller had about 103 GiB free on `/scratch`.
The directly fetched public `dev/manifest.json` remained unchanged at 177
wheel entries and fourteen Sagelite primaries, all from `post8` and `post9`;
no `post24` primary is public. No duplicate build, validation, or publication
was started. The cell remains below `full`, and this checkpoint makes no new
wheel, install, smoke, or full-suite claim.

## Post24 wheel completion and short-gate result

The exact-SHA native build completed with exit code zero at
`2026-07-14T09:13:11Z`. Its source checkout is clean at
`bd7e96a663bc612dcebb1abab34a7cba796ed75b` and produced:

```text
sagelite-10.9.post24-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=0253c921c1430fc09410b492bf83aad01499f15d4545ffe1c5fb12001d8f7363
size=236405650

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=8740d52ed7cdbe15a93f8f85586e0c2a09e020bbaf1a4b010a7a62a3af9f6a7d
size=66578984
```

The validation watcher assembled a fresh strict closure of one primary, 68
companions, and 109 third-party wheels. The 178 staged wheels total
16,617,147,894 bytes, with validator wheelhouse digest
`d5c44a3057e74ab17519bfcd3747e0a867f65abf4360ba37fc6bf3c0841a29a7`
and `SHA256SUMS` file digest
`6894e30c80e9290f7ca2d1e08dbcb20347f282f5d45ec964ec88c795a7f1fe5b`.
Every repaired-wheelhouse filename, dependency, tag, ABI, architecture, and
version preflight passed.

The fresh native Linux aarch64 wheel-only installation of
`sagelite[all-needed-extras]==10.9.post24`, `python -m pip check`, runtime
manifest, and every `sagelite-selftest` probe passed. Packaged pytest reported
215 passed and two skipped. The installed `--optional=sage --short 600` sweep
failed three of 3,954 modules:

```text
sage.interfaces.gap3
sage.interfaces.qepcad
sage.rings.polynomial.polynomial_element
```

The FPLLL relocation failure from `post23` is absent: the exact committed
correction passed the authoritative fresh-wheel gate. The remaining failures
are independent classes. GAP3 returned protocol and formatting results that
the interface did not parse as expected. QEPCAD aborted during startup with
`std::bad_alloc`. Two large polynomial-power examples raised
`RuntimeError: Aborted` in FLINT's `nmod_poly` exponentiation. The gated
watcher correctly did not start the full sweep. Its authoritative artifacts
are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-083918-bd7e96a663b/validation/short-post24/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-083918-bd7e96a663b/validation/short-post24/doctest-installed-linux-aarch64-cp313-post24-short-20260714-091649.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-083918-bd7e96a663b/validation/short-post24/doctest-installed-linux-aarch64-cp313-post24-short-20260714-091649.analysis.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-083918-bd7e96a663b/validation-short-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-083918-bd7e96a663b/validation-short-exit-code
```

After validation, no Sagelite service, process, or container remained active.
The Linux guest had 84,848,066,560 bytes free, above the 30 GiB test-only
threshold; `/Volumes/sage` had about 165 GiB free, and controller `/scratch`
had about 103 GiB free. The public `dev/manifest.json` remained at 177 wheels
and fourteen `post8`/`post9` Sagelite primaries; no `post24` primary is
public. No publication was attempted, and the cell remains below `full`.

## Post25 focused QEPCAD correction

A one-worker rerun of `sage.interfaces.qepcad` in the otherwise untouched
`post24` wheel-only install reproduced the same delayed `std::bad_alloc`, so
the failure was not caused by the eight-worker short sweep. Reducing QEPCAD's
configurable pool to `+N100000` cells also reproduced the failure.

The packaged aarch64 executable contains debug information. A disposable
`gdb` container caught the C++ exception and showed
`slwcistream::slwcistream` appending byte 255 to a string whose requested size
had reached 16,106,127,360 bytes. QEPCAD stored the result of
`istream::get()` in plain `char`; because plain `char` is unsigned on
aarch64, EOF became 255 and the configuration parser never terminated. The
focused artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post24-qepcad-focused-20260714-094500-bd7e96a663b/validation/qepcad-focused.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post24-qepcad-focused-20260714-094500-bd7e96a663b/validation/qepcad-gdb.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-post24-qepcad-focused-20260714-094500-bd7e96a663b/validation/gdb.commands
```

Committed and pushed source
`185c5adec4c628809f194932916a9bdef66db456` preserves EOF in an `int` in
both copies of QEPCAD's single-line stream parser and converts to `char` only
after excluding EOF. It advances Sagelite to `10.9.post25`, advances the
QEPCAD companion to `10.9.post1`, removes the CPython 3.12-only companion
build guard, and raises both dependency floors. The companion CI smoke and
`sagelite-selftest` now launch the real executable with an empty input stream,
require the startup banner and input prompt within 30 seconds, and reject
`bad_alloc` output.

The complete Sage QEPCAD patch stack applied cleanly to the checksummed 1.74
source. A focused C++ regression compiled with `-funsigned-char` parsed the
last configuration line and terminated correctly at EOF. Python compilation,
shell syntax, all 34 selftest unit tests, three focused QEPCAD/all-needed
metadata tests, and `git diff --check` passed. This is focused source evidence
only: an exact committed `post25` QEPCAD companion, primary wheel, fresh
install, short gate, and full sweep remain required. GAP3 and polynomial
exponentiation remain separate failure classes.

## Post25 exact-SHA rebuild start

After preserving the `post24` wheelhouse, summary, reduced analysis, metadata,
and logs, the iteration removed only its 21 GiB disposable validation install
and 1.5 GiB disposable source clone. The guest then had 108,556,218,368 bytes
free, above the 100 GiB heavy-build threshold.

Exactly one native build and one gated validation watcher started as the guest
user-systemd services `sagelite-post25-build.service` and
`sagelite-post25-validate.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-095806-185c5adec4c
```

The build records exact pushed source
`185c5adec4c628809f194932916a9bdef66db456`, Sagelite `10.9.post25`, and the
native Linux `aarch64` CPython 3.13 CIBW contract. The watcher is blocked on
the build exit artifact. After build success it will replace the inherited
primary and matching rebuilt companions, including QEPCAD `10.9.post1`, then
run fresh strict wheel-only `--optional sage` short and full gates in
sequence. Both services remained active after the launching SSH session
exited, with main PIDs `2349570` and `2349576`.

At launch, the guest had about 101 GiB free and `/Volumes/sage` had about 166
GiB free. The public `dev/manifest.json` remained at 177 wheels and fourteen
`post8`/`post9` Sagelite primaries, with no public `post25` primary. No
`post25` wheel, install, smoke, short, or full result is claimed yet, and no
publication was attempted.

## Post25 rebuilt-wheel result and cache-stamp diagnosis

The exact committed `post25` build completed with exit code zero and produced:

```text
sagelite-10.9.post25-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=c7686b254781769547f3723e2766c98728251073808375bb1c6706a890067d5e
size=236405886

sagelite_qepcad_runtime-10.9.post1-py3-none-manylinux_2_28_aarch64.whl
sha256=a5af91bf6f39e536de1808e76243a945bf862d62a53222775b6daf855d6bceeb
size=5242382

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=5b84498a5def60eb668b12d57ad40290ebcaa7cea15a95e8b2285aaa24157407
size=66578984
```

The watcher assembled a fresh strict closure of one primary, 68 companions,
and 109 third-party wheels. The 178 staged wheels total 16,617,147,300 bytes,
with validator wheelhouse digest
`ae4a9446001dfc44cad28604c33da67d8ce9a1fe06b4f4f281dd794930db213e`
and `SHA256SUMS` file digest
`e07ac26b71e4fb35807b27239862e3cb0e10b364bc1a261e06ea74dcd1e0f5c8`.
Every strict filename, dependency, tag, ABI, architecture, and version
preflight passed. The fresh wheel-only installation and `pip check` passed,
and packaged pytest reported 215 passed and two skipped.

Selftest nevertheless failed its new QEPCAD startup gate, and the installed
`--optional=sage --short 600` sweep failed four of 3,954 modules:

```text
sage.interfaces.gap3
sage.interfaces.qepcad
sage.misc.cython
sage.rings.polynomial.polynomial_element
```

QEPCAD still terminated with `std::bad_alloc`; therefore the rebuilt
`post1` companion did not validate the signedness fix. The authoritative
artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-095806-185c5adec4c/validation/short-post25/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-095806-185c5adec4c/validation/short-post25/doctest-installed-linux-aarch64-cp313-post25-short-20260714-103502.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-095806-185c5adec4c/validation/short-post25/doctest-installed-linux-aarch64-cp313-post25-short-20260714-103502.analysis.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-095806-185c5adec4c/validation-short-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-095806-185c5adec4c/validation-short-exit-code
```

A disposable debugger run against the installed `post25` binary reported the
local variable `c` in `slwcistream` still had type `char` and value 255. The
source patch was correct, but the persistent manylinux prefix already had a
`qepcad-1.74` install marker. Because the upstream package version had not
changed, `make qepcad` skipped compilation and the companion builder merely
repackaged the old executable under the new `post1` distribution version.

Committed and pushed source
`6d670ebaaa384dc2efcd4e15afac2a76610f1e6b` advances the Sage package to
`1.74.p1`, while continuing to resolve the checksummed `qepcad-1.74.tar.gz`.
This invalidates the cached install marker through the standard Sage package
patchlevel mechanism. It advances the QEPCAD companion to `10.9.post2`,
Sagelite to `10.9.post26`, and both dependency floors without reusing the
invalid `post1` filename. The real patch applies cleanly, a C++ regression
compiled with `-funsigned-char` terminates at EOF, and three focused metadata
and selftest tests pass.

## Post26 exact-SHA rebuild start

After preserving the `post25` wheelhouse, strict summary, reduced analysis,
metadata, and logs, the iteration removed only its 21 GiB disposable install
and 1.5 GiB disposable source clone. The guest then had 108,078,157,824 bytes
free, just above the 100 GiB heavy-build threshold.

Exactly one native build and one gated watcher started as
`sagelite-post26-build.service` and `sagelite-post26-validate.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-110419-6d670ebaaa3
```

The build records exact pushed source
`6d670ebaaa384dc2efcd4e15afac2a76610f1e6b`, Sagelite `10.9.post26`, and
the native Linux `aarch64` CPython 3.13 CIBW contract. The watcher waits for
the build exit artifact and will replace the inherited primary and rebuilt
companions, including QEPCAD `10.9.post2`, before running fresh strict
wheel-only `--optional sage` short and full gates. Both services survived the
launching SSH session, with main PIDs `2448681` and `2448692`.

The public manifest remained at 177 wheels and fourteen `post8`/`post9`
Sagelite primaries. No `post26` wheel, install, smoke, short, or full result is
claimed yet, and no publication was attempted.

## Post26 rebuilt-wheel result and Singular handoff diagnosis

The exact committed `post26` build completed with exit code zero and produced:

```text
sagelite-10.9.post26-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=78cc65f755bae9bc1f16d656746538ae61ee07190ef4b5d9db63743c0fedad47
size=236405887

sagelite_qepcad_runtime-10.9.post2-py3-none-manylinux_2_28_aarch64.whl
sha256=df93a79295aa444479e5e410d534899aa2574a886d58fe1c3aebaaab1a5f3980
size=5241590

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=e9242320c7157e98a60bb073caef32e604ba74fbf06b2e21c0009afa5c0f0f3d
size=66578984
```

The watcher assembled a fresh strict closure of 178 wheels totaling
16,617,146,509 bytes, with staged wheelhouse digest
`a1cae0c409cc7f9ac9b2b00757d3cce6f5b4da25a346e12c50b58a618a1c9555`.
Every strict filename, dependency, tag, ABI, architecture, version, and
repaired-primary preflight passed. The fresh wheel-only installation of
`sagelite[all-needed-extras]==10.9.post26` and `pip check` passed. Startup
selftest passed, including the rebuilt QEPCAD prompt probe, so the cached
unsigned-`char` executable and its `bad_alloc` are fixed.

The installed short sweep nevertheless logged 66 failures in
`sage.interfaces.qepcad` and ultimately timed out that module. The rebuilt
executable remained alive through startup but died with signal 13 on its
first `go` command, leaving echoed commands such as `go  &` in place of
answers. QEPCAD's applied boolean-Singular patch launches uppercase
`Singular` through `PATH`; the wheel-only process instead knew the companion
only by its private package path. A focused run against the untouched install
reproduced the failure, while prepending the directory returned by
`sagelite_singular_runtime.runtime.executable_path()` made the same
`qepcad(a > b)` operation return `b - a < 0`.

After the failure class was established, the iteration stopped the remaining
failed short sweep rather than starting a full run. Its exit code is 137 from
that deliberate stop. The partial reducer reports QEPCAD's timeout and the
already separate GAP3 runtime failure. Authoritative and focused artifacts
are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-110419-6d670ebaaa3/validation/short-post26/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-110419-6d670ebaaa3/validation/short-post26/doctest-installed-linux-aarch64-cp313-post26-short-20260714-114454.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-110419-6d670ebaaa3/validation/short-post26/doctest-installed-linux-aarch64-cp313-post26-short-20260714-114454.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-110419-6d670ebaaa3/analysis-post26/doctest-installed-linux-aarch64-cp313-post26-short-partial-20260714-120351.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-110419-6d670ebaaa3/analysis-post26/doctest-installed-linux-aarch64-cp313-post26-short-partial-20260714-120351.analysis.json
```

Committed and pushed source
`b9c7d52af26cf35581ba17b5109a22b6da3aa1b8` advances Sagelite to
`10.9.post27`, exposes the Singular companion bindir only in QEPCAD's child
environment, makes the `qepcad` extra request both companions, and strengthens
selftest from a startup-only check to the Singular-backed elimination above.
Twelve focused QEPCAD, selftest, feature, and companion-metadata tests passed;
the broader metadata file still has eleven unrelated pre-existing failures.

## Post27 exact-SHA rebuild start

After preserving the `post26` wheelhouse, strict summary, selftest, full
failure log, stats, and partial reduced analysis, the iteration removed only
its 21 GiB disposable install and 1.5 GiB disposable source clone. The guest
then had 111,159,603,200 bytes free, above the 100 GiB heavy-build threshold;
`/Volumes/sage` had about 185 GiB free.

Exactly one native build and one gated watcher started as
`sagelite-post27-build.service` and `sagelite-post27-validate.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-120609-b9c7d52af26
```

The build records exact pushed source
`b9c7d52af26cf35581ba17b5109a22b6da3aa1b8`, Sagelite `10.9.post27`, and
the native Linux `aarch64` CPython 3.13 CIBW contract. The watcher waits for
the build exit artifact and will assemble a fresh strict wheel closure before
running wheel-only `--optional sage` short and full gates. Both services
survived the launching SSH session, with main PIDs `2548082` and `2548087`.

The public manifest remained at 177 wheels and fourteen `post8`/`post9`
Sagelite primaries. No `post27` wheel, install, smoke, short, or full result is
claimed yet, and no publication was attempted.

## Post27 native compilation checkpoint

The scheduled reconciliation at `2026-07-14T12:34:29Z` found exactly the two
intended guest user-systemd services active. The build service, main PID
`2548082`, owned the sole CIBW container, while the validation watcher, main
PID `2548087`, remained correctly blocked on the absent build exit artifact.
No validation container or short/full validation exit artifact existed.

The exact source checkout was clean at committed SHA
`b9c7d52af26cf35581ba17b5109a22b6da3aa1b8`. The native build environment
reported Linux `aarch64` and had reached Sagelite extension compilation.
Concurrent Cython, GCC, and G++ processes used all eight guest CPUs even while
the top-level build log was buffered, providing forward-progress evidence.

The Linux guest had 104,775,196,672 bytes free after the build began above
the 100 GiB heavy-build threshold. The outer macOS host had about 186 GiB
free on `/Volumes/sage`, and controller `/scratch` had about 103 GiB free.
The controller was clean at `f7af7064ca1a02e7241de9cb87f92dfec57d4364`,
and `origin/develop` reported the same SHA. The directly fetched public
`dev/manifest.json` remained unchanged at 177 wheel entries and fourteen
Sagelite primaries, all from `post8` and `post9`; no `post27` primary is
public. No duplicate build, validation, or publication was started. This
checkpoint makes no new wheel, install, smoke, short, or full-suite claim.

## Post27 rebuilt-wheel result and package-context diagnosis

The exact committed `post27` build completed with exit code zero and produced:

```text
sagelite-10.9.post27-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=e30df39da85a1fe7861e787b9ecda714f5dbacf28f46422bd8fa8fc23fe869d9
size=236406288

sagelite_qepcad_runtime-10.9.post2-py3-none-manylinux_2_28_aarch64.whl
sha256=ea2f208da7703806902e36125c4ad20ff850b6b7007dd7666314a806a1460def
size=5241590

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=a01437b5cc2b38e684f1d1b8ad706075dc1e24f490f68c155032b5efaec2b41d
size=66578984
```

The watcher assembled a fresh strict closure of 178 wheels. Every repaired
wheelhouse preflight passed, and a fresh wheel-only installation of
`sagelite[all-needed-extras]==10.9.post27` plus `pip check` passed. The
strengthened QEPCAD selftest nevertheless returned an empty answer, so no
smoke result is claimed. The bounded doctest sweep was deliberately stopped
after this coherent failure class was established; its durable short and
watcher exit codes are 137.

The failure was in the new Singular companion discovery rather than the
rebuilt QEPCAD executable. The helper loaded `runtime.py` under a synthetic
top-level module name, but that runtime locates its executable with
`importlib.resources.files(__package__)`. Without the real package context,
the lookup failed, `_qepcad_singular_bindir()` returned `None`, and the child
command never received the intended `PATH` entry.

The `post28` correction imports the optional runtime with its real package
context and makes the test fixture exercise the same `importlib.resources`
behavior. In the native CPython 3.13 validation image, 38 focused QEPCAD and
selftest tests passed. Injecting only the corrected module into the untouched
failed install made `_qepcad_singular_bindir()` return the companion bindir,
added it to the QEPCAD child command, and made the exact strengthened
`_check_qepcad_runtime()` pass. This is focused regression evidence, not
fresh-install acceptance. Durable artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-120609-b9c7d52af26/validation/short-post27/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-120609-b9c7d52af26/validation/short-post27/doctest-installed-linux-aarch64-cp313-post27-short-20260714-130005.selftest.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-120609-b9c7d52af26/validation-short-exit-code
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-120609-b9c7d52af26/focused-post28/focused-unit.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-120609-b9c7d52af26/focused-post28/focused-unit-passed
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-120609-b9c7d52af26/focused-post28/focused-qepcad.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-120609-b9c7d52af26/focused-post28/focused-qepcad-passed
```

## Post28 exact-SHA rebuild start

The correction was committed and pushed as
`f239768d9a1c3f8b25e6926370c19095e386f5e3`, advancing Sagelite to
`10.9.post28`. The verified `origin/develop` SHA matched that commit before
the rebuild started.

After preserving the `post27` wheels, strict summary, selftest log, partial
doctest log, and focused evidence, the iteration removed only the 21 GiB
disposable failed install. The guest then had 109,275,881,472 bytes free,
above the 100 GiB heavy-build threshold.

Exactly one native build and one gated validation watcher started as
`sagelite-post28-build.service` and `sagelite-post28-validate.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-131434-f239768d9a1
```

The services survived the launching SSH session with main PIDs `2626199` and
`2626222`. The clean source checkout reports the exact pushed SHA, and the
actual manylinux container reports Linux `aarch64`. The watcher will assemble
a fresh strict 178-wheel closure and run wheel-only `--optional sage` short
and full gates in sequence only after build success.

At launch, `/Volumes/sage` had about 186 GiB free. The directly fetched public
manifest remained unchanged at 177 wheels and fourteen Sagelite primaries,
all from `post8` and `post9`. No `post28` wheel, install, smoke, short, or full
result is claimed yet, and no publication was attempted.

## Post28 native compilation checkpoint

The scheduled reconciliation at `2026-07-14T13:32:31Z` found exactly the two
intended guest user-systemd services active. The build service, main PID
`2626199`, owned the sole CIBW container, while the validation watcher, main
PID `2626222`, remained correctly blocked on the absent build exit artifact.
No validation container, completed `post28` wheel, or validation exit-code
artifact existed.

The source checkout was clean at exact committed and pushed SHA
`f239768d9a1c3f8b25e6926370c19095e386f5e3` and reported Sagelite
`10.9.post28`. The actual build environment reported native Linux `aarch64`.
Its Sagelib log had reached compiled extension target 1,105 of 1,794 and was
growing, while concurrent compiler processes sustained approximately all
eight guest CPUs. This supplies direct forward-progress evidence rather than
relying on the buffered top-level log.

The Linux guest had 100,504,064,000 bytes free, after the build began above
the 100 GiB heavy-build threshold. The outer macOS host had about 181 GiB free
on `/Volumes/sage`, and controller `/scratch` had 110,064,209,920 bytes free.
The directly fetched public `dev/manifest.json` remained unchanged at 177
wheel entries and fourteen Sagelite primaries, all from `post8` and `post9`;
no `post28` primary is public. No duplicate build, validation, or publication
was started. The cell remains below `full`, and this checkpoint makes no new
wheel, install, smoke, short, or full-suite claim.

## Post28 build, strict short gate, and QEPCAD aarch64 GC diagnosis

The exact committed `post28` build from
`f239768d9a1c3f8b25e6926370c19095e386f5e3` completed successfully. It
produced the following repaired native Linux aarch64 artifacts:

```text
sagelite-10.9.post28-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=5ec6c7ccf0287566f923f2caee4484df7b2b009a1dad997bbcca51612042d598
size=236406281

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=7b75294227c0cb4dac6abac0ce3d5b3965bc4ee36041eb169eeefe701194f5b3
size=66578984

sagelite_qepcad_runtime-10.9.post2-py3-none-manylinux_2_28_aarch64.whl
sha256=49742fa225993f3b873ad1a41339901a07ad25d4565afff3c3ba3635bfbc2e34
size=5241590
```

The gated watcher assembled a fresh strict 178-wheel closure. Wheelhouse
preflight, wheel-only installation of `sagelite[all-needed-extras]`, `pip
check`, and `sagelite-selftest` all passed. The 3,954-module short installed
doctest sweep exited 1, so the full gate did not start. Its thirteen failed
examples comprised eight independent GAP3 protocol failures, two independent
`polynomial_element` FLINT aborts, and three QEPCAD failures. Two QEPCAD
failures were exact command-string expectations made stale by the intentional
child `PATH`; the remaining complex CAD operation returned an empty answer.
No publication was attempted.

Direct reproduction showed that the complex QEPCAD operation segfaulted in
`ADV -> MBPROD -> AFCSBM -> AFCSBMDB -> CONSTRUCT -> TICAD -> QEPCAD` on
aarch64, while the same input passed on x86_64. Disabling Singular did not
change the crash. The actual defect was SACLIB's conservative collector:
`GC.c` tried to force register spills with sixteen dummy `register int`
arguments, but aarch64 callers can retain live SACLIB handles in callee-saved
x19-x29. The collector scanned the stack without those roots and reclaimed
live matrices. A broad `setjmp` experiment made the exact regression pass ten
times and confirmed the missing-register diagnosis.

The focused production correction advances SACLIB to `2.2.8.p1` and QEPCAD
to `1.74.p2`. On aarch64, SACLIB now explicitly stores x19-x28 and starts its
scan at the GC frame boundary, which also includes the caller's saved x29.
The linked binary's disassembly contains all five register-pair stores. In a
native manylinux container, the exact complex operation with its documented
3,000,000-cell allocation returned
`2 x - 1 > 0 /\\ z > 0 /\\ z - y < 0 /\\ 3 z + 3 y + x - 1 < 0` in ten of
ten runs. The one-million-cell form still reports 94,553 cells reclaimed,
essentially identical to the broad experiment's 94,557 and below SACLIB's
100,000 threshold; this regression is documented upstream with the explicit
three-million-cell allocation.

The change also advances the QEPCAD runtime companion to `10.9.post3`, raises
both dependency floors, advances Sagelite to `10.9.post29`, and makes
`sagelite-selftest` exercise the complex three-million-cell operation. These
are focused source and rebuilt-runtime results only. A fresh committed
`post29` primary and `post3` companion build, wheel-only installation, short
gate, and full gate are still required. Durable evidence is under:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-131434-f239768d9a1/validation/short-post28
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-131434-f239768d9a1/validation-short-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-131434-f239768d9a1/focused-post28-qepcad/qepcad-gdb.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-131434-f239768d9a1/focused-post28-qepcad/qepcad-valgrind.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-131434-f239768d9a1/focused-post28-qepcad/setjmp-register-fix/gc-frame-boundary-disassembly.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-131434-f239768d9a1/focused-post28-qepcad/setjmp-register-fix/frame-boundary-container-3000000-failures
```

## Post29 exact-SHA rebuild start

The aarch64 GC correction and its whitespace-only patch normalization were
committed and pushed as `c0889e8bd67` and `37e1224bcce`, respectively. The
build source revision, verified against `origin/develop` before launch, is
`37e1224bcce63056cdb61734e4e037986965ff94` and reports Sagelite
`10.9.post29` plus QEPCAD runtime `10.9.post3`.

The disposable `post28` validation install was removed after its strict logs,
wheel closure, and focused diagnostic artifacts were preserved. This raised
guest free space to 107,352,309,760 bytes, above the 100 GiB heavy-build
threshold. No competing container or heavy process was active.

Exactly one native build and one gated validation watcher are active as
`sagelite-post29-build.service` and `sagelite-post29-validate.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-154054-37e1224bcce
```

Their durable main PIDs are `2814796` and `2814800`. The clean source clone is
at the exact pushed SHA, and the actual manylinux build has begun resolving
its CPython 3.13 build environment. The watcher will reuse the preserved
strict closure, replace packages built by this run, and run fresh wheel-only
`--optional sage` short and full gates in sequence only after build success.
No `post29` wheel, install, smoke, short, or full result is claimed yet, and
no publication was attempted.

## Post29 native compilation checkpoint

The scheduled reconciliation at `2026-07-14T16:02:39Z` found exactly the two
intended guest user-systemd services active. The build service, main PID
`2814796`, owned the sole CIBW container, while the validation watcher, main
PID `2814800`, remained correctly blocked on the absent build exit artifact.
No validation container, completed `post29` wheel, or validation exit-code
artifact existed.

The source checkout was clean at exact committed and pushed SHA
`37e1224bcce63056cdb61734e4e037986965ff94` and reported Sagelite
`10.9.post29`. The actual build environment reported native Linux `aarch64`.
Its wheel-construction Ninja log advanced from 517 to 601 records during a
16-second sample while the container sustained approximately 800% CPU usage.
Concurrent Cython and ECL compiler processes supplied direct forward-progress
evidence while the top-level command log was buffered.

The Linux guest had about 90 GiB free after the build began above the 100 GiB
heavy-build threshold. The outer macOS host had about 177 GiB free on
`/Volumes/sage`, controller `/scratch` had about 103 GiB free, and the `host`
bulk filesystem also had about 103 GiB free. The directly fetched public
`dev/manifest.json` remained unchanged at 177 wheel entries and fourteen
Sagelite primaries, all from `post8` and `post9`; no `post29` primary is
public. No duplicate build, validation, or publication was started. The cell
remains below `full`, and this checkpoint makes no new wheel, install, smoke,
short, or full-suite claim.

## Post29 wheel result and post30 QEPCAD expectation correction

The exact committed `post29` build from
`37e1224bcce63056cdb61734e4e037986965ff94` completed with exit code zero
and produced:

```text
sagelite-10.9.post29-cp313-cp313-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
sha256=8164440e56a18a82760c2635be0c6e1b9c4ac46de354b46461495ef7bca5a249
size=236406405

sagelite_qepcad_runtime-10.9.post3-py3-none-manylinux_2_28_aarch64.whl
sha256=1c4b6cc59292de8d9095535c86a866853ab1922197d70cb273e5b11245c0cfbe
size=5242722

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256=16f7d2614b221825cc5531e605b54d946a91ed22eca3985bd2272ba73f6a6507
size=66578984
```

The watcher assembled a fresh strict closure of one primary, 68 companions,
and 109 third-party wheels. The 178 staged wheels total 16,617,148,159 bytes,
with validator wheelhouse digest
`6ef4c6b79d32bf4f0a8cba09dc3655a1425799e4a0c5c5bb7a72fbb827895e9f`
and `SHA256SUMS` file digest
`24d170ba859e518fac4edc654d42c442723bbb20bebc7b96f8f2c3e2b3e8eaf5`.
Every strict filename, dependency, tag, ABI, architecture, version, and
repaired-primary preflight passed. The fresh wheel-only installation of
`sagelite[all-needed-extras]==10.9.post29`, `pip check`, runtime collection,
and every selftest probe passed, including the repaired complex QEPCAD
three-million-cell operation. Packaged pytest reported 215 passed and two
skipped.

The installed `--optional=sage --short 600` sweep tested 3,954 modules and
failed four. The thirteen failed examples were one FriCAS conversion, eight
GAP3 protocol examples, two pre-existing FLINT polynomial-power aborts, and
two QEPCAD command-construction expectations. The prior complex QEPCAD crash
is absent. The two remaining QEPCAD examples assumed the traditional
`SAGE_LOCAL` command verbatim, so they did not allow the intentional
Singular-companion `PATH` assignment needed by wheel installs. The
authoritative failed-gate artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-154054-37e1224bcce/validation/short-post29/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-154054-37e1224bcce/validation/short-post29/doctest-installed-linux-aarch64-cp313-post29-short-20260714-161854.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-154054-37e1224bcce/validation/short-post29/doctest-installed-linux-aarch64-cp313-post29-short-20260714-161854.analysis.json
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-154054-37e1224bcce/validation-short-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-154054-37e1224bcce/validation-short-exit-code
```

Committed and pushed source
`7cd5cb5f82d7ec6275082de618114b79dd64ab74` makes the QEPCAD doctest
validate the semantic argument layout while allowing optional child
environment assignments and companion-resolved executable paths. It advances
Sagelite to `10.9.post30`. Against the untouched failed `post29` wheel-only
install, four focused source tests passed and a read-only overlay of the exact
corrected module passed all 344 QEPCAD doctests. This is focused regression
evidence rather than fresh-install acceptance:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-154054-37e1224bcce/focused-post30/focused.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-154054-37e1224bcce/focused-post30/focused-overlay-doctest-2.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-154054-37e1224bcce/focused-post30/focused-overlay-doctest-2-exit-code
```

After preserving the `post29` wheelhouse, summary, reduced analysis, logs,
and focused evidence, the iteration removed only its disposable 21 GiB
install and source clone, plus the superseded `post28` source clone. The
guest then had 108,581,715,968 bytes free, above the 100 GiB heavy-build
threshold.

Exactly one native build and one gated watcher started as
`sagelite-post30-build.service` and `sagelite-post30-validate.service` at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260714-164203-7cd5cb5f82d
```

The services record the exact pushed `post30` SHA and native Linux aarch64
CPython 3.13 CIBW contract. The watcher will assemble a fresh strict closure
and run wheel-only `--optional sage` short and full gates only after build
success. No `post30` wheel, install, smoke, short, or full result is claimed
yet. The public manifest remains at 177 wheels and fourteen `post8`/`post9`
Sagelite primaries; no publication was attempted, and this cell remains below
`full`.

## Post30 native wheel-construction checkpoint

The scheduled reconciliation at `2026-07-14T17:02:04Z` found exactly the two
intended guest user-systemd services active. The build service, main PID
`2916260`, owned the sole CIBW container, while the validation watcher, main
PID `2916266`, remained correctly blocked on the absent build exit artifact.
No validation container, completed `post30` wheel, build exit artifact, or
validation exit artifact existed.

The clean detached source checkout was still at exact pushed SHA
`7cd5cb5f82d7ec6275082de618114b79dd64ab74` and the native manylinux build
reported `Linux`, `aarch64`, and Sagelite `10.9.post30`. Meson configured 1,795
Ninja targets. The wheel-construction Ninja log advanced from 30 to 132
records during the reconciliation sample, with concurrent Cython processes
and approximately 793% container CPU usage providing direct forward-progress
evidence despite the buffered top-level journal.

The Linux guest had 97,924,575,232 bytes free after the build began above the
100 GiB heavy-build threshold. The outer macOS host had about 180 GiB free on
`/Volumes/sage`, and controller `/scratch` had about 103 GiB free. The
directly fetched public `dev/manifest.json` remained unchanged at 177 wheel
entries and fourteen Sagelite primaries, all from `post8` and `post9`; no
`post30` primary is public. No duplicate build, validation, or publication was
started. The cell remains below `full`, and this checkpoint makes no new
wheel, install, smoke, short, or full-suite claim.
