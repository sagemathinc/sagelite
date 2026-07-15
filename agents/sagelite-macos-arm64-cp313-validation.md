# Sagelite macOS arm64 CPython 3.13 Validation

## 2026-07-15 Portable lrslib, msolve, and QEPCAD Companions

Exact pushed source `300764eac33f8e21cbcf24fddb2edcf241272ea7`
made the lrslib, msolve, and QEPCAD companion builders portable on macOS. The
builders now discover each executable's recursive non-system Mach-O closure,
copy the required dylibs, rewrite executable and dylib references to
loader-relative paths, assign portable install IDs, and ad-hoc sign every
modified Mach-O file. The Linux `ldd` paths are unchanged. Focused repository
validation passed the four portability tests. The complete companion metadata
file had 253 passes and the same 3 pre-existing failures
involving generated Flatter egg-info and the Regina dependency expectation.

The lrslib and msolve wheels reused native inputs built from exact source
`24b5e7aec6db357933703de8a425f10ab4fb0e79`. Their packaging source and the
final exact QEPCAD source `55949b5b79a40e49f69332b186d3a7e1348c1801`
produced:

```text
sagelite_lrslib_runtime-10.9.post1-py3-none-macosx_26_0_arm64.whl
  361,593 bytes
  d5e014b27968214dd0b5ba52921787122c63bb0702c756e86b60ea7ad5f0255c
sagelite_msolve_runtime-10.9.post2-py3-none-macosx_26_0_arm64.whl
  5,276,828 bytes
  382b07cb8bc1719949a44feb5c23e52b3abf6753b75e0e58e021c1f4058475fb
sagelite_qepcad_runtime-10.9.post3-py3-none-macosx_26_0_arm64.whl
  527,740 bytes
  4c17e33df1a16d8b4cc6df6a20a62caf651baced655c19d15bdfc4ee77a5f081
```

Their embedded names, versions, and wheel tags match the filenames. The
exhaustive audits covered 4 Mach-O files and 11 dependencies for lrslib, 6 and
23 for msolve, and 2 and 6 for QEPCAD: 12 Mach-O files and 40 dependencies in
total, with no absolute, unresolved, or escaping load path. Fresh CPython
3.13.14 venvs installed each wheel using only its local wheelhouse and passed
`pip check`. Neutral-environment functional smokes located both `lrs` and
`lrsnash`, exercised `msolve`, and started QEPCAD three independent times,
requiring its banner and first prompt after piped input reached EOF. The final
QEPCAD validation exit code is zero.

QEPCAD required a native input correction in addition to wheel repair. Its
legacy character reader redirected EOF to `/dev/tty`; with piped input it
could wait on a controlling terminal or recursively read an invalid terminal
descriptor. The patched `1.74.p10` input path preserves EOF for noninteractive
standard input, guards a failed terminal open, preserves integer EOF sentinels
in the configuration parsers, and exits before SACLIB's newline discard loop.
The final patch passed both GNU `patch --fuzz=0` and macOS BSD `patch` checks.
The preceding per-SHA runs preserve the initial timeout, unsafe teardown,
terminal-fallback, patch-context, and missing-declaration diagnostics rather
than treating intermittent crashes as successful smokes.

