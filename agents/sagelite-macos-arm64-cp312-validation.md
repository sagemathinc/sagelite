# Sagelite macOS arm64 CPython 3.12 Validation

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
