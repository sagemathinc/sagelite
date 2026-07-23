# Sagelite Linux aarch64 CPython 3.14 Validation

Last updated: 2026-07-23

## 2026-07-23 Post64 Exact Fat-Binary Rebuild Start

Exact pushed `post64` source
`014ae4bf44318b6f5032053957a92291d4363b7a` is building natively at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260723-103846-014ae4bf443
sagelite-post64-arm-cp314-build.service
sagelite-post64-arm-cp314-watch.service
```

The CPython 3.13 acceptance cleanup restored 109,551,865,856 bytes free,
above the binary 100 GiB heavy-build threshold. The retained exact-SHA source
bundle has size 145,833,961 bytes and verified SHA256
`b9e8799924c625055dff6cad4948c84d48ad159581f5e46b8bce42454b3e6eac`.
All 191 wheels in the accepted `post64` CPython 3.12 base closure and all 180
wheels in the accepted `post63` CPython 3.14 ABI seed passed complete SHA256
rechecks before launch.

The detached checkout is clean at the exact selected source and reports
`10.9.post64`. The actual manylinux container reports Linux `aarch64` and
CPython 3.14.3. Its selected isolated native prefix is
`/host/sage-fat-v1-manylinux_2_28_aarch64`; the cache guard correctly replaced
the retained CPython 3.13 interpreter layer with CPython 3.14 before entering
native prerequisite setup. The guarded watcher will assemble a strict closure
and run independent fresh short and full gates only after build success.
Launcher hashes are:

```text
444a35305a67a19e88ed7cf2763e963edc4f194a6eca672e4ffbf7dd383ebcf3  start-build.sh
b52ff9a3b2c4dc2bce41b3d4e39ce12cf24c5cdd74c066161282652e9e24fdad  validate-after-build.sh
1bb0d35374fe3b73de34e67bcd93f3bbd3406fdd9ecfddd1677eaf1c4b76c4c1  watch-and-validate.sh
```

The exact build subsequently completed with exit code zero and produced:

```text
sagelite-10.9.post64-cp314-cp314-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   248307872 bytes
sha256: 6e2a1ea0006b69d6de7f5a8396fe183df1d38517fa3d7d84df6ef687cf5b7017
```

The guarded watcher assembled a deterministic strict closure containing 180
wheels totaling 16,780,148,113 bytes. The closure `SHA256SUMS` file has
SHA256
`de257fb318edfb120bb52c1fbfb43c1c9de3dd9a1d1212c7ab4e90b1723f99da`.
At the latest `2026-07-23T11:33:32Z` check, the fresh short gate had passed
strict preflight, binary-only `sagelite[all-needed-extras]==10.9.post64`
installation, `pip check`, runtime isolation with zero leaks, all 102
selftests, and all 3,953 installed `--optional=sage` modules with zero
failures in 538.7 seconds. Packaged pytest had collected 229 tests with 2
skips and reached 69 percent while the original watcher PID `4041408`
remained active. The independent full gate remains guarded on a zero
short-gate exit. No short or full pass, cell acceptance, or publication is
claimed yet.

## 2026-07-18 Post63 Full Acceptance

The exact native build and guarded watcher both completed with exit code zero.
The repaired primary is:

```text
sagelite-10.9.post63-cp314-cp314-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   237290280 bytes
sha256: 65773c8325493f7fc471ccd2bed0778ca8181adb3b49eeed2a9872b4babd1948
```

The watcher combined the synchronized CPython 3.12 companion set, the new
primary and rebuilt wheels, and the accepted CPython 3.14 `cysignals` and
`pycosat` supplements. Binary-only resolution produced this strict closure:

```text
wheels:                 180
Sagelite projects:       82 (1 primary and 81 companions)
third-party projects:    98
total bytes:             16735962345
wheelhouse SHA256:       38edf8389bf0c8b30febcc8b40b77eb8d3cc1b017a9bf66da0541b43feea1501
SHA256SUMS file SHA256:  171570c6e78e897ac6b9e63c1f6d7f6eed04363ebb55e40ccd29688c5a718d32
```

The independent fresh short gate passed strict repaired-wheelhouse preflight,
binary-only installation of `sagelite[all-needed-extras]==10.9.post63`, `pip
check`, runtime isolation with zero leaks, all 102 selftest checks, all 3,953
installed `--optional=sage` modules with zero failures, and packaged pytest
with 229 passes and 2 skips. The validator exited zero after 1,235.817
seconds.

The separate fresh full gate repeated that contract. Its unrestricted sweep
reported `All tests passed!` after 881.5 seconds; the independent reducer saw
all 3,953 modules and zero failures. Packaged pytest passed 229 tests with 2
skips and 15 warnings. The complete full validator exited zero after 1,636.447
seconds. The build, short gate, full gate, and guarded watcher exit artifacts
all record zero.

The retained authoritative artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-220841-16d6d78012a/wheelhouse
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-220841-16d6d78012a/validation-wheelhouse
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-220841-16d6d78012a/validation-wheelhouse/SHA256SUMS
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-220841-16d6d78012a/validation/short-post63/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-220841-16d6d78012a/validation/full-post63/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-220841-16d6d78012a/validation/full-post63/doctest-installed-linux-aarch64-cp314-post63-full-20260718-230817.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-220841-16d6d78012a/validation-full-command.log
```

Cleanup removed only the completed full-validation venv, its two generated
homes, and the disposable source checkout and host venv. The exact source is
recoverable from the retained verified bundle. Both wheelhouses and all
validation evidence remain, and the guest has 105,984,348,160 bytes free.
Exact pushed `post63` source `16d6d78012a` is accepted locally for this cell.
The public preview remains unchanged; no artifact was published.

## 2026-07-18 Post63 Synchronized Rebuild Start

The higher-priority Linux `x86_64` target is reachable, but its required
`/mnt/cocalc-scratch` bulk mount remains absent. That path resolves to the
24 GB root filesystem with 15,028,146,176 bytes free. The old CPython 3.12
`post60` services are inactive with successful status, but their bulk run root
is not visible, so no result was inferred and no x86_64 build was started.
The directly fetched public `dev/manifest.json` remains the 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primaries from `post8` and `post9`.

