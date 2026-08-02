# Sagelite Linux x86_64 CPython 3.14 Validation

## 2026-08-01 Exact Post64 Portable Rebuild Accepted

The final Linux x86_64 cell completed successfully from exact pushed source
`014ae4bf44318b6f5032053957a92291d4363b7a` (`10.9.post64`). The build
produced:

```text
sagelite-10.9.post64-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
size:   261850177 bytes
sha256: 46c5ec1dfc80b65fc6968f942164d8adf2f9f81ee6dc8849b76c6c98b6b43b4f
```

The strict closure contains 180 wheels totaling 14,360,482,199 bytes, with
wheelhouse SHA256
`0275a2813da7153b918b530a8087b8241d779e0c6de38924c86c3b3b998fed5b`.
The corrected QEMU Nehalem probe passed with BMI2 and ADX absent
(`leaf7_ebx=0x0`).

Independent fresh short and full gates passed strict preflight, binary-only
`sagelite[all-needed-extras]==10.9.post64` installation, `pip check`, runtime
isolation with zero leaks, all 102 selftests, all 3,953 installed
`--optional=sage` modules with zero failures, and packaged pytest with 229
passes and 2 skips. The unrestricted sweep took 925.4 seconds, packaged
pytest took 432.47 seconds, and the full validator exited zero after
1,933.391 seconds at `2026-08-01T22:40:31Z`. The build, old-CPU, short, full,
and watcher exit artifacts all contain zero.

Linux x86_64 CPython 3.14 is therefore the ninth synchronized full-pass cell
from the selected `post64` release-candidate revision. The authoritative run
and its retained wheelhouse and validation evidence are:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260730-014100-014ae4bf443
```

Nothing had been published when this local acceptance was recorded.

## 2026-08-01 Exact Post64 Portable Rebuild Started

After Linux x86_64 CPython 3.13 became the eighth synchronized full-pass
cell, its completed install environments were removed while all concise
evidence and wheel artifacts were retained. The already staged final matrix
run is:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260730-014100-014ae4bf443
```

Its checkout is clean at exact pushed source
`014ae4bf44318b6f5032053957a92291d4363b7a` (`10.9.post64`), the source
archive and all four launcher hashes passed, Docker was idle, the persistent
fat-binary prefix was intact, and the assigned filesystem had
153,127,497,728 bytes free. The durable build and guarded watcher started at
`2026-08-01T21:06:50Z` under:

```text
sagelite-post64-x86-cp314-build-r1.service
sagelite-post64-x86-cp314-watch-r1.service
```

The watcher pins the previously accepted CPython 3.14 x86_64 `pycosat`
wheel and portable 4D polytope database by SHA256, then requires a corrected
fresh QEMU Nehalem probe and independent short and full gates. No post64
CPython 3.14 wheel or validation pass is claimed yet, and nothing has been
published.

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

## Post57 Strict Short-Gate Rejection And Post58 Fix

The durable 9,100,370,523-byte 4D polytope database transfer completed at
`2026-07-17T13:31:43Z` with exit code zero.  The destination SHA256 matched
`e22d60ebd324d848871f0980a7e48226396b5ed5ebecab23f8e1b5482b6438f2`.
The guarded watcher then launched exactly one host system service,
`sagelite-post57-x86-cp314-validate.service`, and exited zero.

The deterministic strict closure contained 181 compatible wheels totaling
14,288,021,185 bytes: one exact `post57` primary, 81 Sagelite companions, and
99 third-party wheels.  Strict preflight reported no invalid filenames,
missing requested dependencies, duplicate primaries, or tag mismatches.  A
fresh binary-only `sagelite[all-needed-extras]==10.9.post57` installation and
`pip check` passed.  Runtime manifest collection, runtime isolation, and all
selftests also completed, and packaged pytest passed with 229 tests and 2
skips.

