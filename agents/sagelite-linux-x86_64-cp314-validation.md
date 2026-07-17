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

## Post57 Primary And Synchronized Companion Builds

The exact CPython 3.14 build above completed with exit code zero. Its restored
host prefix is again the original symlink to the retained bulk-backed prefix.
The repaired primary is:

```text
sagelite-10.9.post57-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
size:   244935135
sha256: 9f806bab9af28243e8437ef6b39d13188f3407f3f917e39ab1ffbd1e34b19b53
```

That ABI build also produced repaired CPython 3.14 `pplpy` and
ABI-independent Maxima and QEPCAD wheels. Every filename in its four-wheel
output passed the generated SHA256 inventory. No install or test result is
inferred from the successful build.

The Linux repair contract intentionally emits the complete platform companion
set only from its CPython 3.12 leg. Exact source
`6361dc1935cda24f0c080a6f0f55a5ff29fc23b2` therefore ran a separate cached
CPython 3.12 build at:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp312-companions-20260717-105534-6361dc1935c
```

It completed with exit code zero and produced 82 repaired wheels totaling
4,654,304,280 bytes: one CPython 3.12 primary, one CPython 3.12 `pplpy`, and
80 platform runtime/data companions. Its complete `SHA256SUMS` inventory
passed. This synchronized set includes the current required Flatter `post1`,
Graphviz `post4`, GIAC `post1`, ImageMagick `post3`, lrslib `post2`, Meataxe
`post1`, msolve `post2`, Singular `post2`, Sympow `post2`, and Tachyon `post1`
companions. The build restored the retained prefix symlink on exit and left
118,918,078,464 bytes free.

Maxima `post15` and QEPCAD `post4` were emitted by both ABI builds with the
same filenames but different bytes. The strict CPython 3.14 closure therefore
uses the complete CPython 3.12 platform companion set and only the primary and
`pplpy` wheels from the CPython 3.14 build; it never exposes both byte variants
to pip. A marker-aware inventory comparison found exactly one companion absent
from the new 82-wheel output: the policy-gated, platform-independent
`sagelite-database-polytopes-4d==10.9` wheel.

The previously accepted portable 4D database wheel is being transferred from
`m1` to the CPython 3.14 ABI input. Its expected identity is:

```text
sagelite_database_polytopes_4d-10.9-py3-none-any.whl
size:   9100370523
sha256: e22d60ebd324d848871f0980a7e48226396b5ed5ebecab23f8e1b5482b6438f2
```

The durable controller transfer is owned by tmux session
`sagelite-polytopes4d-transfer`; its PID, command log, timestamps, and eventual
exit code are under:

```text
/scratch/sagelite-automation/polytopes4d-transfer-20260717
```

Its destination is
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-101057-6361dc1935c/cp314-abi-input/`.

The resumed iteration found both of that transfer's SFTP endpoints and its
controller process alive. At `2026-07-17T12:39:14Z`, the destination had grown
to 2,969,457,664 bytes; the latest capacity check found 115,927,535,616 bytes
free on `host`. A direct
64 MiB transfer probe from `m1` was no faster, so the intact durable transfer
was retained. The exact probe files were removed afterward.

The guarded validation launcher is staged as `validate-post57.sh` in the run
root with SHA256
`f544391e8c47041797dbedd52f697de1b299cb174e9cbd8ba33b2adf4d12dd9d`.
Controller tmux session `sagelite-post57-x86-cp314-watch` waits for a successful
transfer exit artifact, then launches exactly one host system service named
`sagelite-post57-x86-cp314-validate.service`. Before changing the failed
staging closure, the launcher requires Linux `x86_64`, both successful build
exit artifacts, exact source `6361dc1935c`, the 82-wheel companion inventory,
and the expected portable-wheel SHA256. It then resolves the binary-only
closure and runs independent fresh strict short and full gates. The watcher
metadata is at
`/scratch/sagelite-automation/post57-x86-cp314-validation-watch-20260717`.

No install, smoke, short, full, or publication result is claimed. The directly
inspected public manifest remains the 177-wheel set generated on 2026-07-09.
