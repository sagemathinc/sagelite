# Sagelite Linux aarch64 CPython 3.14 Validation

Last updated: 2026-07-15

## Current status

The native Linux `aarch64` CPython 3.14 `post33` build contract produced a
repaired primary wheel from exact pushed source `5ab41cd4b684`. Binary closure
assembly then exposed the two missing CPython 3.14 dependency wheels,
`cysignals` and `pycosat`; both were built and repaired natively. The resulting
167-wheel strict closure resolved successfully. Its fresh wheel-only install,
`pip check`, all 102 selftest probes, and packaged pytest passed, but the short
doctest gate failed before executing examples because the primary wheel had
been compiled against CPython 3.14.0b3 private interpreter headers and was run
on CPython 3.14.6. No short-gate or full-suite pass is claimed.

Pushed fix `369ec99ad346f7d04458f6154c1d1304868995fd` upgrades the Linux
wheel contract to cibuildwheel 3.4.1, removes the obsolete CPython prerelease
opt-in, rejects prerelease build interpreters inside the selected manylinux
container, and advances the primary version to `10.9.post34`. A new exact-SHA
primary rebuild is required.

The authoritative run root is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-033748-5ab41cd4b684
```

It is running in the persistent Lima guest `sagelite-linux-arm64` on `m1`.
The exact source input is pushed commit
`5ab41cd4b68460e5b6af76461ec955768c401910`, with Sagelite version
`10.9.post33`. The detached guest checkout reports that exact SHA and a clean
status.

## Preflight and cleanup

The outer host reported Darwin `arm64`, about 164 GiB free on `/Volumes/sage`
before cleanup, and Homebrew Python 3.12, 3.13, and 3.14. The Lima guest
reported Linux `aarch64`; a fresh `linux/arm64` container also reported
`aarch64`.

The completed CPython 3.13 validation had left 84,735,225,856 bytes free,
below the 100 GiB heavy-build threshold. Cleanup removed only these
automation-owned disposable artifacts:

- the accepted run's installed validation venv, disposable source checkout,
  and host venv;
- the superseded `post24` validation closure, while retaining its concise
  failure evidence;
- an older resolved-failure run's disposable source checkout and host venv.

The accepted CPython 3.13 `post33` 178-wheel closure and all short/full
validation summaries, reductions, logs, and exit artifacts remain. The guest
had 108,484,116,480 bytes free after cleanup, above the exact 100 GiB
pre-build threshold.

After the first CPython 3.14 build failed, the guest had only
106,742,906,880 bytes free. Cleanup removed only that failed run's disposable
source checkout and host venv while retaining its command log, exit artifacts,
metadata, and orchestration scripts. This restored 108,313,989,120 bytes,
again above the exact 100 GiB heavy-build threshold.

## Durable build and validation services

The first run used these two user-systemd services:

```text
sagelite-post33-cp314-build.service
sagelite-post33-cp314-validate.service
```

The build uses the repository's Linux CIBW helpers with
`CIBW_BUILD=cp314-manylinux_aarch64`, `CIBW_ARCHS=aarch64`, and the absolute
repair interpreter `/opt/python/cp314-cp314/bin/python3`. The companion target
set and repair contract match the accepted CPython 3.13 build. The sole active
manylinux container reported Linux `aarch64`.

The watcher is blocked on the build's absent `exit-code` file. After a
successful build it will:

1. retain the accepted ABI-independent aarch64 companion wheels;
2. replace rebuilt distributions from the CPython 3.14 wheelhouse;
3. resolve all third-party dependencies in a native
   `python:3.14-slim-bookworm` container with binary-only downloads;
4. run the strict repaired-wheelhouse short gate with explicit
   `--optional sage --short 600`;
5. if that passes, run a fresh strict full validation with explicit
   `--optional sage --full`.

At `2026-07-15T01:40:36Z`, both services were active, the command log was
growing, and neither build nor validation had an exit artifact. The CIBW
container was installing the native manylinux prerequisite set. This is
forward-progress evidence only.

At `2026-07-15T01:46:42Z`, the build exited 1 and the watcher correctly stopped
without starting validation. The preserved build log shows that the cached
`post33` prefix was still configured for CPython 3.13: `pplpy` generated
`cpython-313` extension names while the build invoked
`/opt/python/cp314-cp314/bin/cython`. The CIBW environment exposed only the
CPython 3.14 Sage site-packages directory, so that stale CPython 3.13 build
could not find `gmpy2.pxd` and failed. The failed run produced no wheels.

The failed run root is preserved at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-013434-914817f8ad8
```

