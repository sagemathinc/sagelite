# Sagelite macOS arm64 CPython 3.12 Validation

## 2026-07-18 Post61 Full Acceptance

The guarded validator completed both independent fresh gates and exited zero
at `2026-07-18T08:19:50Z`.  The short gate passed strict preflight,
binary-only `sagelite[all-needed-extras]==10.9.post61` installation,
`pip check`, all 102 selftest checks, runtime isolation with zero host or
source leaks, all 3,953 installed standard modules with zero failures, and
packaged pytest with 226 passes and 5 skips.  Its standard sweep completed in
477.1 seconds, and the gate exited zero after 1,773.109 seconds.

The separately named full gate repeated the fresh installation, dependency,
selftest, and isolation contract.  Its unrestricted sweep passed all 3,953
installed standard modules with zero failures in 747.9 seconds.  Packaged
pytest again passed with 226 passes and 5 skips, and the gate exited zero after
1,988.185 seconds.  The earlier rare `GF((2^29-3)^2)` decomposition failure
did not recur with the committed square-order repair.  Exact pushed
`10.9.post61` source `33f8a4dae1da1571b07b9bbf8adddfe07a41af6c` is accepted
locally for macOS arm64 CPython 3.12.  No public publication is claimed.

Precise cleanup removed only the two reproducible validation installs and the
now-disposable `post60` and `post61` extracted source/build trees.  The exact
`post61` source archive, repaired 180-wheel closure, hashes, command logs,
runtime manifests, selftest logs, reducers, and validation summaries remain
retained.  The worker finished with 110,707,924,992 bytes free, above the
binary 100 GiB heavy-build threshold.  Durable accepted evidence is at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260718-065714-33f8a4dae1d/
```

## 2026-07-18 Post61 Build Complete And Strict Validation Start

The exact-source build completed with exit code zero at
`2026-07-18T07:13:01Z`.  Repair injected 2,079 native headers, rewrote 23
companion dependencies in 16 Mach-O files, and audited 1,176 dependencies
across 637 Mach-O files.  It produced:

```text
sagelite-10.9.post61-cp312-cp312-macosx_26_0_arm64.whl
  102,263,610 bytes
  0056083a2847e795d38e2e146f9d3684a1b5253ed54c407f27e52c66781cc17e
```

The deterministic strict closure completed with exit code zero at
`2026-07-18T07:15:01Z`.  Its resolver selected all 180 staged projects and
removed none.  The closure contains one primary, 68 companion, and 111
third-party wheels totaling 13,896,963,812 bytes.  The closure inventory has
SHA256
`622f63be408b4e495b306321cc7cf605d78113db1901fe46f6ea5b7e8dd976d6`,
and the independent pip resolution report has SHA256
`9fb059ac3a1b25e8d8eeb2051258f6e1a5f32d00ff7cfd8b3ec6ba16429a9558`.

One guarded validator is active under tmux session
`sagelite_cp312_post61_validate`, with recorded PID 9830.  It starts the
separately named fresh full gate only after a zero short-gate exit.  Both
commands use the exact checksummed closure, strict macOS wheelhouse preflight,
binary-only `sagelite[all-needed-extras]==10.9.post61` installation, a neutral
environment, runtime isolation, every selftest, packaged pytest, and the
installed standard-module sweep.  At this checkpoint the short gate was
installing the resolved closure in its fresh environment.  No short-gate,
full-suite, or publication pass is claimed yet.  Evidence remains under:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260718-065714-33f8a4dae1d/
```

## 2026-07-18 Post61 Exact Rebuild Start

Exact pushed repair commit
`33f8a4dae1da1571b07b9bbf8adddfe07a41af6c` (`10.9.post61`) is the
verified `origin/develop` tip.  Its controller-created archive is 144,083,559
bytes with SHA256
`a708b1fbe826894a03c0ed2606756ff0e60a55c4bd2d6686c24bfb0266dc4314`.
The independently materialized remote tree is
`c74fc7f733b8934357e7db5bdd24208da0540ad8`, matching the committed tree.

Capacity cleanup removed only the two completed disposable `post60` short-
and full-gate install environments.  Their wheelhouse, command logs, reducer,
focused diagnostics, source snapshot, and build evidence remain retained.
The native Darwin `arm64` worker, its Linux arm64 guest, and the target tmux
namespace had no other heavy build.  After the full archive transfer, the
launch guard recorded 107,937,693,696 bytes free, above the binary 100 GiB
threshold.

