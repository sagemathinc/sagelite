# Sagelite macOS arm64 CPython 3.13 Validation

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