The public manifest was rechecked with a pip user agent and remains unchanged:
generated 2026-07-09, 177 wheels, and fourteen Sagelite primary wheels. These
artifacts were not published. This reduces the missing `all-needed-extras`
companion closure from 8 distributions to 5:
`sagelite-database-polytopes-4d`, `sagelite-fricas-runtime`,
`sagelite-imagemagick-runtime`, `sagelite-info-runtime`, and
`sagelite-kenzo-runtime`. No strict Sagelite installation,
`sagelite-selftest`, short run, full run, or publication result is claimed.
Final cell validation must still build those companions and rebuild the
primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-native-command-20260715-183617-300764eac33/
/scratch/sagelite-automation/macos-arm64-cp313-qepcad-eof-20260715-200855-55949b5b79a/
```

The matching `m1` directories retain the exact sources, native inputs, wheels,
clean installs, audits, smokes, and intermediate diagnostic runs. Important
successful evidence includes `wheelhouse/SHA256SUMS`,
`validation/wheel-inventory.txt`, `validation/strict-macho-audit.txt`, the
install and `pip-check` files, the companion smoke files, `run-metadata.txt`,
`command.log`, and `exit-code`. The native-command packaging run and final
QEPCAD run both have exit code `0`; the superseded combined validation exit
code remains `1` because it records the original QEPCAD timeout after the
lrslib and msolve validations had passed.

## 2026-07-15 Portable Giac Companion

Exact pushed source `4075521634d7ec628c3dca2c158066a47261f7f6`
made the Giac companion portable on macOS. The builder now discovers Giac's
complete non-system Mach-O closure, including Homebrew GCC dependencies
expressed through `@rpath`, copies that closure, rewrites executable and dylib
references to loader-relative paths, assigns portable install IDs, and ad-hoc
signs every modified Mach-O file. The Linux `ldd` path is unchanged. The
shared companion smoke now accepts Giac's numeric-only macOS version output
and requires a successful arithmetic calculation. Focused repository
validation passed 4 tests. The complete companion metadata file had 252
passes and the same 3 pre-existing failures involving generated Flatter
egg-info and the Regina dependency expectation.

The exact pushed revision reused the Giac native input built by exact source
`24b5e7aec6d` and produced:

```text
sagelite_giac_runtime-10.9.post1-py3-none-macosx_26_0_arm64.whl
  25,360,869 bytes
  15c8ba839d67bd64b00f0e0a17a45627484e362fbe1b5799838662e7c651557f
```

Its metadata and wheel tag match the filename. An exhaustive audit covered
all 20 Mach-O files and 71 load dependencies and found no absolute,
unresolved, or escaping load path. A fresh CPython 3.13.14 venv installed the
wheel using only the local wheelhouse, passed `pip check`, and completed the
version and arithmetic smokes from a neutral environment with no inherited
Sage or Homebrew path. The validation exit code is zero. The public manifest
was rechecked with a pip user agent and remains unchanged at 177 wheels and
fourteen Sagelite primary wheels; this artifact was not published.

This reduces the missing `all-needed-extras` companion closure from 9
distributions to 8: `sagelite-database-polytopes-4d`,
`sagelite-fricas-runtime`, `sagelite-imagemagick-runtime`,
`sagelite-info-runtime`, `sagelite-kenzo-runtime`,
`sagelite-lrslib-runtime`, `sagelite-msolve-runtime`, and
`sagelite-qepcad-runtime`. No strict Sagelite installation,
`sagelite-selftest`, short run, full run, or publication result is claimed.
Final cell validation must still build those companions and rebuild the
primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-giac-20260715-180928-4075521634d/
```

The matching `m1` directory retains the exact detached source checkout,
native input reference, wheel, clean install, and audit tree. Important
evidence includes `wheelhouse/SHA256SUMS`,
`validation/wheel-inventory.txt`, `validation/strict-macho-audit.txt`,
`validation/install.txt`, `validation/pip-check.txt`,
`validation/smoke.txt`, `run-metadata.txt`, `command.log`, and `exit-code`
(`0`).

## 2026-07-15 Portable CSDP Companion

Exact pushed source `099c31b802a9d02557076228f6651afbb2af60ad`
made the CSDP companion portable on macOS. The package builder now discovers
the complete non-system Mach-O closure of `theta`, including Homebrew GCC
runtime dependencies expressed through `@rpath`, copies that closure, rewrites
all executable and dylib references to loader-relative paths, assigns portable
install IDs, and ad-hoc signs every modified Mach-O file. The existing Linux
`ldd` path is unchanged. Focused repository validation passed 2 tests; the
complete companion metadata file had 251 passes and the same 3 pre-existing
failures involving generated Flatter egg-info and the Regina dependency
expectation.

The exact pushed revision reused the CSDP native input built by exact source
`24b5e7aec6d` and produced:

```text
sagelite_csdp_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  827,120 bytes
  a5ba39d47c55ceec24ce841983405dbb4f1ac12dd790e817b1b7d127a786ecaf
```