This revealed that the existing cache guard rejected a `config.status` only
when the Sage version changed. It did not reject a same-version configuration
from another Python ABI. The follow-up source change also compares the cached
`PYTHON_MINOR` with the selected `SAGE_PYTHON` before reusing the
configuration.

Pushed commit `3cb65496e5a1175116bb44c19c5e81cbd815db94` contains that guard and
its focused regression assertion. The replacement build and gated watcher are
running as:

```text
sagelite-post33-cp314-r2-build.service
sagelite-post33-cp314-r2-validate.service
```

At `2026-07-15T02:05:58Z`, both services were active, no build exit artifact
existed, and the detached guest checkout reported the exact pushed SHA with a
clean status. The build was bootstrapping the source before entering CIBW;
this is forward-progress evidence only.

At `2026-07-15T02:07:54Z`, the replacement build exited 1 and its watcher
again correctly stopped without starting validation. The version and Python
minor guard did discard a cached `post30` CPython 3.14 `config.status` and
reconfigured the `post33` source for CPython 3.14. The retained native prefix,
however, still had this virtual-environment interpreter link:

```text
/sage-manylinux_2_28_aarch64/bin/python3 -> /opt/python/cp313-cp313/bin/python3
```

Python's venv setup did not replace the existing link when it created the
CPython 3.14 marker in place. Prefix launchers such as `meson` use
`/host/sage-manylinux_2_28_aarch64/bin/python3`, so Meson still ran CPython
3.13 while the explicit Cython shim ran CPython 3.14. This produced the same
mixed `cpython-313` extension names and missing `gmpy2.pxd` failure. The
failed run produced no wheels.

The follow-up source change detects a retained prefix interpreter whose link
target differs from `SAGE_PYTHON`, removes only its venv interpreter symlinks
and `python3_venv` marker, and recreates the venv interpreter layer with the
selected ABI. This retains the expensive ABI-independent native prefix while
allowing the existing module probes to invalidate Python build-tool markers
against the correct interpreter. A new exact-SHA run is required.

