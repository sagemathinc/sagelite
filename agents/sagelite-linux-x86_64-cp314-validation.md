# Sagelite Linux x86_64 CPython 3.14 Validation

## 2026-07-15 Preflight Blocker

The scheduled matrix iteration selected Linux `x86_64` with CPython 3.14, the
next cell in the authoritative work order. The canonical repository was clean
at source commit `cef925c228a6803f37c8ca68ed92d516bb8c94b5` on `develop`, with
`origin/develop` at the same commit.

The public `dev/manifest.json` still reported 177 wheels generated on
2026-07-09 and the public Sagelite project page still listed fourteen primary
wheels: seven each for `10.9.post8` and `10.9.post9`. No newer local aarch64
primary was assumed to be public.

Read-only preflight through the required `host` SSH alias found:

- the environment reported Linux `x86_64`;
- the expected `/mnt/cocalc-scratch` filesystem was not mounted;
- `/mnt/cocalc` had 64 GiB free and `/` had 17 GiB free;
- no automation-owned Sagelite build or validation process, PID, exit-code,
  validation summary, or run metadata was present;
- Podman 4.9.3 was available, but Docker and host `python3.14` were not.

The 64 GiB filesystem is above the 30 GiB test-only threshold but below the
runbook's non-negotiable 100 GiB threshold for a heavy build. It is also a
different mount from the assigned automation root. Safe cleanup cannot repair
the capacity shortfall: the filesystem was only 13% used and its total size
was 75 GiB.

No build, validation, or public publication was started. Re-running the public
`10.9.post9` CPython 3.14 wheel would not validate the current committed source
and would predate failure fixes already proved in the aarch64 work. The cell
therefore remains `smoke only`. Resume by restoring the expected bulk volume
on `host` (with at least 100 GiB free), then preflight again and build the exact
current committed revision using the repository CIBW contract.

## 2026-07-17 Post56 Release-Candidate Build Start

The next scheduled iteration found `host` reachable on its first bounded SSH
attempt. The assigned environment reported Linux `x86_64`, Docker 29.1.3,
and the expected `/mnt/cocalc-scratch` mount. Docker's data root is on that
bulk filesystem. No Sagelite build, cibuildwheel process, validator, installed
doctest process, or live automation PID was active.

The bulk filesystem initially had 96,531,124,224 bytes free, below the
runbook's 100 GiB heavy-build threshold. Two exact, superseded automation
validation trees for `post6` and `post7` occupied about 32.8 GB. They had
no live processes and were superseded by the retained `post8` validation
tree and public artifacts. Their container-created ownership required the
host's available non-interactive `sudo`; removing only those two paths raised
free space to 129,343,483,904 bytes. The removal is irreversible.

Exact pushed source `288c3f219682ed6ba6e7a77cb069b94ba0073c13`
(`10.9.post56`) was fetched as a depth-one detached checkout from the
canonical controller repository. The controller and `origin/develop` were
synchronized at `877ff231622eedd37a266d4a51922d2824015f8e`; the only
changes between the selected source and that tip were matrix evidence
documents. The remote checkout passed exact-SHA, clean-status, version, Linux,
and `x86_64` guards before launch.

The first durable launch was preserved at:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-095227-288c3f21968
sagelite-post56-x86-cp314-build.service
```

It passed host bootstrap but exited one before compilation or wheel creation.
cibuildwheel mounted the host root read-only at `/host`, so the before-all
hook could resolve but not write the retained
`/host/sage-manylinux_2_28_x86_64` prefix. A focused manylinux probe proved
that over-mounting `/mnt/cocalc-scratch` read/write beneath the read-only
`/host` hierarchy permits both persistent-prefix and run-directory writes.

A fresh exact-SHA replacement is running at:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-095911-288c3f21968
sagelite-post56-x86-cp314-build-r1.service
main PID 48200
```

It uses cibuildwheel 3.4.1 with `CIBW_BUILD=cp314-manylinux_x86_64`,
`CIBW_ARCHS=x86_64`, the repository's current before-all, before-build,
repair, and build-wheel helpers, the bulk-backed persistent manylinux prefix,
and one explicit read/write bind of the assigned bulk filesystem beneath
`/host`. Its pip, cibuildwheel, temporary, venv, source, output, and log
paths are all below the assigned bulk filesystem. The replacement passed the
previously failing prefix-write phase; an actual
`manylinux_2_28_x86_64` container was installing native prerequisites with
124,854,374,400 bytes free at the latest health check.

The public `dev/manifest.json` remains the 177-wheel set generated at
`2026-07-09T17:17:42.743310+00:00`, with fourteen Sagelite primaries from
`post8` and `post9`. No `post56` x86_64 wheel, install, smoke, short, or
full result is claimed yet, and no publication was attempted. A resumed
iteration must reconcile the replacement service, its PID, log growth,
`exit-code`, and wheel inventory before launching any other x86_64 build.

## Post56 Prefix-Mount Failures And Post57 Correction

The first replacement above subsequently exited before compilation.
CPython 3.14's venv implementation rejected the writable retained prefix
because `/host/sage-manylinux_2_28_x86_64` still appeared as a symlink.
An exact child Docker bind did not hide that symlink. A reversible focused
probe temporarily replaced only the host's generic prefix symlink with a bind
mount of its unchanged bulk-backed target. Inside the CPython 3.14 manylinux
image the path then reported `exists=True`, `isdir=True`, and
`islink=False`, and a write probe passed. The original host symlink was
restored immediately.

A fresh exact-`post56` retry at
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-100334-288c3f21968`
used that reversible mount with an exit trap. It cleared venv creation and
restored the original symlink correctly on exit, but exposed a separate cache
initialization defect. The retained prefix had no `bin/python3`, so the
before-all hook skipped both venv initialization and Python-module cache
validation. The stale `python_build-1.4.2` marker survived, after which
cysignals and NumPy both failed with `No module named build`. This run also
exited one before wheel creation.

Exact pushed source `6361dc1935cda24f0c080a6f0f55a5ff29fc23b2`
fixes that missing-interpreter branch by initializing the selected-ABI Sage
venv before cached module markers are validated. It bumps the immutable wheel
version to `10.9.post57`. Shell syntax and all four focused Linux before-all
contract tests pass. The complete companion-metadata test file passed 260
tests and had three unrelated existing failures involving stale generated
Flatter metadata and Regina dependency expectations.

The fresh authoritative replacement is running at:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-101057-6361dc1935c
sagelite-post57-x86-cp314-build.service
main PID 102398
```

Before launch, only the generic retained prefix's Python venv symlinks and
`python3_venv` marker were removed to reproduce the exact defect; the stale
`python_build-1.4.2` marker was deliberately retained. The live log proves
that `post57` selected the new `Initializing missing Sage venv interpreter`
branch, removed the stale `python_build`, cysignals, and NumPy markers, and
then installed `python_build 1.4.2` successfully. The native x86_64
manylinux build remains active with no exit artifact and 122,928,590,848
bytes free at the latest checkpoint.

No `post57` wheel, install, smoke, short, or full result is claimed yet, and
no artifact was published. The public manifest remains the 177-wheel set
generated on 2026-07-09. A resumed iteration must reconcile this exact
`post57` service before launching another x86_64 build.