Its metadata and wheel tag match the filename. An exhaustive audit covered all
5 Mach-O files and found no absolute, unresolved, or escaping load path. A
fresh CPython 3.13.14 venv installed the wheel using only the local wheelhouse,
passed `pip check`, and completed a functional Lovasz theta-number smoke from
a neutral directory with no inherited Sage or Homebrew path. The validation
exit code is zero. The public manifest was rechecked with a pip user agent and
remains unchanged at 177 wheels and fourteen Sagelite primary wheels; this
artifact was not published.

This reduces the missing `all-needed-extras` companion closure from 10
distributions to 9: `sagelite-database-polytopes-4d`,
`sagelite-fricas-runtime`, `sagelite-giac-runtime`,
`sagelite-imagemagick-runtime`, `sagelite-info-runtime`,
`sagelite-kenzo-runtime`, `sagelite-lrslib-runtime`,
`sagelite-msolve-runtime`, and `sagelite-qepcad-runtime`. No strict Sagelite
installation, `sagelite-selftest`, short run, full run, or publication result
is claimed. Final cell validation must still build those companions and
rebuild the primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-csdp-20260715-173818-099c31b802a/
```

The matching `m1` directory retains the exact detached source checkout, native
input reference, wheel, clean install, and audit tree. Important evidence
includes `wheelhouse/SHA256SUMS`, `validation/wheel-inventory.txt`,
`validation/macho-inventory.txt`, `validation/strict-macho-audit.txt`,
`validation/install.txt`, `validation/pip-check.txt`, `validation/smoke.txt`,
`run-metadata.txt`, `command.log`, and `exit-code` (`0`).

## 2026-07-15 Giac System-BLAS Build Ordering

Exact pushed source `24b5e7aec6db357933703de8a425f10ab4fb0e79`
fixes the first failure in the remaining-native-companion batch. Giac's
package metadata did not declare either the selected BLAS implementation or
the conditional system pkg-config facade targets, even though Giac configure
unconditionally requires `lapack.pc`. On this Homebrew system, explicit
`make giac` therefore bypassed the facade that maps the accepted system
OpenBLAS installation to BLAS, CBLAS, and LAPACK pkg-config names.

The fix declares both `$(BLAS)` and `$(PCFILES)`. In a fresh exact-source run,
the generated dependency graph retained both abstractions, created
`prefix/lib/pkgconfig/lapack.pc` as a symlink to Homebrew's `openblas.pc`, and
built and installed Giac 1.9.0.15p0 successfully. The preceding failed run at
exact pushed source `15a6f69795d9169cc02e95b6b768a8ad16e87609`
is preserved and shows the original `Package 'lapack' not found` configure
failure. The public manifest was rechecked with a pip user agent and remains
unchanged at 177 wheels and fourteen Sagelite primary wheels.

This resolves the native Giac build blocker only. No Giac companion wheel,
Mach-O repair, isolated smoke, strict Sagelite installation, short run, full
run, or publication result is claimed yet. The exact-source native-input run
continues durably under:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp313-remaining-native-20260715-170825-24b5e7aec6d/
```

Important completed evidence includes `run-metadata.txt`,
`validation/source-status.txt`,
`validation/giac-generated-dependencies.txt`, `validation/lapack-pc.txt`,
`validation/lapack-pc-target.txt`, `validation/giac-built-at.txt`, and
`command.log`. The ten-distribution macOS companion closure count is unchanged
until repaired wheels pass their audits and isolated smokes.

## 2026-07-15 Portable Command Companion Batch

Exact pushed source `2df580c98da3f01a41ad4232542c91673cbc33d2`
made the LiE companion portable on macOS by copying its non-system Readline
dylib, rewriting both the executable dependency and dylib install ID to
loader-relative paths, and ad-hoc signing the modified Mach-O files. Focused
repository validation passed five tests. The native inputs from the preceding
exact-source command build at `5e6a45e7160` were then packaged into six native
macOS arm64 wheels:

