# Sagelite Linux aarch64 CPython 3.14 Validation

Last updated: 2026-07-15

## Current status

The second native Linux `aarch64` CPython 3.14 `post33` build failed during
native prerequisite staging. No primary wheel, wheel-only install, smoke
result, short-gate result, or full-suite result is claimed yet.

The authoritative run root is:

```text
/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260715-020454-3cb65496e5a
```

It is running in the persistent Lima guest `sagelite-linux-arm64` on `m1`.
The exact source input is pushed commit
`3cb65496e5a1175116bb44c19c5e81cbd815db94`, with Sagelite version
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

## Public preview state

The directly fetched public `dev/manifest.json` remained generated at
`2026-07-09T17:17:42.743310+00:00`, with 177 wheels and fourteen Sagelite
primary wheels from `10.9.post8` and `10.9.post9`. There is no public
`post33` primary and no Linux aarch64 CPython 3.14 primary. No publication was
attempted.
