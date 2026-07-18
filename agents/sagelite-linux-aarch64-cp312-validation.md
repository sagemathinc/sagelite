# Sagelite Linux aarch64 CPython 3.12 Validation

## 2026-07-18 Post60 Wheel And Strict Short/Full Passes

All three bounded attempts to reconcile the higher-priority Linux `x86_64`
CPython 3.12 job through the required `host` alias timed out during SSH
connection. That possibly surviving job was left untouched. The public
`dev/manifest.json` remained the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primary wheels, so
no local `post60` artifact was assumed public.

The native Linux arm64 build and watcher described below completed from exact
pushed source `22a2cb56739940d7a9eb313e997fd0a004a9ea36`
(`10.9.post60`). The clean native `aarch64` build exited zero and produced 82
repaired primary and companion wheels totaling 4,623,974,563 bytes. The
primary is:

```text
sagelite-10.9.post60-cp312-cp312-manylinux_2_27_aarch64.manylinux_2_28_aarch64.whl
size:   236,678,592 bytes
sha256: 95ab03ac02865369c08ce3b6b2acb00f5cc54189404084ce4518f65ab7bcfd3b
```

The build-wheel inventory SHA256 is
`13bf345e42a91fa19c6452dc342eef0266202abf3a44bfd0362a569e6107a370`.
The watcher combined the new exact-build wheels with accepted ABI-specific
supplements and portable companions, then resolved a deterministic strict
191-wheel closure totaling 16,739,251,241 bytes. Its inventory SHA256 is
`e0bf111356e5848111a6b24d8b4f320dd62ea9d3411b2a4b6d664c4b425f6592`.

The independent fresh short gate passed strict repaired-wheelhouse preflight,
binary-only `sagelite[all-needed-extras]==10.9.post60` installation,
`python -m pip check`, runtime-manifest isolation, every selftest, all 3,953
installed `--optional=sage --short 600` modules with zero failures, and
packaged pytest with 229 passes, 2 skips, and 15 warnings. The doctest sweep
took 519.2 seconds, pytest took 295.89 seconds, and the validator exited zero
after 1,266.143 seconds. Its reduced-analysis JSON reports 3,953 modules seen,
zero failed modules, and no actionable buckets.

The separately named full gate created a second fresh install from the same
strict closure. Preflight, wheel-only installation, `pip check`, runtime
isolation, and every selftest passed again. The unrestricted installed
`--optional=sage` sweep reported `All tests passed` for all 3,953 modules in
888.6 seconds. Packaged pytest then passed 229 tests with 2 skips and 15
warnings in 298.02 seconds. The validator exited zero after 1,617.91 seconds,
and the independent reducer again reported 3,953 modules seen and zero failed
modules. The durable build, short, full, and watcher exit-code files all
contain zero.

Authoritative artifacts are retained at:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260717-223804-22a2cb56739
```

Deliberate cleanup retained the exact strict closure, build inventory,
validation summaries, runtime manifests, selftest logs, reduced analyses, and
top-level command logs. It removed only completed install homes and build
venvs, inactive pushed-source checkouts, one resolved superseded closure, two
obsolete pre-post60 bundles, and the unused 2025 manylinux image. Final guest
capacity is 107,698,089,984 bytes free, above the binary 100 GiB heavy-build
threshold. No artifact was published.

## 2026-07-17 Post60 Synchronized Build Start

Three bounded attempts to reconcile the higher-priority Linux `x86_64`
CPython 3.12 job through the required `host` alias timed out during SSH
connection. That possibly surviving job was left untouched. The public
`dev/manifest.json` remained the 177-wheel set generated on 2026-07-09, so no
local `post60` artifact was assumed public.

Independent preflight on `m1` found the outer Darwin host native `arm64`, the
persistent Lima guest running Linux `aarch64`, and no active Sagelite build,
validator, or Docker container. The outer `/Volumes/sage` filesystem had
108,004,188,160 bytes free. The guest initially had 103,446,056,960 bytes
free, below the binary 100 GiB heavy-build threshold. Precise cleanup removed
only superseded regenerated closure links, eight inactive disposable source
checkouts, and six obsolete exact-source bundle inputs. Accepted wheelhouses,
validation evidence, logs, and the latest useful failure evidence remain.
This restored 108,706,050,048 bytes free in the guest before source staging.

Exact pushed release-candidate source is:

```text
source SHA: 22a2cb56739940d7a9eb313e997fd0a004a9ea36
version:    10.9.post60
bundle:     sagelite-shallow-22a2cb56739.bundle
size:       145,770,108 bytes
sha256:     84f2902d2051d598b04430d9ef95b4e9fe672f4d02a0701a653d2764b82285dc
```

The hash matched on the controller, outer Mac, and Linux guest. The new native
run is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260717-223804-22a2cb56739
```

Its clean checkout was independently confirmed at the exact source SHA and
`10.9.post60`. The pre-launch guest capacity was 108,560,244,736 bytes. The
build uses the repository Linux CIBW helpers with
`CIBW_BUILD=cp312-manylinux_aarch64`, `CIBW_ARCHS=aarch64`, and the accepted
CPython 3.12 closure as the guarded source of ABI-specific supplements and
portable wheels. This leg emits a synchronized platform companion set before
the watcher resolves a fresh strict closure and runs independent short and
full gates.

The durable services are active as:

```text
sagelite-post60-arm-cp312-build.service  main PID 432512
sagelite-post60-arm-cp312-watch.service  main PID 432520
```

Script hashes are:

```text
d9f70b4345cc933a5f86a8d95b2ce0f5f5c98a24ea61d93d27baac2fead48e86  start-build.sh
57805b8cd47d58ca7b20de0403c97bab5660df33646fc730d26d4f5c9b3f80b9  validate-after-build.sh
1ecd09f1175f8f626fa23678ec70bc16ed2d210eec280bd5bd7a4fdcc66a7a15  watch-and-validate.sh
```

The build completed exact-bundle checkout and entered native prerequisite
setup while the watcher remained active. No `post60` wheel, install, short
gate, full gate, or publication result is claimed yet.

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