```text
sagelite_gap3_runtime-10.9.post1-py3-none-macosx_26_0_arm64.whl
  20,585,435 bytes
  ffc08bcb43eae2e1ee8bac604ffd8af95f0517b09e4812ff093382af8e203883
sagelite_glucose_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  137,687 bytes
  98b4f1d1fdb7ae344dca4688a0d3dbc361f7fde2f8ecf654febe14643dc79e67
sagelite_kissat_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  123,174 bytes
  e4a3737d3157279797647f3b6d14d6e4b43b908cd1bd7ba595f1287e50cfae5d
sagelite_lie_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  889,476 bytes
  701f8da3b95cab38a44f5ad6455d070ce90798b96cde7f314311882452cdb023
sagelite_plantri_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  116,195 bytes
  334cd5e2c06d14ef9a399d17e021116366437712157f7574b2d593a74848568c
sagelite_rubiks_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  192,609 bytes
  b09f6a4ebef1f402c11dbb45eef744c6eff07f5ba1a5da36c1d261b2e31daa40
```

Their embedded metadata and wheel tags match the filenames. An exhaustive
audit covered 97 Mach-O files and found no absolute, unresolved, or escaping
load path. The initial smoke exposed two validation defects rather than wheel
defects: Glucose rejects `-help` and directs callers to `--help`, and the
shared smoke script had no handlers for LiE or GAP3. Exact pushed sources
`701ebbdc8471b8fa42e5eea779be921809ae901d` and
`dd2cf612b014b9973cc68f522ad24efd8fff6827` corrected those protocols and
added deterministic arithmetic probes for LiE and GAP3. Focused repository
validation then passed seven tests.

Exact validation source `dd2cf612b01` installed the unchanged, hash-verified
wheel bytes into six separate fresh CPython 3.13.14 venvs with a neutral
runtime `PATH`. All six isolated smokes passed, including both Glucose
executables, Plantri, Kissat, two Rubiks commands, and arithmetic through LiE
and GAP3. The validation exit code is zero. The public manifest remains
unchanged at 177 wheels; no artifact from this batch was published.

Together with the previously completed Maxima and Planarity wheels, this batch
reduces the missing `all-needed-extras` closure from 16 distributions to 10:
`sagelite-csdp-runtime`, `sagelite-database-polytopes-4d`,
`sagelite-fricas-runtime`, `sagelite-giac-runtime`,
`sagelite-imagemagick-runtime`, `sagelite-info-runtime`,
`sagelite-kenzo-runtime`, `sagelite-lrslib-runtime`,
`sagelite-msolve-runtime`, and `sagelite-qepcad-runtime`. No strict Sagelite
installation, `pip check`, selftest, short run, full run, or publication result
is claimed. Final cell validation must still build those companions and rebuild
the primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-command-companions-20260715-160338-2df580c98da/
/scratch/sagelite-automation/macos-arm64-cp313-command-smoke-20260715-161127-dd2cf612b01/
```

The matching `m1` directories retain the exact source checkouts and fresh
smoke venvs. Important evidence includes both `wheelhouse/SHA256SUMS` files,
the wheel metadata inventory, `validation/macho-inventory.txt`, the empty
`validation/strict-macho-audit.txt`, all six `validation/smoke-*.txt` files,
`run-metadata.txt`, `command.log`, and the final validation `exit-code` (`0`).

## 2026-07-15 Portable Planarity Companion

Exact pushed source `7d63944caeb9c4c0fdcf4c2463db95d7ee97c1a3`
fixed the first failure recovered from the macOS command-companion batch. The
planarity wheel builder had unconditionally invoked Linux `ldd`; on Darwin it
now discovers `libplanarity` with `otool`, copies the dylib, rewrites the
executable dependency and dylib install ID to loader-relative paths, and
ad-hoc signs both modified Mach-O files. The Linux packaging path remains
unchanged. Focused repository validation passed 7 tests; the complete
companion metadata file had 248 passes and 3 pre-existing failures involving
ignored generated egg-info and the separately inconsistent Regina dependency
expectation.

The exact pushed revision then built this native companion wheel on `m1`:

```text
sagelite_planarity_runtime-10.9-py3-none-macosx_26_0_arm64.whl
  95,228 bytes
  5911d9dc3d634ecef7033b71af50988f8cda815472cfd1431ec41756ec236632