Native macOS and its Linux aarch64 Lima guest were idle. The guest initially
had 106,578,915,328 bytes free, below the binary 100 GiB heavy-build
threshold. Deliberate cleanup reverified and archived the complete inventory
of one superseded `post29` CPython 3.13 closure, then removed that regenerated
closure and two unused test-container images. It also reverified and archived
the complete inventories of the superseded `post60` and rejected `post61`
CPython 3.14 closures before removing them. Their summaries, reduced
analyses, logs, and exit artifacts remain, as do the accepted current
`post62` CPython 3.12 and 3.14 closures and the synchronized `post63` CPython
3.13 closure. This restored 107,941,404,672 bytes free in the guest; the
outer `/Volumes/sage` filesystem also remained above 100 GiB free.

Exact pushed `post63` source
`16d6d78012a4971870e165e3ae948a24b8f7ed9c` is now building natively for
Linux aarch64 CPython 3.14 at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-220841-16d6d78012a
sagelite-post63-arm-cp314-build.service  main PID 2095391
sagelite-post63-arm-cp314-watch.service  main PID 2095398
```

The retained 145,792,413-byte depth-one bundle reverified with SHA256
`89c36c7de5b51212c1d1dc386ead6dc85dbd3b39188f6cbe95ff463cf5a83e20`.
The detached checkout is clean at the exact selected SHA and reports version
`10.9.post63`. All 191 CPython 3.12 seed-wheel hashes and all 180 CPython
3.14 ABI-seed hashes passed before launch. The actual pinned manylinux
container reports Linux `aarch64` and CPython 3.14.3. The guarded watcher
will assemble the strict closure and run independent fresh short and full
gates only after build success. Launcher hashes are:

```text
38a77016a6807f8e4b77049ec78eb226cea02e728c7575c256e1c39fa29e89fc  start-build.sh
01fd98a3831ac51f943a45557863a420d4fbc5031b855b6da2ac48b2b86ad0cf  validate-after-build.sh
1bb0d35374fe3b73de34e67bcd93f3bbd3406fdd9ecfddd1677eaf1c4b76c4c1  watch-and-validate.sh
```

No `post63` CPython 3.14 wheel, validation pass, cell acceptance, or
publication is claimed yet.

## Current status

Native Linux `aarch64` CPython 3.14 is `full` for Sagelite `10.9.post63`.
Exact pushed source `16d6d78012a4971870e165e3ae948a24b8f7ed9c` produced a
repaired primary and strict 180-wheel closure. Independent fresh short and
full gates passed strict preflight, wheel-only installation of
`sagelite[all-needed-extras]`, `pip check`, runtime isolation with zero leaks,
all 102 selftests, all 3,953 installed standard modules with zero failures,
and packaged pytest with 229 passes and 2 skips. The unrestricted sweep took
881.5 seconds. This synchronizes the cell with the selected release-candidate
revision and retains the narrowed `Integer.digits` signal guard validated by
the earlier `post62` baseline.

The earlier accepted `post38` primary was compiled against final CPython
3.14.3 and validated under CPython 3.14.6. It includes the fix that avoids the
unstable private `PyInterpreterState` atexit offset on Python 3.14 and later.
Earlier `post33` and `post36` attempts established the dependency closure and
exposed the prerelease and patch-level ABI failures documented below; neither
supplies the current release-candidate acceptance evidence.

The initial `post33` authoritative run root was:

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

At `2026-07-15T05:20:57Z`, the `post34` build exited 1 after 32 minutes. It
successfully completed all 4,903 primary installation entries against stable
CPython 3.14.3, injected 3,375 native headers, and had auditwheel assign the
expected `manylinux_2_27_aarch64.manylinux_2_28_aarch64` tags. The repair
helper also produced `pplpy`, Maxima runtime, and QEPcad runtime wheels in
cibuildwheel's repair destination. cibuildwheel 3.4.1 then rejected that
destination because its current contract requires exactly one repaired wheel.
The container was removed and the run wheelhouse remained empty, so no
`post34` wheel-built claim is made. The watcher saw build exit 1 and stopped
without assembling a closure or starting validation.

The durable failure evidence is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-044758-49015d0a2b45/command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-044758-49015d0a2b45/exit-code
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-044758-49015d0a2b45/validation-follow.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-044758-49015d0a2b45/validation-follow-exit-code
```

Cleanup retained those logs, metadata, orchestration scripts, exit artifacts,
and disk snapshots, and removed only the disposable source checkout and host
venv. Guest free space increased to 103,187,791,872 bytes, above the
100,000,000,000-byte heavy-build threshold used by these native runs.

Exact pushed commit `a32742fac4a36d214cfb40a8c175fb0687a1d8c4`
separates companion outputs into a host-mounted staging directory, leaves
only the repaired primary in cibuildwheel's destination, and collects the
companions into the requested wheelhouse after cibuildwheel succeeds. It also
advances the version to `10.9.post35` rather than reusing the observed
`post34` filename. Focused repair-contract tests passed 5 tests, and eight
companion-repair metadata assertions passed. The broader companion metadata
file had 11 pre-existing failures outside this failure class.

The new exact-SHA source bundle has SHA256:

```text
ce256c99045a2db81818be824d2f88d4e9cd8fe62c910705d8d805ed21faf9c0
```

