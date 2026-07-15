# Sagelite macOS arm64 CPython 3.13 Validation

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