```

Its native input was reused from the immediately preceding exact-source
command-companion run at `5e6a45e7160`; that source differs from the wheel's
source only by this packaging repair and its test. The resulting wheel has two
Mach-O files. An exhaustive load-path and install-ID audit found no absolute,
unresolved, or escaping dependency, and a separate fresh CPython 3.13.14 venv
installed the wheel and passed the planarity executable smoke with an empty
environment apart from the required neutral `PATH` and smoke selectors.

This adds one of the 17 previously missing `all-needed-extras` companion
distributions, leaving 16. It does not establish a strict Sagelite install,
`pip check`, selftest, short run, full run, or publication result. Final cell
validation must still assemble all remaining companions and rebuild the
primary from the selected coherent revision.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-planarity-20260715-153510-7d63944caeb/
```

The matching `m1` directory retains the exact source checkout, build venv, and
unpacked audit tree. Important evidence includes `wheelhouse/SHA256SUMS`,
`validation/wheel-inventory.txt`, `validation/macho-inventory.txt`, the empty
`validation/strict-macho-audit.txt`, `validation/smoke.txt`, `command.log`,
and `exit-code` (`0`).

## 2026-07-15 Portable Base Companion Batch

Exact pushed source `cc8d999d436a256a42ff70d51963fc4f04bb836b`
completed a native macOS arm64 build of the three base companions that were
missing or below the `post39` primary's dependency floors. The resulting
`macosx_26_0_arm64` wheels are:

```text
sagelite_flatter_runtime-10.9.post1-py3-none-macosx_26_0_arm64.whl
  13,936,429 bytes
  20c09b5c7118a4aa8aa7a309ed6ddf70cfb98c206dced84938b9f15874aa8878
sagelite_graphviz_runtime-10.9.post4-py3-none-macosx_26_0_arm64.whl
  11,651,031 bytes
  ed8300dc724f217f52b0129da7d79a983dc72f225ed41ce19408a37a7757f0a8
sagelite_maxima_runtime-10.9.post15-py3-none-macosx_26_0_arm64.whl
  23,470,010 bytes
  4fc54eeff0d301f74aaac937fee1be2c8626f3d939c9f10b93d5fe7922e0b981
```

All three were installed into separate fresh CPython 3.13.14 venvs with no
inherited Sage or Homebrew path, then passed their companion smoke. Flatter
ran help and lattice-reduction probes, Graphviz ran its executable and plugin
probes, and Maxima evaluated its arithmetic probe through the bundled ECL
image. An exhaustive audit of every Mach-O file in all three wheels found no
non-system absolute load path. The repair work covers recursive Darwin dylib
discovery, Homebrew alias handling, plugin install IDs, loader-relative
Maxima/ECL/GMP/GC references, and the `ecl_min` helper. Focused repository
validation passed 24 tests.

This removes all three base-companion compatibility gaps recorded for
`post39`. It does not complete the cell: 17 distinct `all-needed-extras`
companion distributions still lack compatible macOS wheels. Also, the retained
portable primary was built from `c6c8d1b6665`, so final coherent-revision
validation must rebuild the primary from the selected then-current commit
before strict installation. No clean-install, `pip check`, selftest, short,
full, or publication claim is made. The public manifest remains unchanged at
177 wheels and fourteen primary wheels.

Durable controller artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-base-companions-20260715-123539-84b84caad68/
```

The matching `m1` directory retains the build tree. Important evidence
includes `wheelhouse/SHA256SUMS`, `validation/wheel-inventory.txt`, the three
`validation/smoke-*.txt` files, the empty strict-audit result,
`run-metadata.txt`, `command.log`, and `exit-code` (`0`).

## 2026-07-15 Portable Primary Wheel and Companion-Closure Blocker

Exact pushed source `c6c8d1b666516434e24793bee92ff57430575442`
(`10.9.post39`) completed a fresh native build on `m1`. The controller-created
source archive had SHA-256
`49783ef08ceaa378c397a8d50001510fd52009f9818fe12e3b3df15edcd99656`.
The controller and `m1` independently reproduced its materialized source tree
`e51552e11c63ee82dad1caedb29550cc1cacc3aa`. An initial source guard compared
that materialized archive tree with the unexported commit tree and stopped
before building; the guard and preserved failure log were corrected to compare
the independently reproduced archive tree before the same archive was used.

The committed general macOS repair now succeeds. The resulting primary wheel
is:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp313-20260715-114613-c6c8d1b6665/wheelhouse/sagelite-10.9.post39-cp313-cp313-macosx_26_0_arm64.whl
```