That hash matched on the controller, outer Mac, and Linux guest. The new run
root and durable services are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-052653-a32742fac4a3
sagelite-post35-cp314-r10-build.service
sagelite-post35-cp314-r10-validate.service
```

At `2026-07-15T05:27:15Z`, both services were active. The build had begun
preparing the exact bundle, while the watcher was waiting for its exit
artifact. On success it will reuse the accepted companion closure plus the
CPython 3.14 `cysignals` and `pycosat` wheels, run the explicit
`--optional sage --short 600` strict gate, and start a fresh full validation
only if that gate passes. This is forward-progress evidence only.

## Public preview state

The directly fetched public `dev/manifest.json` remained generated at
`2026-07-09T17:17:42.743310+00:00`, with 177 wheels and fourteen Sagelite
primary wheels from `10.9.post8` and `10.9.post9`. There is no public
`post33` primary and no Linux aarch64 CPython 3.14 primary. No publication was
attempted.

## Post35 repair-staging failure and post36 retry

The `post35` build service finished with exit code 1 at
`2026-07-15T06:06:15Z`; its watcher recorded the same exit and did not start
closure assembly or validation. The exact pushed source remained clean. The
build completed all 4,903 primary installation entries against stable CPython
3.14.3, built the raw primary, entered the repaired-wheel path, and produced
the rebuilt `pplpy` and QEPcad companion wheels in the separate companion
staging directory. The Maxima companion builder then failed with:

```text
repaired sagelite wheel not found in /host/sagelite-companion-wheelhouse
```

The primary was correctly located in cibuildwheel's distinct repair
destination. The earlier staging change reassigned the general companion
destination variable, but the Maxima builder still used that variable when it
needed to inspect the repaired primary for the bundled ECL soname. Cibuildwheel
discarded the disposable container output after the repair command failed, so
the run retained no wheel and no `post35` wheel-built claim is made.

The durable failure evidence is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-052653-a32742fac4a3/command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-052653-a32742fac4a3/exit-code
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-052653-a32742fac4a3/validation-follow.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-052653-a32742fac4a3/validation-follow-exit-code
```

Exact pushed commit `c483e52c63c5b4fab6181c420307c3cc85cf926a`
keeps the primary repair directory in a separate immutable variable and uses
it for the Maxima lookup after companion staging begins. It advances the
preview version to `10.9.post36`, because the failed `post35` repair produced
versioned bytes inside its disposable container. All five focused
repair-contract assertions and shell syntax checks passed.

Cleanup retained the failed run's logs, metadata, scripts, disk snapshots, and
exit artifacts and removed only its disposable source checkout and host venv.
The guest then had 102,879,617,024 bytes free, above the exact 100 GB
heavy-build threshold. The new exact-SHA source bundle has SHA256:

```text
53d9379bc1004b71aa3c59e4770c809d50fa45ed84d0a29d0780485dc782da93
```

That hash matched on the controller, outer Mac, and Linux guest. The new run
root and durable services are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-061101-c483e52c63c5
sagelite-post36-cp314-r11-build.service
sagelite-post36-cp314-r11-validate.service
```

At `2026-07-15T06:12:27Z`, both services were active, the detached guest
checkout reported the exact pushed SHA with a clean status, and CIBW had
started its stable CPython 3.14 native aarch64 preparation. This is
forward-progress evidence only; no `post36` wheel, install, smoke, short-gate,
or full result is claimed yet.

## Post36 collector recovery and post37 staging fix

The `post36` build reached a repaired primary and completed all three companion
builds. Cibuildwheel copied this primary into the run wheelhouse:

```text
sagelite-10.9.post36-cp314-cp314-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   237279082 bytes
sha256: 2d3134cd308b5462ef0646bd8b092effea702165efe1d4d92da7065930b2f4f2
```

The separate repair destination contained the rebuilt `pplpy`, Maxima, and
QEPcad wheels, but `/host` inside cibuildwheel maps the outer guest filesystem
root. The repair command therefore wrote them to
`/sagelite-companion-wheelhouse`, while the outer wrapper inspected
`source/sagelite-companion-wheelhouse`. The wrapper exited 1 with the exact
error `repair completed without producing companion wheels`, and its watcher
correctly did not start validation. The failed service artifacts remain at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-061101-c483e52c63c5
```

The exact root-staged companion artifacts were preserved and hash-inventoried
with the primary in this recovery run:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-070525-c483e52c63c5

pplpy-0.9.0.post1-cp314-cp314-manylinux_2_24_aarch64.manylinux_2_28_aarch64.whl
sha256: b3ab72ec7367621dda18bfefcccdda9db17657aeebe71ce5d7489b04a8ad7553

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256: df649384f88f29bb0044f62992ab9adeeeb10aa4056151e9a2bd3c125300bb37

sagelite_qepcad_runtime-10.9.post3-py3-none-manylinux_2_28_aarch64.whl
sha256: 57f72eae9bde1b21255f16c95b4f7521cbe492ef8073feb104b9a4297741c411
```

The first recovery validation resolved all 167 wheels but exited 2 before the
strict gate because its source checkout was a symlink whose target was outside
the Docker bind mount. No install or test result is claimed from that attempt.
The replacement uses an exact clean local copy of source
`c483e52c63c5b4fab6181c420307c3cc85cf926a` and runs durably as:

```text
sagelite-post36-cp314-r13-recovery-validate.service
```

At `2026-07-15T07:08:22Z`, it was active and reassembling the 167-wheel closure
before the explicit `--optional sage --short 600` strict gate. It will start a
fresh explicit `--optional sage --full` validation only if the short gate
passes. This is forward-progress evidence only.

Exact pushed commit `09cc51c9c4525428a7d6bc42500fdc2251ea7999`
replaces the fixed root-relative companion path with a marker that the outer
wrapper expands to `/host` plus its actual absolute staging directory. It
advances the preview version to `10.9.post37`; the six focused repair-contract
tests and both Linux shell syntax checks pass. The remote `develop` ref was
verified at that exact SHA. No `post37` wheel or validation result is claimed.

## Post36 stable-patch failure and post38 retry

The corrected recovery service finished at `2026-07-15T07:24:10Z` with exit
code 16. The strict profile accepted all 167 wheels in the
16,620,400,068-byte closure. A fresh wheel-only installation of
`sagelite[all-needed-extras]==10.9.post36`, `pip check`, and all 102 selftest
probes passed. Packaged pytest also passed 215 tests with 2 skips. The explicit
`--optional sage --short 600` gate then reported every one of its 3,953 modules
as killed by a segmentation fault, so no short or full pass is claimed.

The common failure remained `sage.cpython.atexit._get_exithandlers()`. A direct
call in the installed validation environment exited 139. Although the primary
now used final CPython 3.14.3 rather than the earlier beta, it still compiled
the private `PyInterpreterState` layout into the extension. CPython 3.14.6
changed an earlier interpreter-state member, shifting the later `atexit`
member. Comparing the upstream 3.14.3 and 3.14.6 internal headers confirmed
that patch-release layout change. Stable release level alone therefore cannot
make this private offset safe across CPython 3.14 patch releases.

Exact pushed commit `a2bdbbb674e80db5fa5bde37fe5fdf3f31983390`
removes the private interpreter-state lookup on Python 3.14 and later. It
registers a uniquely identifiable temporary callback, discovers the owning
callback list through Python object references, copies the existing entries,
and unregisters the temporary callback in a `finally` block. The existing
private-array implementation remains confined to Python before 3.14. The
preview version advances to `10.9.post38`.

Focused native aarch64 proof compiled the generated extension against CPython
3.14.3 in the pinned manylinux image and loaded it under CPython 3.14.6. The
handler snapshot and `restore_atexit(clear=True)` round trip passed where the
`post36` extension exited 139. Compiling and running the unchanged branch under
CPython 3.13.14 also passed.

The failed validation venv was the only large disposable artifact removed;
all summaries, logs, reductions, manifests, inventories, wheelhouses, and exit
artifacts remain. This restored 100,724,989,952 bytes free, just above the
100,000,000,000-byte heavy-build threshold. The new exact-SHA bundle has
SHA256:

```text
b33dfe92ae1b378976af772a839714c363803da59d7476ef139449c4e50dc7b1
```

That hash matched on the controller, outer Mac, and Linux guest. The new run
root and durable services are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-074210-a2bdbbb674e
sagelite-post38-cp314-r14-build.service
sagelite-post38-cp314-r14-validate.service
```