The second failed run remains preserved at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-020454-3cb65496e5a
```

After confirming that both failed build/watch pairs were inactive and had
exit code 1, cleanup removed only this second run's disposable source checkout
and host venv. Its logs, metadata, orchestration scripts, and exit artifacts
remain. Guest free space increased from 106,742,505,472 bytes to
108,313,604,096 bytes, above the exact 100 GiB heavy-build threshold.

Pushed commit `1e07983f06ae1a09c7c0a397288065200be2c9a1` contains the venv reset and
its focused regression assertion. The third build and gated watcher are
running as:

```text
sagelite-post33-cp314-r3-build.service
sagelite-post33-cp314-r3-validate.service
```

At `2026-07-15T02:13:14Z`, both services were active, no exit artifact
existed, and the build was cloning the exact pushed source. This is
forward-progress evidence only.

At `2026-07-15T03:01:59Z`, the GitHub clone was still transferring but had
advanced by only 679,936 bytes over 20 seconds after running for 48 minutes.
It had received about 91.6 MB of this repository's roughly 1.14 GiB packed
history and had not produced a checkout or `HEAD`. The network socket and
object writes proved that the process was not dead, but continuing that
full-history transfer would have delayed the native build by hours.

The watcher was stopped before the build service, and the stalled clone log,
metadata, exit code, finish timestamp, and disk snapshot were retained with
`r3-stalled-clone-*` names in the authoritative run root. Cleanup removed only
the incomplete automation-owned source checkout. The guest then had
108,167,819,264 bytes free, above the exact 100 GiB heavy-build threshold.

The controller created a shallow Git bundle containing the exact pushed
commit and its complete source tree. Its SHA256 is:

```text
8677f0d4b4f890d84200d6d4af42f7225ce5172147ae37a9af1afa8185d9f7c2
```

That hash matched on the controller, the outer Mac, and the Linux guest. The
replacement launcher verifies the hash, imports the bundle into a new Git
repository, records the exact commit as the shallow boundary, checks out the
detached source SHA, requires a clean status, and runs `git fsck --full`
before building. The build and gated watcher now run as:

```text
sagelite-post33-cp314-r4-build.service
sagelite-post33-cp314-r4-validate.service
```

At `2026-07-15T03:07:53Z`, both services were active, no exit artifact
existed, the checkout reported the exact pushed SHA with a clean status, and
CIBW had started the native `manylinux_2_28_aarch64` container for
`cp314-manylinux_aarch64`. This is forward-progress evidence only.

At `2026-07-15T03:14:50Z`, the build exited 1 and its watcher again stopped
without starting validation. The corrected prefix interpreter ran CPython
3.14, and the earlier mixed-ABI `pplpy`/`gmpy2.pxd` failure did not recur.
The retained prefix still had `jinja2` and `markupsafe` install markers from
CPython 3.13, however, while its new CPython 3.14 site-packages did not contain
those modules. The Sage library metadata build therefore stopped immediately
when its interpreter generator imported `jinja2`. The failed run produced no
wheels.

The follow-up source change adds `jinja2` and `markupsafe` to the existing
interpreter-specific module probes. A cross-ABI prefix reuse will now remove
their stale markers so the normal `sage_setup` dependency chain reinstalls
both packages for the selected interpreter.

Cleanup retained the failed run's command log, metadata, scripts, disk
snapshots, and exit artifacts, and removed only its disposable source checkout
and host venv. This restored 107,787,530,240 bytes free, above the 100 GiB
heavy-build threshold.

Pushed commit `5ab41cd4b68460e5b6af76461ec955768c401910` contains the two added probes
and their focused regression assertions. A new shallow exact-SHA bundle with
complete source-tree objects had SHA256
`4b34a9719f15377617c919a2c3cdaf89a53a340758ebb86e82affb14ac594836` on
the controller, outer Mac, and Linux guest. The fourth build and gated watcher
are running as:

```text
sagelite-post33-cp314-r5-build.service
sagelite-post33-cp314-r5-validate.service
```

At `2026-07-15T03:38:39Z`, both services were active, neither had an exit
artifact, and the detached guest checkout reported the exact pushed SHA with
a clean status. CIBW had started from the native Linux `aarch64` guest. This
is forward-progress evidence only.

## Repaired wheel and strict closure

The fourth build completed successfully at `2026-07-15T04:06:11Z`. Its CIBW
contract produced four repaired wheels in 27 minutes, including this primary:

```text
sagelite-10.9.post33-cp314-cp314-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   237276641 bytes
sha256: 3eb9e3bd1b4569f82923c86e756b3574e12c0b77f94491a735b5a9b62cb46989
```

The same contract rebuilt `pplpy`, `sagelite-maxima-runtime`, and
`sagelite-qepcad-runtime`. The raw primary completed all 4,903 installation
entries, the repair path built `cypari2` under CPython 3.14, injected 3,375
native headers, and `auditwheel` assigned the expected
`manylinux_2_27_aarch64.manylinux_2_28_aarch64` tags. The build exit artifact
is zero, the exact source checkout remains clean, and the six-wheel build
inventory with the two dependency additions below totals 318,952,451 bytes.

The first validation attempt failed before validation because the closure
assembler tried to hard-link a root-owned accepted CPython 3.13 companion
wheel as the unprivileged guest user. Its inline Python failure did not stop
the original launcher, so the subsequent incomplete closure predictably
failed at `cysignals`. The failure evidence is preserved with the
`r5-closure-` prefix in the run root. The recovery launcher uses privileged
hard links and explicitly exits on closure-assembly failure; a direct probe
proved that path before it was used.

The corrected closure assembly exposed two genuine binary-wheel gaps. Direct
CPython 3.14 probes confirmed that the other ABI-specific dependencies,
including `cypari2`, `gmpy2`, `fpylll`, `primecountpy`, `pynormaliz`, PyYAML,
SciPy, and SymEngine, already have compatible aarch64 wheels. These two were
built from their published source releases in the same native
`manylinux_2_28_aarch64` image and repaired with `auditwheel`:

```text
cysignals-1.12.6-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl
size:   265700 bytes
sha256: 1e72abc8f620adfcc8bb147a05392721f0b82c206dee80298e28dd2d21ed3d88