It is 98,560,684 bytes with SHA-256
`92742b66f1155e8518d8b01103dcd76709fd0b819880f7166b30a66133cb5d8c`.
Its metadata and wheel tag are `10.9.post39` and
`cp313-cp313-macosx_26_0_arm64`. The wheel has 4,986 members, including 638
Mach-O files and 51 general bundled dylibs. The final repair rewrote 23
companion-owned PARI/GMP/MPFR/Singular dependencies in 16 Mach-O files and
audited 1,178 load dependencies across all 638 Mach-O files. The audit found
only system libraries, wheel-contained loader-relative libraries, and the
exact allowed companion-relative library paths; it rejected absolute,
unresolved `@rpath`, and escaping paths. Delocate's permissive scan still logs
expected missing-companion diagnostics before that independent strict audit,
because those companion libraries deliberately do not live in the primary
wheel.

The primary-wheel portability blocker is therefore fixed, but the cell cannot
yet start its required strict clean installation. A CPython 3.13.14 native-tag
probe of the public dev index found no compatible release satisfying 3 of 45
base companion requirements:

```text
sagelite-flatter-runtime >=10.9.post1,<10.10
sagelite-graphviz-runtime >=10.9.post4,<10.10
sagelite-maxima-runtime >=10.9.post15,<10.10
```

The public index has older macOS wheels for each, respectively `10.9`,
`10.9.post3`, and `10.9.post14`. A separate probe found 18 of the 33 Sagelite
companions in `all-needed-extras` without a compatible public wheel. Most have
only Linux wheels; `sagelite-database-polytopes-4d` has no public simple-index
entry, and the Maxima gap overlaps the base set. There are 20 distinct missing
base-or-extra companion distributions. The incomplete 3.7 GiB download probe
was removed after its logs and compatibility inventories were preserved.

No clean-install, `pip check`, selftest, short-doctest, full-doctest, or
publication claim is made. The next macOS CPython 3.13 iteration should build
the 20 missing compatible companion distributions from committed source,
assemble the complete wheelhouse around this primary, and run the named strict
short and full `--optional=sage` gates. Durable controller evidence is under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-20260715-114613-c6c8d1b6665/
```

The matching `m1` run retains the wheel and build evidence. Important files
include `command.log`, `exit-code`, `wheelhouse/SHA256SUMS`,
`validation/base-companion-compatibility-probe.txt`, and
`validation/all-needed-companion-compatibility-probe.txt`.

## 2026-07-15 Native Build and Portability Blocker

The next scheduled iteration built exact pushed source
`c978063abdb6c3c14359784be591b635eca63783` (`10.9.post38`) on `m1` from a
controller-created `git archive`. The transferred archive had SHA-256
`471039880fafee2e8564694597c17291024ad910f3b849f2dd0d5fd4efaac5fa`, and
the temporary build repository reproduced canonical source tree
`86bc87b0b9f1a6492267d3db30e4c38945a9eab0`. This avoided building an
uncommitted or independently modified remote checkout.

The native CPython 3.13 compilation completed after two preserved diagnostic
attempts. The first identified five missing native build dependencies and led
to run-local builds of Bliss, Coxeter3, MCQD, MeatAxe, and TDLib. The second
found that an older CPython 3.14 prefix was preceding the CPython 3.13 virtual
environment in `PATH`; correcting that ordering selected NumPy 2.5.0 from the
build environment. The completed intermediate wheel is:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp313-20260715-103605-c978063abdb6/wheelhouse/sagelite-10.9.post38-cp313-cp313-macosx_26_0_arm64.whl
```