At `2026-07-15T07:42:55Z`, both services were active, the detached guest
checkout reported the exact pushed SHA with a clean status, and no build exit
artifact existed. The gated watcher will assemble a fresh strict closure, run
the explicit `--optional sage --short 600` validation, and start a fresh
explicit `--optional sage --full` validation only if the short gate passes.
This is forward-progress evidence only; no `post38` wheel, install, smoke,
short-gate, or full result is claimed yet.

## Post38 full installed-suite pass

The durable `post38` build finished at `2026-07-15T08:16:05Z` with exit code
zero. The exact detached source checkout remained clean at pushed commit
`a2bdbbb674e80db5fa5bde37fe5fdf3f31983390`. The repaired primary is:

```text
sagelite-10.9.post38-cp314-cp314-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   237286104 bytes
sha256: 9b00da0505c50815b6b7f9923c3f75653fcf15bf260961d6cb41493b7b8de207
```

The same contract rebuilt these three companion wheels and collected them
through the corrected `post37` staging path:

```text
pplpy-0.9.0.post1-cp314-cp314-manylinux_2_24_aarch64.manylinux_2_28_aarch64.whl
sha256: 1dadcd832f3d39abb678bbec2469f52bb960c5e72fe417a790bc17b9da227cd9

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
sha256: dc8b5dba2668e26663803df4f0111d13a47e697dd516a73cc281f55ae84b408d

sagelite_qepcad_runtime-10.9.post3-py3-none-manylinux_2_28_aarch64.whl
sha256: b66ba9ec8858e6a7d17539bd86017118f7c0de5f2d92dcb8c969e82c26221c34
```

The watcher assembled and hash-inventoried a 167-wheel closure containing one
primary, 68 companions, and 98 third-party wheels. It totals 16,620,407,090
bytes and has wheelhouse digest
`06e3c51cd43c2cbca0ce2250456f1b080abbbb11d6e9cacb98b15a2bfed4cd3f`.
The strict profile found all 68 requested Sagelite dependencies and accepted
every Python, ABI, architecture, platform, repair, and duplicate-wheel check.

The explicit short gate used:

```text
--package sagelite[all-needed-extras]==10.9.post38
--strict-repaired-wheelhouse-preflight
--optional sage
--short 600
--nthreads 8
```

Its fresh CPython 3.14.6 wheel-only installation and `python -m pip check`
passed. All 102 `sagelite-selftest` probes passed. The installed doctest sweep
ran all 3,953 modules and reported `All tests passed!`; reduced analysis found
zero failed modules. The gate finished at `2026-07-15T08:38:34Z` with exit
code zero.

The watcher then deleted only the short validation venv and started a separate
fresh full validation with the identical wheel contract and these explicit
options:

```text
--package sagelite[all-needed-extras]==10.9.post38
--strict-repaired-wheelhouse-preflight
--optional sage
--full
--nthreads 8
```

That independent wheel-only installation, `pip check`, runtime collection,
and all 102 selftest probes passed. The complete installed standard sweep ran
all 3,953 modules, reported `All tests passed!`, and reduced to zero failed
modules. Packaged pytest passed 215 tests with 2 skips and 15 warnings. The
full validator started at `2026-07-15T08:39:02Z`, finished at
`2026-07-15T09:06:07Z`, and recorded exit code zero; its durable wrapper also
exited zero.

Both doctest processes spent several minutes in ECL/Maxima finalization after
printing their clean summaries. A read-only performance sample of the short
run showed active ECL and Boehm GC work rather than an atexit discovery loop;
both processes completed naturally and the reducers exited zero.