The 600-second installed `--optional=sage` short sweep was rejected after one
of the 3,954 seen modules failed.  In `sage.misc.cython`, a successful C++
compile emitted 119 copies of Zig 0.16's bundled libc++
`-Wnullability-completeness` warning.  Parallel compiler output fused a Zig
source excerpt with a pathless warning location, so the existing narrow
filter conservatively retained the 4,464,649-byte stderr stream.  The reducer
reported exactly one failed module and one failed example.  The short
validator and follow-on service exited one; the full gate was correctly not
started.  Durable evidence is below:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-101057-6361dc1935c/validation/short-post57/
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-101057-6361dc1935c/validation-short-command.log
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-101057-6361dc1935c/validation-short-exit-code
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-101057-6361dc1935c/validation-follow-exit-code
```

The `post58` working change suppresses a pathless warning spliced into a
compiler source excerpt only when a nearby full Zig libc++ diagnostic repeats
the same line and column.  Ordinary non-Zig diagnostics, other warning
categories, compiler errors, and uncorroborated excerpts remain visible.  The
exact helper passed seven focused positive and negative cases, and applying it
to the preserved 4,464,649-byte stderr reduced the output to exactly zero.
Python compilation and `git diff --check` pass.  A fresh exact-source `post58`
primary rebuild and both independent strict gates are required; no `post57`
install, smoke, short, or full pass is claimed.

The repair commit `8bbd27d5134eb708e43222beafdf7a1126fec929` was pushed to
`origin/develop` and verified there.  Removing only the rejected gate's
inactive 21 GB install venv retained all nine validation artifacts and restored
108,724,629,504 bytes free on the assigned bulk filesystem.  The fresh exact
`post58` CPython 3.14 build is running under
`sagelite-post58-x86-cp314-build.service` at:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-140439-8bbd27d5134
```

The detached checkout is clean at the exact repair SHA, reports
`10.9.post58`, and passed Linux, `x86_64`, free-space, idle-Docker, and prefix
guards before launch.  The live native manylinux build entered the cached
CPython 3.14 environment setup with 107,703,951,360 bytes free at the latest
checkpoint.  No `post58` wheel or validation result is claimed yet.

## Post58 Full-Gate Rejection And Post59 Correction

The exact `post58` build completed with exit code zero and produced this
repaired primary:

```text
sagelite-10.9.post58-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
size:   244935373
sha256: 101544fef2dbd3b1b3ff35ca9013bb4196ebfd0283d1ac80540004a33e84c02d
```

Its strict 181-wheel closure totals 14,288,021,423 bytes and has aggregate
SHA256 `6119debfc64c078083986a110b45e6c7821d3dc633a8d3e5cfe22f5216a312b5`.
The fresh short gate passed strict preflight, binary-only installation,
`pip check`, runtime isolation, every selftest, all 3,953 standard modules
with zero failures, and packaged pytest with 229 passes and 2 skips.  The
validator exited zero after 1,570.383 seconds.

The separate fresh full gate passed installation, isolation, selftest, and
packaged pytest with 229 passes and 2 skips, but rejected one of 3,954 seen
modules.  `sage.misc.cython` again received only Zig libc++
`-Wnullability-completeness` output, this time with character-level parallel
interleaving that split `_type:3199:84: warning:` from intact libc++
diagnostics at the same location by thousands of lines.  The `post58`
eight-line corroboration window therefore preserved the 4,458,206-byte
compiler stream.  The reducer reported one failed module and one failed
example; the full validator exited one after 1,945.082 seconds.  No full pass
is claimed.

The `post59` working correction collects exact line-and-column locations from
complete Zig libc++ diagnostics across the same compiler stream.  It
suppresses a pathless interleaved fragment only when one of those full
diagnostics corroborates the location; errors, other warning categories,
complete non-Zig diagnostics, and uncorroborated fragments remain visible.
All focused positive and negative cases pass, including corroboration by a
libc++ `note:`, and the exact preserved 4,458,206-byte stream reduces to zero.
Python compilation and `git diff --check` pass.  An exact committed `post59`
rebuild and independent fresh short and full gates are required.