It is 67,044,960 bytes with SHA-256
`54071f863141da72099fa71a04bd9ec56b6ac9dafc2dd8b6a6bdd818cc406d00`.
Its metadata has the expected `cp313-cp313-macosx_26_0_arm64` tag, and its
4,934 members include 585 extension modules. Existing Singular and PARI
companion-runtime repairs ran successfully.

This artifact is **not** an installable portable-wheel result. An exhaustive
Mach-O audit found no bundled dylibs and 30 distinct non-system absolute dylib
dependencies. They resolve into the run-local prefix, the older
`/Volumes/sage/sagelite-build/prefix`, or Homebrew. A subsequent standard
`delocate` attempt failed with `DelocationError: Could not find all
dependencies` because the existing companion repairs had already rewritten
PARI/GMP/MPFR references to `@loader_path` locations supplied by separate
companion wheels, which are absent while repairing the primary wheel alone.

The next implementation step is a macOS repair stage that bundles the general
native dependency closure while preserving one authoritative
PARI/GMP/MPFR/Singular runtime from the companion wheels. It must then reject
all remaining non-system absolute dependencies before strict preflight or
installation begins. Running generic delocation before the companion repairs
may duplicate those runtimes, so it is not accepted without an explicit
post-repair audit.

No wheel-built, install-passed, smoke-passed, full-passed, or publication claim
is made for this artifact. In particular, the public `post9` matrix entry
remains unchanged. Durable controller evidence is under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-20260715-103605-c978063abdb6/
```

The remote run and its build products remain under the matching path in
`/Volumes/sage/sagelite-automation`. Preserved evidence includes source and
archive hashes, run metadata, both failed build logs, the successful exit
code, the complete Mach-O dependency inventory, the 30-entry absolute
dependency inventory, the primary checksum and size, and the delocation
traceback.

## 2026-07-15 Strict-Profile Preparation

The scheduled matrix iteration first rechecked Linux `x86_64` CPython 3.14.
The required `host` alias still reached an `x86_64` machine without
`/mnt/cocalc-scratch`; `/` had 17 GiB free and `/mnt/cocalc` had 64 GiB free.
That leaves the existing x86_64 heavy-build blocker unchanged. No x86_64
build, validation, or publication was started.

Independent preflight for the next available work-order cell found `m1` idle,
native macOS `arm64`, running macOS 26.4, with Homebrew CPython 3.13 and 181 GiB
free on `/Volumes/sage`. Preserved macOS wheels and doctest logs are from the
earlier `post1`/`post3` work and do not match the current source or companion
dependency floors, so none were promoted to acceptance evidence.

Exact pushed source `718dba53d4005967543dc9e2e103e397b3852dc8`
(`10.9.post38`) adds `--strict-macos-wheelhouse-preflight` to
`tools/validate-sagelite-wheelhouse.py`. The profile requires a primary
`macosx` wheel and applies the complete closure, requested version, companion
version, interpreter, ABI, architecture, and host-compatible platform checks.
It deliberately omits the Linux-only manylinux repair requirement. The
validator also records `OBJC_DISABLE_INITIALIZE_FORK_SAFETY` in install
metadata when the accepted macOS full-suite workaround is explicitly set.

Focused validation passed 43 tests. The commit was pushed to `origin/develop`
and the remote ref was verified at the exact SHA above. Durable controller
artifacts are under:

```text
/scratch/sagelite-automation/macos-arm64-cp313-20260715-100758-718dba53d400/
```

Important files include:

```text
run-metadata.txt
host-preflight.txt
m1-preflight.txt
public-manifest-summary.txt
validation/pytest-validator.log
```

The public manifest remained unchanged at 177 wheels generated on 2026-07-09,
including fourteen Sagelite primaries. No `post38` artifact is public.

No macOS CPython 3.13 wheel-built, install-passed, smoke-passed, or full-passed
claim is made. The cell remains `smoke only`. The next iteration should build
the exact then-current pushed source and its complete macOS arm64 CPython 3.13
wheel closure in a new `/Volumes/sage/sagelite-automation` run, then run the
named strict short gate and full `--optional=sage` sweep.