The authoritative artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-074210-a2bdbbb674e/wheelhouse/SHA256SUMS
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-074210-a2bdbbb674e/validation-wheelhouse/SHA256SUMS
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-074210-a2bdbbb674e/validation/short-post38/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-074210-a2bdbbb674e/validation/short-post38/doctest-installed-linux-aarch64-cp314-post38-short-20260715-082011.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-074210-a2bdbbb674e/validation/full-post38/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-074210-a2bdbbb674e/validation/full-post38/doctest-installed-linux-aarch64-cp314-post38-full-20260715-084145.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-074210-a2bdbbb674e/validation-full-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-074210-a2bdbbb674e/validation-full-exit-code
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-074210-a2bdbbb674e/validation-follow-exit-code
```

Cleanup removed only the completed full validation venv. All wheelhouses,
source, logs, summaries, reductions, manifests, inventories, exit artifacts,
and the small performance sample remain. The Linux guest then had
102,352,547,840 bytes free, above the 100,000,000,000-byte heavy-build
threshold used by these native runs.

The public `dev/manifest.json` remained generated at
`2026-07-09T17:17:42.743310+00:00`, with 177 wheels and fourteen Sagelite
primaries from `post8` and `post9`. There is no public Linux aarch64 CPython
3.14 primary, and no publication was attempted.

## 2026-07-17 Post54 Release-Candidate Rerun

The scheduled iteration first retried the higher-priority Linux `x86_64`
CPython 3.14 builder. The `host` SSH alias timed out during connection, so no
x86_64 work was started. The controller read the R2 object directly and
confirmed that the public `dev/manifest.json` is still the 177-wheel set
generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primaries split between `10.9.post8` and `10.9.post9`.

The independent native Linux arm64 backend was idle and reported Linux
`aarch64`. The outer Mac had 107 GiB available on `/Volumes/sage`, and the
guest had 105,595,858,944 bytes available before the build, above the explicit
100,000,000,000-byte heavy-build threshold. No other Sagelite build,
validator, or user service was active.

Exact pushed source `4071f482bcc3865116d57391b00227ae0a9f28d4`
(`10.9.post54`) was selected for the release-candidate rerun. Its
145,752,626-byte shallow exact-HEAD bundle has SHA256
`6dcb540bb8aa59de419210b0a21f6173e4dba99264a4e8a91d20b2b67a94c8bf`;
that hash matched on the controller, outer Mac, and Linux guest. The detached
guest checkout reports the exact source SHA and a clean status.

The durable build and gated validation ran at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260717-023339-4071f482bcc
sagelite-post54-rc-cp314-build.service
sagelite-post54-rc-cp314-validate-r2.service
sagelite-post54-rc-cp314-full-r1.service
```

The build uses the repository's native Linux CIBW contract with
`CIBW_BUILD=cp314-manylinux_aarch64`, `CIBW_ARCHS=aarch64`, and CPython 3.14
paths throughout. The selected EPEL mirror timed out twice while fetching
filelists metadata, then recovered on its automatic retry. The build finished
at `2026-07-17T03:22:04Z` with exit code zero. Its repaired outputs are:

```text
sagelite-10.9.post54-cp314-cp314-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   237288901 bytes
sha256: 4ae5dbfc89bc1728dc103d5605d9e9468a64a2a0c9d43d7fea7be457ff595764

pplpy-0.9.0.post1-cp314-cp314-manylinux_2_24_aarch64.manylinux_2_28_aarch64.whl
size:   9380835 bytes
sha256: be0772459236f146c55d16cd53ac208c4577f68ed0751914f87aa0d0bd62c104

sagelite_maxima_runtime-10.9.post15-py3-none-manylinux_2_28_aarch64.whl
size:   66578982 bytes
sha256: 552975fbdcfd4fbaf514008709e5bab24b78b46c8bf71bbe1aa71064f24aea32

sagelite_qepcad_runtime-10.9.post4-py3-none-manylinux_2_28_aarch64.whl
size:   5243824 bytes
sha256: a901c1e3c65248a947b0e2ccba497a381bfc3f8b968cf68861ca8990b2e7d11d
```

The initial watcher used the obsolete `post38` companion set and stopped
before installation because `sagelite-meataxe-runtime 10.9` did not satisfy
the current `>=10.9.post1` requirement. A first orchestration retry passed the
wheelhouse directory rather than its parent to the validator and therefore
exposed only four wheels. Both non-source failures are preserved. The corrected
retry combined accepted ABI-independent `post54` companions, the accepted
CPython 3.14 `cysignals` and `pycosat` wheels, and the four new build outputs.
Fresh binary-only resolution produced a 180-wheel closure: one primary, 81
companions, and 98 third-party wheels. It totals 16,735,945,069 bytes and has
wheelhouse digest
`9d05b995f82e1e6799998fa599064ecc022c908e6387d62b12110a555204f703`.
All 68 requested Sagelite dependencies and every strict tag, architecture,
platform, repair, and duplicate-wheel check passed.

The explicit short gate used:

```text
--package sagelite[all-needed-extras]==10.9.post54
--strict-repaired-wheelhouse-preflight
--optional sage
--short 600
--nthreads 8
```

Its fresh CPython 3.14.6 wheel-only installation, `pip check`, runtime
isolation, and every selftest passed. The installed doctest sweep ran all
3,953 modules, reported `All tests passed!`, and reduced to zero failed
modules. Packaged pytest passed 229 tests with 2 skips and 15 warnings. The
short gate finished at `2026-07-17T03:46:55Z` with exit code zero.

The first independent full run used the same contract with `--full`. It ran
all 3,953 modules but failed eight examples in
`sage.rings.polynomial.multi_polynomial_libsingular.pyx`: four repeated
`GF((2^29-3)^2)` constructors unexpectedly raised that the order was not a
prime power, causing four immediately following examples to use the prior
ring. The failed summary, log, analysis, and exit code 1 are retained under
`validation/full-post54-r0-failed` and `validation-full-r0-*`.

A native CPython 3.14 focused replay used the identical failing random seed.
One hundred calls reported the correct `(536870909, 2)` perfect-power
decomposition with no constructor failures, and the complete polynomial
module reported `All tests passed!`. Its log is retained at
`validation/focused-post54/gf-prime-power-replay.log`. No source or wheel was
changed before the acceptance rerun.

The separately named fresh full rerun used a new `full-post54-r1` install
directory and the unchanged 180-wheel closure. Strict preflight, wheel-only
installation, `pip check`, runtime isolation, and every selftest passed. Its
unrestricted installed sweep reported `All tests passed!` after 916.6 seconds;
analysis saw all 3,953 modules and zero failures. Packaged pytest passed 229
tests with 2 skips and 15 warnings. The validator ran from
`2026-07-17T04:16:29Z` through `2026-07-17T04:44:09Z`, took 1,661.187 seconds,
and recorded exit code zero.

