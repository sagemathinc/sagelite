# Sagelite Linux aarch64 CPython 3.14 Validation

Last updated: 2026-07-15

## Current status

The native Linux `aarch64` CPython 3.14 build is active. No primary wheel,
wheel-only install, smoke result, short-gate result, or full-suite result is
claimed yet.

The authoritative run root is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-013434-914817f8ad8
```

It is running in the persistent Lima guest `sagelite-linux-arm64` on `m1`.
The exact source input is pushed commit
`914817f8ad8af5056af0d2f73fc3dbb1f36af596`, with Sagelite version
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

## Durable build and validation services

Exactly two user-systemd services were started:

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

## Public preview state

The directly fetched public `dev/manifest.json` remained generated at
`2026-07-09T17:17:42.743310+00:00`, with 177 wheels and fourteen Sagelite
primary wheels from `10.9.post8` and `10.9.post9`. There is no public
`post33` primary and no Linux aarch64 CPython 3.14 primary. No publication was
attempted.