The native macOS arm64 CPython 3.12.13 build is active under tmux session
`sagelite_cp312_post61_build`, with recorded PID 70928, at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260718-065714-33f8a4dae1d/
```

The durable launcher reuses the proven native dependency prefix, raises the
soft file-descriptor limit to 4,096, and records its output, PID, metadata,
disk state, and eventual exit code below the run root.  Exact archive hash,
source tree, version, architecture, operating system, and interpreter guards
passed.  At this checkpoint the fresh build environment was installing its
pinned native build dependencies.  No `post61` wheel, strict closure, fresh
installation, short gate, full-suite pass, or publication result is claimed
yet.

## 2026-07-18 Post60 Short Pass And Full Rejection

The guarded validator completed both independent fresh gates from the exact
180-wheel `post60` closure.  The short gate passed strict preflight,
binary-only `sagelite[all-needed-extras]` installation, `pip check`, runtime
isolation, every selftest, all 3,953 installed standard modules with zero
failures, and packaged pytest with 226 passes and 5 skips.  Its validator
exited zero after 1,753.648 seconds.

The separate fresh full gate passed the same installation, isolation, and
selftest contract.  Its unrestricted sweep saw 3,954 modules but rejected
`sage.rings.polynomial.multi_polynomial_libsingular` under seed
`213528177385953471796963154323692312109`.  Four repeated
`GF((2^29-3)^2)` constructors unexpectedly rejected the square as a prime
power, and four following examples cascaded from the missing ring.  The
reducer found one failed module and eight failed examples.  Packaged pytest
still passed with 226 passes and 5 skips, and the validator exited 1 after
1,981.702 seconds.  This is the same prime-square decomposition failure seen
once in the earlier Linux aarch64 CPython 3.14 full run, so it is now treated
as a shared source failure rather than a transient acceptance candidate.

An exact-seed replay passed all 1,363 polynomial-module doctests.  One million
fresh primality checks and two million parallel perfect-power decompositions
also passed, confirming the rare nature of the failure.  The `post61` working
repair makes finite-field construction decompose square orders first through
GMP's exact integer square root, recursively preserving the maximal exponent,
before using the general PARI perfect-power path.  A diagnostic source overlay
passed all 150 finite-field-constructor doctests and the complete polynomial
module under the exact failing seed.  The rejected install was restored to its
original SHA256 after the overlay.  A committed exact `post61` rebuild and
both independent fresh gates are required; no `post60` full pass or public
publication is claimed.

All closure, short-pass, full-rejection, reducer, and focused replay evidence
is retained at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260718-050339-22a2cb56739/
```

## 2026-07-18 Post60 Build Complete And Strict Validation Start

The exact-source build started in the preceding checkpoint completed with exit
code zero at `2026-07-18T05:18:11Z`. Repair injected 2,079 native headers,
rewrote 23 companion dependencies in 16 Mach-O files, and audited 1,176
dependencies across 637 Mach-O files. It produced:

```text
sagelite-10.9.post60-cp312-cp312-macosx_26_0_arm64.whl
  102,263,875 bytes
  4b450cf0fc612aca7737f55d1df8b332bfbd18af28bb38b022cb802480dc2566
```

The deterministic strict closure completed at `2026-07-18T05:35:06Z`. It
contains 180 compatible wheels: one primary, 68 companions, and 111
third-party wheels totaling 13,896,964,077 bytes. The closure inventory has
SHA256
`476b952d64ec0eed3fa612b3e06d3f7d05c4184ab5756f7216fc770689f69d84`,
and the independent pip resolution report has SHA256
`2193588c3c9e751ffbaff9f10854650ce0313dcf4845f4739ecd00bf1a65b181`.
Resolution selected all 180 staged projects and removed none.

A single guarded watcher is active under tmux session
`sagelite_cp312_post60_validate`. It runs the fresh neutral-path short gate and
starts a separately named fresh full gate only if the short gate exits zero.
The short gate passed strict 180-wheel preflight, binary-only
`sagelite[all-needed-extras]==10.9.post60` installation, and `pip check`.
At this checkpoint it was collecting the installed runtime manifest before
selftest and the 600-second standard module sweep. The validator environment
sets `PYTHONNOUSERSITE=1`, uses only `/usr/bin:/bin` after the fresh install on
`PATH`, and records `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` explicitly.