The authoritative current artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260717-023339-4071f482bcc/wheelhouse/SHA256SUMS
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260717-023339-4071f482bcc/validation-wheelhouse/SHA256SUMS
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260717-023339-4071f482bcc/validation/short-post54/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260717-023339-4071f482bcc/validation/full-post54-r0-failed/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260717-023339-4071f482bcc/validation/focused-post54/gf-prime-power-replay.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260717-023339-4071f482bcc/validation/full-post54-r1/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260717-023339-4071f482bcc/validation/full-post54-r1/doctest-installed-linux-aarch64-cp314-post54-full-20260717-041908.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260717-023339-4071f482bcc/validation-full-r1-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260717-023339-4071f482bcc/validation-full-r1-exit-code
```

Cleanup removed only the accepted rerun's completed 21 GiB validation venv.
Both wheelhouses, the clean source checkout, failed-run evidence, focused
replay, accepted summaries, reductions, manifests, logs, and exit artifacts
remain. The guest then had 103,443,734,528 bytes free, above the explicit
100,000,000,000-byte heavy-build threshold.

The public `dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primaries from
`post8` and `post9`. No publication was attempted.

## 2026-07-18 Post60 Synchronized Rerun Start

The higher-priority Linux `x86_64` CPython 3.12 job could not be reconciled:
all three bounded connections through the required `host` SSH alias timed out.
The possibly surviving build and watcher were left untouched. The public
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`; no `post60` artifact was assumed public.

Independent preflight found the outer Mac reachable as `arm64`, its Lima
instance running, and the guest idle as native Linux `aarch64` with no Docker
container or Sagelite automation service active. The guest initially had
107,511,595,008 bytes free. Cleanup removed only the completed CPython 3.13
post60 run's disposable source checkout, host venv, and four install-home
directories. Its strict 191-wheel closure, accepted summaries, reductions,
logs, and exit artifacts remain. The cleanup restored 108,741,181,440 bytes
free, above the binary 100 GiB heavy-build threshold.

The exact source input is pushed commit
`22a2cb56739940d7a9eb313e997fd0a004a9ea36` (`10.9.post60`). Its retained
145,770,108-byte shallow bundle has SHA256
`84f2902d2051d598b04430d9ef95b4e9fe672f4d02a0701a653d2764b82285dc`,
which was reverified immediately before launch. The new run is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-031637-22a2cb56739
```

The detached source checkout reports the exact selected SHA and a clean
status. The build uses the repository CIBW helpers with
`CIBW_BUILD=cp314-manylinux_aarch64`, `CIBW_ARCHS=aarch64`, CPython 3.14
paths throughout, the retained bulk prefix, and the bounded 2 GiB per-ABI
ccache. The actual pinned manylinux container reports `aarch64` and CPython
3.14.3. Its guarded watcher will combine the accepted synchronized CPython
3.12 post60 companion closure, the new primary and rebuilt wheels, and the
accepted CPython 3.14 `cysignals` and `pycosat` supplements. It will then
resolve the binary-only closure and run independent strict short and full
gates with explicit `--optional sage`.

The durable services are:

```text
sagelite-post60-arm-cp314-build.service
sagelite-post60-arm-cp314-watch.service
```

At the launch checkpoint both services were active, with main PIDs 855079 and
855086. The source was bootstrapped and the command log was growing; no build
exit artifact or wheel existed yet. The launcher hashes are:

```text
ea2ecc11d064cbad84f7913da31864db0d4129e0b979a657f98a65cd2ec04d8c  start-build.sh
3350bb883d8fa1af201f8b1019fbe7c3b7bcaf9e0663a7e6216c53d864ad7af4  validate-after-build.sh
1bb0d35374fe3b73de34e67bcd93f3bbd3406fdd9ecfddd1677eaf1c4b76c4c1  watch-and-validate.sh
```

No `post60` primary wheel, closure, install, short gate, full gate, or
publication result is claimed yet. A resumed iteration must reconcile both
services, `command.log`, log growth, the build `exit-code`, wheel inventory,
and validation artifacts before launching any other heavy job on `m1`.

## 2026-07-18 Post60 Synchronized Full Acceptance

The resumed iteration first attempted the higher-priority Linux `x86_64`
CPython 3.12 reconciliation. All three bounded connections through the
required `host` alias timed out, so that possibly surviving job was left
untouched. The public `dev/manifest.json` was fetched directly and remained
the 177-wheel set generated at `2026-07-09T17:17:42.743310+00:00`, with
fourteen Sagelite primaries and no `post60` artifact.

The native Linux aarch64 build was healthy when reconciled: both guarded
services were active, the actual manylinux container was `aarch64`, the
command log and live compiler processes showed forward progress, and the
source checkout was clean at exact pushed SHA
`22a2cb56739940d7a9eb313e997fd0a004a9ea36`. The build completed with exit
code zero and produced four repaired wheels totaling 318,492,831 bytes. The
primary is:

```text
sagelite-10.9.post60-cp314-cp314-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   237289190 bytes
sha256: c0efdcb2737ec69e7790a027fca870f78388921515491ccc55172342271169ad
```

The other three new outputs are CPython 3.14 `pplpy`, the Maxima runtime, and
the QEPCAD runtime. The guarded watcher combined them with the synchronized
CPython 3.12 companion set and the accepted CPython 3.14 `cysignals` and
`pycosat` supplements. Binary-only resolution produced a strict closure with
these properties:

```text
wheels:              180
Sagelite projects:    82 (1 primary and 81 companions)
third-party projects: 98
total bytes:          16735951613
wheelhouse SHA256:    285cdd9c9d6d0afe7a405a1c29155a271584f4a075affdba5e3fe738cd37b6c0
```

The independent fresh short gate passed strict repaired-wheelhouse preflight
and binary-only installation of `sagelite[all-needed-extras]==10.9.post60`.
It also passed `pip check`, runtime isolation, all 102 selftests, and all 3,953
installed standard
modules with zero failures, and packaged pytest with 229 passes and 2 skips.
The doctest sweep took 547.9 seconds; the validator exited zero after
1,334.111 seconds.

The separately named fresh full gate passed the same strict preflight,
installation, `pip check`, runtime isolation, and selftests. Its unrestricted
installed `--optional=sage` sweep reported `All tests passed!` after 898.3
seconds. The reducer saw all 3,953 modules and zero failures. Packaged pytest
again passed 229 tests with 2 skips and 15 warnings. The full validator ran
from `2026-07-18T04:14:31Z` through `2026-07-18T04:42:03Z`, took 1,652.432
seconds, and recorded exit code zero. The watcher also exited zero.

