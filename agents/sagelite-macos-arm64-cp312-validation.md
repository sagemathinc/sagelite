# Sagelite macOS arm64 CPython 3.12 Validation

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