## Post59 Build And Validation Watcher Start

The focused repair commit `48f88027b3946287f171fb781a37ed9cbcbd86d9` was
pushed to `origin/develop` and verified there.  The public manifest remains the
177-wheel set generated on 2026-07-09.  Exact clean `post59` source is now
building natively for Linux `x86_64` CPython 3.14 under
`sagelite-post59-x86-cp314-build.service` at:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-160733-48f88027b39
```

The run passed source SHA, clean checkout, version, architecture, idle-Docker,
persistent-prefix, and free-space guards.  Its recorded pre-build capacity was
107,379,126,272 bytes, just above the 100 GiB heavy-build threshold.  The live
manylinux container completed raw primary compilation and entered wheel repair
while the service remained active with no exit artifact at the latest
checkpoint.

A separate durable watcher,
`sagelite-post59-x86-cp314-watch.service`, will accept only a successful exact
build, assemble the strict closure from the synchronized companion set and
four exact CPython 3.14 ABI inputs, then run independent fresh short and full
gates.  It records distinct exit artifacts and skips the full gate if the
short gate fails.  No `post59` wheel, install, short, or full result is claimed
yet, and no publication was attempted.

## Post59 Short Pass, Full Rejection, And Post60 Correction

The exact `post59` build completed with exit code zero and produced this
repaired primary:

```text
sagelite-10.9.post59-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
size:   244935382
sha256: f1aa27bb993bcbae3340409c9152c44196cef7c70a126738d042ce56cb2e785d
```

Its strict closure contains 181 wheels totaling 14,288,021,432 bytes. The
fresh short gate passed strict preflight, binary-only
`sagelite[all-needed-extras]==10.9.post59` installation, `pip check`, runtime
isolation, every selftest, all 3,953 installed standard modules with zero
failures, and packaged pytest with 229 passes and 2 skips. The installed
doctest validator exited zero after 1,433.526 seconds; the module sweep itself
took 564.0 seconds.

The independent fresh full gate passed the same preflight, installation,
`pip check`, isolation, and selftest contract. The unrestricted sweep took
923.1 seconds and confirmed that the `post59` Zig diagnostic correction fixed
`sage.misc.cython`. It rejected one of 3,954 seen modules, however:
`sage.schemes.elliptic_curves.ell_finite_field` had four failed examples under
random seed `166469527479524600599751122278591708351`. Packaged pytest still
passed with 229 tests and 2 skips. The reduced analysis reports one failed
core-supported module and four failed examples, so the full validator and
guarded follow-on service exited one. Durable evidence is below:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-160733-48f88027b39/validation/short-post59/
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-160733-48f88027b39/validation/full-post59/
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-160733-48f88027b39/validation-short-command.log
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-160733-48f88027b39/validation-full-command.log
```

The reducer-provided exact-seed module replay reproduced all four failures in
13.5 seconds. The primary exception occurred for `p=263`, extension degree 8,
and composite `q=12`: the direct kernel-polynomial constructor correctly
reported that no cyclic normalized degree-12 isogeny linked the selected
curves. The remaining examples then reused stale doctest variables and were
cascading failures. An exhaustive diagnostic over all 38 conductor-valid
values below `p/4` found this direct-constructor failure only for `q=12`; the
function's existing composite-isogeny enumeration successfully constructed a
degree-12 trace-zero endomorphism for that exact case.

