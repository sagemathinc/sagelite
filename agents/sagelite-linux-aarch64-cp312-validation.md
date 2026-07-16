# Sagelite Linux aarch64 CPython 3.12 Validation

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