The authoritative current artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-031637-22a2cb56739/wheelhouse
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-031637-22a2cb56739/validation-wheelhouse/SHA256SUMS
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-031637-22a2cb56739/validation/short-post60/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-031637-22a2cb56739/validation/full-post60/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-031637-22a2cb56739/validation/full-post60/doctest-installed-linux-aarch64-cp314-post60-full-20260718-041712.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-031637-22a2cb56739/validation-full-command.log
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-031637-22a2cb56739/validation-full-exit-code
```

Cleanup removed only the completed 21,840,131,519-byte full-validation
install home and the run's disposable source checkout and host venv. The
exact build wheelhouse, strict closure, summaries, manifests, reduced
analyses, logs, and exit artifacts remain. Guest free space increased to
107,425,660,928 bytes. Exact pushed `post60` source `22a2cb56739` is accepted
locally for this cell. No publication was attempted.

## 2026-07-18 Post61 Synchronized Rerun Start

The required `host` alias was reachable again as Linux `x86_64`, but the
expected `/mnt/cocalc-scratch` bulk mount was absent: that path resolved to
the 24 GB root filesystem with about 14 GB free. The old exact `post60` Linux
x86_64 CPython 3.12 run root was therefore not visible on this host. Its two
recorded services were inactive with zero service status, but no build or
validation result is inferred because the assigned bulk artifacts could not
be inspected. No heavy x86_64 job was started.

The public `dev/manifest.json` was fetched directly and remains the 177-wheel
set generated at `2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite
primary wheels and no `post60` or `post61` artifact.

Independent preflight found `m1` reachable as native `arm64` and its Lima
guest idle as Linux `aarch64`. The guest initially had 108,068,257,792 bytes
free, only about 694 MB above the binary 100 GiB build threshold. Precise
cleanup affected only the superseded accepted `post54` CPython 3.14 build and
closure directories plus its obsolete resolver seed. Their SHA256 lists and
inventories were first archived under that run's retained validation tree;
all summaries, logs, reduced analyses, focused replay, and exit artifacts
remain. The current accepted `post60` strict closure was not touched. Cleanup
restored 108,894,273,536 bytes free.

The exact source input is pushed commit
`33f8a4dae1da1571b07b9bbf8adddfe07a41af6c` (`10.9.post61`). Its retained
145,788,566-byte shallow bundle again verified with SHA256
`c2670796bf1b7a7254b7a9824f1caedd60dbb5295c2c08d658ce3bf5e00a4ab7`.
The new run is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-123524-33f8a4dae1d
```

Its detached checkout reports the exact selected SHA and a clean status. The
actual pinned manylinux container reports Linux `aarch64` and CPython 3.14.3.
The build uses `CIBW_BUILD=cp314-manylinux_aarch64`, `CIBW_ARCHS=aarch64`,
the retained bulk prefix, and the repository Linux build and repair helpers.
The guarded watcher will combine the accepted `post61` CPython 3.12 companion
closure, the new build outputs, and the accepted CPython 3.14 `cysignals` and
`pycosat` supplements before binary-only resolution and independent strict
short and full gates with explicit `--optional sage`.

The durable services are:

```text
sagelite-post61-arm-cp314-build.service
sagelite-post61-arm-cp314-watch.service
```

At the checkpoint both services were active with main PIDs 1319097 and
1319104. The source was bootstrapped, the native manylinux container was in
prerequisite setup, and neither build nor validation had an exit artifact.
The launcher hashes are:

```text
f523191ba438f0efeecb8fb5813247fbf194affd2f2e00624b0c43e5098bb93e  start-build.sh
b26bf83ae996825975634c47bf5cd4339c149cbaf5994b5395dd8713c9d6df44  validate-after-build.sh
1bb0d35374fe3b73de34e67bcd93f3bbd3406fdd9ecfddd1677eaf1c4b76c4c1  watch-and-validate.sh
```

No `post61` wheel, closure, install, validation pass, or publication is
claimed. A resumed iteration must reconcile both services, log growth, exit
artifacts, wheel inventory, and validation evidence before launching another
heavy job on `m1`.

## 2026-07-18 Post61 Build, Short Pass, And Full Rerun

The resumed iteration fetched the public `dev/manifest.json` directly. It
remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`; no `post60` or `post61` artifact is
public. The required `host` alias was reachable as Linux `x86_64`, but
`/mnt/cocalc-scratch` still resolved to its 24 GB root filesystem with only
15,028,678,656 bytes free. The recorded CPython 3.12 services were inactive,
but their bulk run root was not visible, so no result was inferred and no
x86_64 build was started.

The exact Linux aarch64 build exited zero and produced this repaired primary:

```text
sagelite-10.9.post61-cp314-cp314-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   237289462 bytes
sha256: 933bc988134159bd8ed94e1339d0b30235e44effa7b73d204c5113c6ee980ac7
```

The guarded watcher combined the synchronized CPython 3.12 `post61`
companions, the new outputs, and the accepted CPython 3.14 `cysignals` and
`pycosat` supplements. Binary-only resolution produced this exact closure:

```text
wheels:              180
Sagelite projects:    82 (1 primary and 81 companions)
third-party projects: 98
total bytes:          16735961528
SHA256SUMS sha256:    94b32e08421691d7487dbf5df23d6fb4955c5fe7584264cc6234d6555056a3cd
```

The fresh short gate exited zero after strict repaired-wheelhouse preflight,
binary-only installation of `sagelite[all-needed-extras]==10.9.post61`,
`pip check`, runtime isolation with zero leaks, all 102 selftest checks, all
3,953 installed `--optional=sage` modules with zero failures, and packaged
pytest with 229 passes and 2 skips.

The separate fresh full gate passed the same setup and packaged pytest, but
its unrestricted sweep rejected two of 3,954 seen modules under random seed
`82629442647405722006767383889818940802`. `sage.rings.integer` raised
`SystemError: calling remove_from_pari_stack() inside sig_on()` in one
`Integer.digits` example. `sage.rings.polynomial.msolve` returned two exact
solutions and one spurious rational approximation for a four-solution ideal.
The reducer recorded two failed modules and two failed examples. Both complete
modules then passed exact-seed focused replays in the unchanged full install:
1,197 integer doctests and 54 `msolve` doctests. The first full gate remains
rejected.