The `post60` working correction lets this `ValueError` select the existing
enumerative fallback and adds a deterministic `p=263`, `q=12` regression
example. A source-file overlay on the unchanged rejected wheel install is
focused evidence only, not acceptance. Under the exact failing seed it passed
all 548 module doctests in 8.4 seconds. The overlay source and durable focused
log are at:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-post60-focused-20260717-ell-composite/
```

The source SHA256 is
`3875400d6269e418b9aab826b6fedc9edd21bfca5041fcb157f4d1704c841c2d`;
the log SHA256 is
`f0d48f5436016f601ad1f8298b4b944284c5e1031142dcbf05a7c47bd7ed6810`.
Python compilation and `git diff --check` pass. A committed exact `post60`
wheel rebuild and both independent fresh strict gates are required; no
`post59` full pass is claimed.

## Post60 Exact Build Start

The focused repair commit
`22a2cb56739940d7a9eb313e997fd0a004a9ea36` was pushed to
`origin/develop` and verified there. Targeted cleanup removed only the two
completed `post59` install venvs and homes plus three superseded failed
`post56` run trees whose failure evidence is already recorded above. The
`post59` wheelhouse and all validation evidence remain. This restored
108,025,143,296 bytes free; the exact clean `post60` checkout left
107,563,696,128 bytes free at launch, above the 100 GiB heavy-build threshold.

The native Linux `x86_64` CPython 3.14 build is running under
`sagelite-post60-x86-cp314-build.service` at:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-175700-22a2cb56739
```

The run passed exact-source, clean-checkout, version, architecture,
idle-Docker, persistent-prefix, and pre-launch capacity guards. Its live
manylinux container entered cached native prerequisite setup. The durable
build, watcher, and validation scripts have SHA256 values
`5c1a00f796d41f972b3f0c4be86b370e41f097f64b57898d39ec3404d4a7462f`,
`b759a477d1932b0b4f0c56c31c0c561e62e42f1dc5c25fc4e86e08dcc9111ef2`,
and `17d8df1f44ea681ed4a78b42b4aef6ff0a5a24feec495a624141df7cfcd27edb`,
respectively.

One separate guarded watcher,
`sagelite-post60-x86-cp314-watch.service`, is active. It will accept only a
successful exact build, assemble the strict closure from the synchronized
companion set and four exact CPython 3.14 ABI inputs, and run independent
fresh short and full gates. No `post60` wheel or validation result is claimed
yet, and no artifact was published.

## Post60 Full Acceptance

The exact build and guarded watcher completed with exit code zero. The repaired
primary is:

```text
sagelite-10.9.post60-cp314-cp314-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl
size:   244935492
sha256: 20c994068d744e08a0fd9c6c4196839517721a7b530a3f89e1caa47a473c96bb
```

The deterministic strict closure contains 181 compatible wheels totaling
14,288,021,542 bytes: one exact primary, 81 Sagelite companion wheels, and 99
third-party wheels. Its complete `SHA256SUMS` file contains 181 entries and has
SHA256 `c87afd33ef0c100ba2b5df6baa61bc58f5863a196f6d9344db9c0c5c085f88b4`.
The authoritative run and durable evidence are at:

```text
/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-175700-22a2cb56739
```

The independent fresh short gate passed strict repaired-wheelhouse preflight,
binary-only `sagelite[all-needed-extras]==10.9.post60` installation,
`pip check`, runtime isolation, every selftest, all 3,953 installed
`--optional=sage` modules with zero failures, and packaged pytest with 229
passes and 2 skips. Its validator exited zero after 1,587.481 seconds.

The separately named fresh full gate passed the same preflight, installation,
`pip check`, runtime-isolation, and selftest contract. The unrestricted sweep
tested all 3,953 installed standard modules with eight threads and reported
zero failures in 914.9 seconds. Packaged pytest again passed with 229 tests and
2 skips. The reduced analysis has no actionable buckets, failed modules,
failed examples, framework errors, or timeouts, and the full validator exited
zero after 1,928.526 seconds. Build, short, full, and watcher exit artifacts
are all zero.

Exact pushed source `22a2cb56739940d7a9eb313e997fd0a004a9ea36` is therefore
accepted locally for Linux x86_64 CPython 3.14. The two completed validation
venvs and their disposable homes were removed after preserving the strict
wheelhouse and validation artifacts, restoring 106,631,876,608 bytes free on
`/mnt/cocalc-scratch`. The public R2 manifest remains the 177-wheel set
generated on 2026-07-09, and no artifact was published.