This is a completed repaired-wheel and strict-closure result, plus partial
short-gate evidence. No short gate, full-suite pass, or publication is claimed
yet. All durable artifacts are retained at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260718-050339-22a2cb56739/
```

The higher-priority Linux x86_64 CPython 3.12 job remains unreconciled: all
three bounded attempts through the required `host` alias timed out. The public
manifest remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen primary Sagelite wheels and
no `10.9.post60` artifact.

## 2026-07-18 Post60 Release-Candidate Build Start

The scheduled matrix iteration first attempted to reconcile the
higher-priority Linux x86_64 CPython 3.12 job. All three bounded SSH attempts
through the required `host` alias timed out, so that possibly surviving job
was left untouched and no result was inferred. The directly fetched public
`dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels and
no `10.9.post60` artifact.

Independent preflight found `m1` idle and native Darwin `arm64`, with
Homebrew CPython 3.12, 3.13, and 3.14 available. `/Volumes/sage` initially had
111,955,656,704 bytes free, above the 100 GiB heavy-build threshold. Exact
pushed release-candidate source
`22a2cb56739940d7a9eb313e997fd0a004a9ea36` (`10.9.post60`) is an ancestor of
verified `origin/develop` tip `2c4aca1dfb7130d9fcf7ae40b82700bf936bf648`.
It was transferred as an exact-tree archive:

```text
name:   sagelite-22a2cb567399.tar.gz
size:   144070311
sha256: 2664484d573b1626904a337c03818a035f5ab48619d8a4f670df1bbc6c644ec7
tree:   82f7785253d84ab5c634b29aeeb364733e6524fa
```

The native macOS arm64 CPython 3.12.13 build is active under tmux session
`sagelite_cp312_post60_build`, with recorded PID 77663, at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260718-050339-22a2cb56739
```

The durable launcher reuses the proven native dependency prefix, raises the
soft file-descriptor limit to 4,096 before compilation, and records its output,
PID, metadata, disk state, and final exit code below the run root. The source
checkout passed exact SHA, tree, archive hash, version, interpreter, operating
system, and architecture guards. At this checkpoint the log was growing and
the build had entered its 1,795-edge native Ninja compilation. The launcher
script SHA256 is
`6e3e8efafe83375b2809db1b3a09c58e9abf8c67a99efb6ef17019ba177c104f`.

This is exact-source build-start evidence only. No `post60` CPython 3.12
wheel, compatible closure, fresh installation, `pip check`, selftest, short
gate, full-suite pass, or publication result is claimed yet.

## 2026-07-17 Post56 Full Acceptance

The scheduled continuation first retried the higher-priority Linux x86_64
cell, but all three bounded SSH attempts to `host` timed out. The directly
fetched public R2 manifest remained the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, including fourteen Sagelite primary
wheels, so no public state changed.

Exact pushed `10.9.post56` source
`288c3f219682ed6ba6e7a77cb069b94ba0073c13` has tree
`5fbf7601cd1e7d6e81fa8d6e8e0f6190bd87909d`. Its 144,004,948-byte source
archive has SHA256
`50522fcd49a659c85935694767e6c442825a1fa659d6d6844f5a38c4d1b8c781`.
The native Darwin arm64 CPython 3.12.13 build initially stopped in the Maxima
subproject because the process inherited a 256-file soft descriptor limit;
the linker reported `errno=24` while opening SDK stubs. A controlled resume
raised only that limit to 4,096, reused the same verified source and persistent
Meson tree, and completed with no source change. The initial and resume exit
codes are retained as 1 and 0 respectively.

The completed repair produced:

```text
sagelite-10.9.post56-cp312-cp312-macosx_26_0_arm64.whl
  102,263,590 bytes
  6b700467acc9083a7f9176e8ff684f50ab53e48810f6a1f84f2dcacea7561b7b
