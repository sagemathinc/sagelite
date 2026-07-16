# Sagelite Linux aarch64 CPython 3.12 Validation

## 2026-07-16 Post54 Wheel And Strict Short/Full Passes

The native build from exact pushed source
`9492b6cbf83875c024ef2c6760977707ef8065f2` completed with exit code zero.
It produced 82 repaired wheels: one primary and 81 companion runtime/data
wheels, including ABI-specific `pplpy`. The native `pycosat` and `cysignals`
supplements described below brought the build wheelhouse to 84. The primary is:

```text
sagelite-10.9.post54-cp312-cp312-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   236,678,292 bytes
sha256: ae629dc301f91273aec9eeb85ebe9625ff768f1d9fa7c411be35e9cfc9eaa2be
```

The first binary-only closure attempt correctly rejected the retained CPython
3.13 `pycosat` wheel and stopped before installation because no public CPython
3.12 aarch64 wheel exists. Native manylinux builds then supplied repaired
CPython 3.12 wheels for `pycosat 0.6.6` and `cysignals 1.12.6`. The matching
`cysignals` avoids the exported-C-function mismatch already established on
CPython 3.13. The failed resolution log and exit code remain preserved as
`validation-follow-r1.log` and `validation-follow-r1-exit-code`.

The resulting deterministic strict closure has 191 wheels totaling
16,739,248,783 bytes: one primary, 81 Sagelite companions, and 109 third-party
wheels. Its staged wheelhouse digest is
`cf8bef4b02173028cd2b1c7e9db8203c4d5b81df8c395d46eb464f480cbee675`,
and its inventory-file digest is
`4c94228fe9f9da854b1d9c5d19d2fd7b163cad97dd8e2382451d0cdef5b701af`.

The strict short gate then passed in a fresh CPython 3.12 wheel-only install.
All 191 wheel filenames and tags passed strict repaired-wheelhouse preflight;
all 68 requested Sagelite dependency projects were present. Installation,
`pip check`, runtime manifest collection, and every selftest probe passed. The
explicit installed `--optional=sage --short 600` sweep saw all 3,953 modules
and reduced to zero failures in 519.2 seconds. Packaged pytest passed 229 tests
with 2 skips and 15 warnings. The validator recorded `Status: passed`, exit
code 0, and 1,246.475 seconds total elapsed time.

After removing the short gate's fresh install, the same durable validation
service ran a separate fresh strict full gate from the identical wheel
contract. Strict preflight, wheel-only installation, `pip check`, runtime
manifest collection, and every selftest probe passed again. The unrestricted
installed `--optional=sage` sweep saw all 3,953 modules and reduced to zero
failures; its doctest runner reported `All tests passed` in 883.4 seconds.
Packaged pytest then passed 229 tests with 2 skips and 15 warnings in 306.60
seconds. The full validator recorded `Status: passed`, exit code 0, and
1,630.778 seconds total elapsed time.

The durable service completed successfully as:

```text
sagelite-post54-cp312-validate-r2.service
```

This is repaired-wheel, compatible-closure, independent fresh-install short
and full evidence. Both validation and follow-up exit-code files contain zero.
The cell is accepted as `full`. The completed full gate's disposable 21 GiB
install tree was removed after preserving the wheelhouses and validation
evidence, restoring 103,526,285,312 bytes free in the guest. No publication
was attempted.

## 2026-07-16 Post54 Native Build Start

The scheduled matrix iteration first retried the higher-priority Linux
`x86_64` CPython 3.14 cell. The required `host` SSH alias again timed out
during connection, so no x86_64 build or validation was started. The public
`dev/manifest.json` remained the 177-wheel set generated on 2026-07-09, with
fourteen public Sagelite primaries split between `10.9.post8` and
`10.9.post9`.

The independent Linux aarch64 CPython 3.12 cell then passed native backend
preflight on `m1`. The outer host reported Darwin `arm64`, and the persistent
Lima guest reported Linux `aarch64` with Docker running as `arm64`. No
Sagelite build, validator, or user service was active.

The outer filesystem initially had 59 GiB free and the guest had less than
100 GiB free. Cleanup removed only completed fresh-install venvs and
disposable build/source/cache content from accepted macOS runs, plus source,
venv, and wheelhouse content from superseded resolved-failure runs. It
retained the accepted macOS CPython 3.13 and 3.14 wheelhouses, their concise
short/full evidence, and the accepted Linux aarch64 CPython 3.13 and 3.14
wheelhouses and evidence. After cleanup and source staging, the outer volume
had 117,415,904 KiB free and the Linux guest had 110,081,482,752 bytes free,
both above the 100 GiB heavy-build threshold.

The exact pushed source is:

```text
source SHA: 9492b6cbf83875c024ef2c6760977707ef8065f2
version:    10.9.post54
bundle:     sagelite-shallow-9492b6cbf83.bundle
size:       145,745,628 bytes
sha256:     2c3d130ea8b058c6cd706e5c17523be666f724427bcaf397c9bce0f370647537
```

The bundle hash matched on the controller, outer Mac, and Linux guest. The
native build uses the repository CIBW helpers with
`CIBW_BUILD=cp312-manylinux_aarch64`, `CIBW_ARCHS=aarch64`, and the CPython
3.12 manylinux interpreter. Its durable run root is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260716-221205-9492b6cbf83
```

The build and gated watcher are active as:

```text
sagelite-post54-cp312-build.service
sagelite-post54-cp312-validate.service
```

The watcher waits for the build's durable `exit-code`. After build success it
will assemble a CPython 3.12-compatible closure from the new repaired wheels,
accepted ABI-independent aarch64 companions, and binary-only third-party
wheels. It will then run strict fresh wheel-only short and full validations
with `sagelite[all-needed-extras]==10.9.post54` and explicit
`--optional sage`.

This checkpoint is preflight, cleanup, exact-source transfer, and build-start
evidence only. No `post54` wheel, install, smoke, short, or full result is
claimed, and no publication was attempted.