One separately named fresh full rerun from the unchanged strict closure is
active as:

```text
sagelite-post61-arm-cp314-full-rerun1.service
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-123524-33f8a4dae1d/install/full-post61-rerun1
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-123524-33f8a4dae1d/validation/full-post61-rerun1
```

Before launch, guards verified native Linux `aarch64`, exact clean source SHA
`33f8a4dae1d`, the successful build and short-gate exit artifacts, all 180
wheel hashes, no competing Docker container, and more than the required 30
GiB test-only capacity. At the checkpoint the service and fresh
`python:3.14-slim-bookworm` container were active, the binary-only install was
progressing, and the guest had 84,752,695,296 bytes free. No `post61` full
pass or publication is claimed. A resumed iteration must reconcile
`validation-full-rerun1-exit-code`, the validation summary and reduced
analysis, and service/container state before starting other work on `m1`.

## 2026-07-18 Post61 Full Rerun Rejection And Post62 Repair

The separately named fresh full rerun completed with exit code 1. It again
passed strict preflight, binary-only installation, `pip check`, runtime
isolation, all 102 selftests, and packaged pytest with 229 passes and 2 skips.
Its unrestricted sweep tested 3,954 modules in 961.1 seconds and rejected only
`sage.rings.integer`: the same large `Integer.digits` example raised
`SystemError: calling remove_from_pari_stack() inside sig_on()`. The reducer
recorded one failed module and one failed example. This second independent
occurrence makes the failure coherent rather than transient.

The traceback enters `Integer.digits`, enables its broad outer `sig_on()`, and
then calls `exact_log()`. For this large value, `exact_log()` uses real
interval arithmetic; normal Python cleanup can release a PARI-backed object
while that unrelated signal region is active. The `post62` working change
moves `sig_on()` below exact digit counting, digit-object allocation, and
power-table construction, immediately around only `_digits_naive` or
`_digits_internal`. The edited Cython source passes standalone translation
with the repository's required `cdivision=True` directive. Exact committed
source still needs a focused installed-module stress replay, a repaired wheel,
and independent fresh short and full gates; no `post62` result or publication
is claimed.

## 2026-07-18 Post62 Exact Rebuild Start

The repair was committed, pushed, and verified as exact source
`b68997abc23abff78d8744ed7bb3cfa9c926b7c3` (`10.9.post62`). Its standalone
Cython translation passed with the repository's `cdivision=True` directive.
The public `dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primaries and no
`post60`, `post61`, or `post62` artifact.

Cleanup removed only the rejected `post61` validation installs, its disposable
source checkout and host venv, and three superseded CPython 3.14 closure trees
whose complete SHA256 inventories were first archived with their validation
evidence. The accepted `post60` closure and current `post61` closure remain.
Guest free space was 109,266,255,872 bytes immediately before launch, above
the binary 100 GiB heavy-build threshold.

The self-contained depth-one exact-SHA bundle is 145,796,607 bytes with
SHA256:

```text
323f23af946b83e059ce23f06887ea4f720c034db3ee54bc42f5462702d9cfc3
```

That hash matches on the controller, outer Mac, and Linux guest. The exact
detached checkout is clean at the selected SHA. The actual manylinux container
reports Linux `aarch64` and CPython 3.14.3. The durable services and run root
are:

```text
sagelite-post62-arm-cp314-build.service
sagelite-post62-arm-cp314-watch.service
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-151432-b68997abc23
```

Both services are active. The build entered native prerequisite setup, and the
guarded watcher will assemble the strict closure and run independent fresh
short and full gates only after build success. No `post62` wheel, install,
validation pass, or publication is claimed.

## 2026-07-18 Post62 Full Acceptance

The exact native build and guarded watcher both completed with exit code zero.
The repaired primary is:

```text
sagelite-10.9.post62-cp314-cp314-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   237290139 bytes
sha256: 0bb1c787b0e00832e9327fb87c1abc48f0becca56fa213e8d2143aba8a1c46b3
```

The watcher combined the synchronized CPython 3.12 companion set, the new
primary and rebuilt wheels, and the accepted CPython 3.14 `cysignals` and
`pycosat` supplements. Binary-only resolution produced this strict closure:

```text
wheels:           180
total bytes:      16735962205
SHA256SUMS sha256: 166ae7f98a9843bb4f33ae5741ddb3e02de60bd5add715bbb8313014cdc104ec
```

The independent fresh short gate passed strict repaired-wheelhouse preflight,
binary-only installation of `sagelite[all-needed-extras]==10.9.post62`,
`pip check`, runtime isolation with zero leaks, all 102 selftest checks, all
3,953 installed `--optional=sage` modules with zero failures, and packaged
pytest with 229 passes and 2 skips. Its bounded standard sweep took 535.7
seconds.

The separate fresh full gate repeated that contract. Its unrestricted sweep
reported `All tests passed!` after 880.5 seconds; the reducer saw all 3,953
modules and zero failures. Packaged pytest passed 229 tests with 2 skips and
15 warnings. The complete full validator took 1,615.146 seconds and exited
zero. The build, watcher, short gate, full gate, and follow-up exit artifacts
all record zero.

The retained authoritative artifacts are:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-151432-b68997abc23/validation-wheelhouse
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-151432-b68997abc23/validation-wheelhouse/SHA256SUMS
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-151432-b68997abc23/validation/short-post62/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-151432-b68997abc23/validation/full-post62/validation-summary.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-151432-b68997abc23/validation/full-post62/doctest-installed-linux-aarch64-cp314-post62-full-20260718-161439.analysis.md
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-151432-b68997abc23/validation-full-command.log
```

Cleanup removed only the completed run's disposable 21 GB install tree,
465 MB source checkout, and 22 MB host venv. The strict closure and complete
validation evidence remain, and the guest has 108,433,313,792 bytes free.
Exact pushed `post62` source `b68997abc23` is accepted locally for this cell.
The public preview remains unchanged; no artifact was published.