```

Repair injected 2,079 native headers, rewrote 23 companion dependencies in
16 Mach-O files, and audited 1,176 dependencies across 637 Mach-O files. The
strict compatible closure contains 180 wheels: one primary, 68 companions,
and 111 third-party wheels totaling 13,896,963,792 bytes. Its inventory digest
is `91018519e0f5281b9d5727d83723a6b226516f0652b4a8d2126d9f38682d0181`.

The independent fresh short gate passed strict preflight, binary-only
installation, `pip check`, runtime isolation, all 102 selftests, all 3,953
installed `--optional=sage` modules with zero failures in 484.0 seconds, and
packaged pytest with 226 passes and 5 skips in 270.24 seconds. The validator
exited zero after 1,771.01 seconds.

The separate fresh full gate passed the same installation, isolation, and
selftest contract. Its unrestricted sweep passed all 3,953 installed modules
with zero failures or timeouts in 742.4 seconds, including the deterministic
elliptic-kernel coverage that timed out in post55. Packaged pytest then passed
with 226 passes and 5 skips in 269.88 seconds. The full validator exited zero
after 1,991.206 seconds.

Both runtime summaries report zero dependency, host-executable, Python-path,
source-path, or GAP-host-path leaks. `SAGE_ROOT` was null, `PYTHONPATH` and
`LD_LIBRARY_PATH` were absent, `PYTHONNOUSERSITE=1`, and `PATH` contained only
the fresh install followed by `/usr/bin:/bin`. Every resolved Sage prefix was
inside its corresponding fresh install.

The exact post56 primary and closure are accepted locally for macOS arm64
CPython 3.12. The public preview remains the unchanged post9 set; nothing was
published. Durable wheel, checksum, inventory, build-resume, short-gate, and
full-gate evidence is retained at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260717-080007-288c3f21968/
```

The disposable build/source trees and both completed validation environments
were removed after evidence capture, restoring 104 GiB free on `/Volumes/sage`.

## 2026-07-17 Post55 Full Rejection And Post56 Deterministic Doctest

Exact pushed `10.9.post55` source
`94480894829dfe517401120c63e8af9e1d5fe84c` has tree
`ad3a88eeb78b82a542d7fd05607867e899bf95ba`. Its 144,055,983-byte source
archive has SHA256
`cd9edb35606882bf7d92952ce5363f7c7750590c33560fa30072b0694ac83de8`.
The native Darwin arm64 CPython 3.12 build and repair passed and produced:

```text
sagelite-10.9.post55-cp312-cp312-macosx_26_0_arm64.whl
  102,265,036 bytes
  932d038a86563b873e338b56b328a92018d645fbee0f77aed02d22a50390aec5
```

Repair injected 2,079 native headers, rewrote 23 companion dependencies in
16 Mach-O files, and audited 1,176 dependencies across 637 Mach-O files. The
strict compatible closure contains 180 wheels: one primary, 68 companions,
and 111 third-party wheels totaling 13,896,965,238 bytes. Its inventory
digest is
`d4fe25eb64249dddcf0fc36620553e423c00440c98eef7b51881694cf6206855`.

The independent fresh short gate passed strict preflight, binary-only
installation, `pip check`, runtime isolation, every selftest, all 3,953
installed standard modules with zero failures in 481.3 seconds, and packaged
pytest with 226 passes and 5 skips. The validator exited zero after 1,730.967
seconds. `SAGE_ROOT` was null, every resolved Sage prefix was inside the fresh
install, and the runtime manifest contained no build venv, rejected post54
run, or old source SHA.

The separate fresh full gate passed the same preflight, install, `pip check`,
runtime-manifest isolation, and selftest contract. Its unrestricted sweep
completed all other work but rejected
`sage.schemes.elliptic_curves.hom` after the module exceeded the 600-second
worker limit under seed
`183514028347342237074558759984525756750`. The reducer classified exactly one
`performance-only` timeout, zero failed examples, and 3,954 modules seen. The
validator exited 4 after 2,546.274 seconds; packaged pytest was not reached.

An isolated exact-seed replay reproduced the original random 99-step
2-isogeny path for 1,155.1 seconds without reaching an assertion. Selecting a
stable branch allowed the module to pass, but also showed that its following
random curve/isogeny search spent about 150 seconds each in extension-field
kernel construction and generation. Exact pushed `10.9.post56` source
`288c3f219682ed6ba6e7a77cb069b94ba0073c13` makes both coverage cases
deterministic while retaining the large 2-isogeny chain and an
extension-field kernel example. The complete module then passed all 497
doctests under the exact failing seed and original 600-second limit in 7.5
seconds. An exact post56 rebuild and independent strict short and full gates
are still required. All build, closure, rejection, and focused replay evidence
is retained at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260717-055907-94480894829d/
```

## 2026-07-17 Post54 Rejection And Post55 Order-Independent Doctest

The exact pushed `10.9.post54` source `4071f482bcc3865116d57391b00227ae0a9f28d4`
completed its native Darwin arm64 CPython 3.12 build. Repair injected 2,079
native headers, rewrote 23 companion dependencies in 16 Mach-O files, and
audited 1,176 dependencies across 637 Mach-O files. The repaired primary is:

```text
sagelite-10.9.post54-cp312-cp312-macosx_26_0_arm64.whl
  102,252,654 bytes
  f45f17aba5ca6f6564097bb0e4d1cf6d6df003bcabde9743e7a8da6e79be6503