pycosat-0.6.6-cp314-cp314-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl
size:   207579 bytes
sha256: 48a442857eb81da0f4f072254a670db3cf36e5fd0e68f233dbd5b45d5d19b190
```

The `cysignals` and `pycosat` build exit artifacts are both zero. Their first
resolution failures are preserved with the `r6-cysignals-resolution-` and
`r7-pycosat-resolution-` prefixes. No source rebuild was needed.

Validation service `sagelite-post33-cp314-r8-validate.service` then assembled
and hash-inventoried a 167-wheel, 16,620,397,617-byte strict closure. Binary-
only resolution of `sagelite[all-needed-extras]==10.9.post33` and the required
`ziglang==0.16.0` helper completed. At `2026-07-15T04:16:18Z` it started the
fresh strict short gate with explicit `--optional sage --short 600`; the clean
wheel-only installation was active at the latest check. The guest had
106,104,467,456 bytes free. This is forward-progress evidence only, not an
install or short-gate pass.

## First strict short-gate result

The r8 validation service finished with exit code 16 at
`2026-07-15T04:31:46Z`. The strict preflight accepted all 167 wheels. The fresh
wheel-only installation of `sagelite[all-needed-extras]==10.9.post33` and
`pip check` both passed. `sagelite-selftest` passed all 102 probes, including
all required native imports and companion executable/data checks. Packaged
pytest passed 215 tests with 2 skips.

The installed doctest controller then reported 3,953 failed modules out of
3,954. A one-file serial reproduction proved that this was one startup failure
class, not 3,953 independent doctest failures:

```text
python -m sage.doctest --optional=sage --serial sage/version.py
```

That process received SIGSEGV in `sage.cpython.atexit._get_exithandlers()`.
Calling `_get_exithandlers()` directly also exited 139. The primary build log
records `Python 3.14.0b3`, while the clean validation container records Python
3.14.6. `sage.cpython.atexit` uses the private `PyInterpreterState` layout to
save and restore callbacks; the prerelease build headers therefore generated
an extension that reads the wrong field offset in the stable validation
runtime. The existing `cysignals` crash reporter made the gate's aggregate
output look like per-module segmentation faults.

The durable failure evidence is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-033748-5ab41cd4b684/validation-short-exit-code
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-033748-5ab41cd4b684/validation/short-post33/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-033748-5ab41cd4b684/validation/short-post33/doctest-installed-linux-aarch64-cp314-post33-short-20260715-041940.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-033748-5ab41cd4b684/validation/short-post33/doctest-installed-linux-aarch64-cp314-post33-short-20260715-041940.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-033748-5ab41cd4b684/validation/short-post33/doctest-installed-linux-aarch64-cp314-post33-short-20260715-041940.selftest.log
```

The fix is in exact pushed source
`369ec99ad346f7d04458f6154c1d1304868995fd`. cibuildwheel 3.4.1 pins the
manylinux aarch64 image dated 2026-03-20 and a stable CPython 3.14 build; the
new in-container release-level guard prevents a future stale prerelease image
from silently producing another advertised CPython 3.14 wheel.

## Stable-interpreter rebuild

Cleanup removed only the failed short gate's disposable installed venv, which
used 22,176,149,504 bytes. All validation summaries, logs, reductions,
manifests, inventories, and exit artifacts remain. This restored
106,108,026,880 bytes free. Pulling cibuildwheel 3.4.1's pinned
`quay.io/pypa/manylinux_2_28_aarch64:2026.03.20-1` image left
103,191,810,048 bytes free, still above the 100 GB heavy-build threshold.
Inside that exact image, `uname -m` reports `aarch64` and
`/opt/python/cp314-cp314/bin/python3` reports CPython 3.14.3 with release level
`final`.

The new authoritative run root is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-044758-49015d0a2b45
```

Its exact source is pushed commit
`49015d0a2b4590aeb6fcf1675b8273e5f4380783`, version `10.9.post34`. The
shallow source bundle has SHA256
`6947748dd8b950e050d94cb0b1a90647ac99aca8584f7a8caff5258f7ce1be31`
on the controller, outer Mac, and Linux guest. The detached guest checkout
reports the exact SHA, version, and a clean status.

The durable services are:

```text
sagelite-post34-cp314-r9-build.service
sagelite-post34-cp314-r9-validate.service
```

At `2026-07-15T04:48:35Z`, both were active. The build had verified and
checked out the exact bundle and was bootstrapping the source. The watcher is
waiting for the build exit artifact; on success it retains the repaired
CPython 3.14 `cysignals` and `pycosat` wheels, assembles a fresh strict closure,
runs the explicit `--optional sage --short 600` gate, and only then starts a
fresh full validation. This is forward-progress evidence only; no `post34`
wheel, install, smoke, short-gate, or full result is claimed yet.

## Public preview state

The directly fetched public `dev/manifest.json` remained generated at
`2026-07-09T17:17:42.743310+00:00`, with 177 wheels and fourteen Sagelite
primary wheels from `10.9.post8` and `10.9.post9`. There is no public
`post33` primary and no Linux aarch64 CPython 3.14 primary. No publication was
attempted.