```

The deterministic CPython 3.12 closure contains 180 compatible wheels: one
primary, 68 companions, and 111 third-party wheels totaling 13,896,962,399
bytes. Its inventory digest is
`f248102ba0ca21746674be08f1963b7eb086d873201de30e56abadac3feddb51`.
Closure assembly preserved two rejected orchestration attempts: the first used
a bare interpreter without `packaging`, and the second proved that the
CPython 3.13 seed lacked the CPython 3.12-only `pycryptosat` dependency. The
accepted closure uses the compatible PyPI `pycryptosat==5.14.7` macOS arm64
wheel and passed complete local pip resolution and interpreter-tag checks.

The strict neutral-path short gate passed wheel-only installation, `pip
check`, runtime-manifest isolation, every selftest, and packaged pytest with
226 passes and 5 skips. Its installed `--optional=sage` sweep covered 3,954
modules and rejected one module because `pycryptosat` returned the correct
Boolean solution with a different dictionary insertion order:

```text
Expected: [{z: 0, y: 1, x: 0}]
Got:      [{y: 1, z: 0, x: 0}]
```

The mappings compare equal and both reduce the system to zero. The `post55`
working change makes this single doctest compare dictionary equality instead
of dictionary representation. A focused replay of the complete
`multi_polynomial_sequence.py` doctest file in the rejected fresh install
passed, including the `brial` and `pycryptosat` features. A coherent exact
`post55` primary rebuild and independent strict short and full gates are still
required. The authoritative rejected run and focused evidence are retained at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260717-050335-4071f482bcc/
```

## 2026-07-17 Post54 Exact Rebuild Start

The scheduled iteration first retried the higher-priority Linux x86_64
CPython 3.14 cell. All three bounded SSH attempts to `host` timed out. No
x86_64 build or validation was started. The directly fetched public
`dev/manifest.json` remained the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, including fourteen Sagelite primary
wheels.

Independent preflight found `m1` idle and native Darwin arm64 with Homebrew
CPython 3.12, 3.13, and 3.14 available. `/Volumes/sage` had 105 GiB free,
above the 100 GiB heavy-build threshold. The Lima backend also reported Linux
aarch64 with 103,443,718,144 bytes free, but no Linux work was selected because
the next independent matrix cell is native macOS arm64 CPython 3.12.

The selected release-candidate source is exact pushed commit
`4071f482bcc3865116d57391b00227ae0a9f28d4` (`10.9.post54`). It is an
ancestor of the verified `origin/develop` head. The controller-created source
archive is 151,219,896 bytes with SHA256
`7e457b3827627b290e2b58a426f618227de12269dc19aae3689d8a7072691ba2`.
Its independently materialized tree is
`513286131f987e2cb30e3fd12956c800cfca2328`, matching the committed tree.
The full archive size and digest were verified on `m1` before launch.

The native CPython 3.12 build is running durably under tmux session
`sagelite_cp312_post54_build`, with recorded PID 26677, at:

```text
/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260717-050335-4071f482bcc/
```

The build reuses the retained automation-owned native dependency prefix from
the proven macOS build chain at
`macos-arm64-cp313-20260716-021120-d75dd63d011`, creates a fresh CPython 3.12
build venv, and applies the committed cypari, Singular, PARI, and general
macOS repair stages. Its durable evidence includes `build-command.sh`,
`command.log`, `pid`, `disk-before.txt`, and, after source verification,
`run-metadata.txt`. Completion will be recorded in `exit-code`.

This is exact-source build-start evidence only. No CPython 3.12 `post54`
wheel, compatible closure, fresh installation, `pip check`, selftest, short
gate, full-suite pass, or publication result is claimed yet.
