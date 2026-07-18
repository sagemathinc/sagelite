# Sagelite Matrix Automation Loop

Last reviewed: 2026-07-18

This is the authoritative operating runbook for an automated Codex loop that
advances Sagelite toward a complete wheel and standard-test matrix. Read this
file at the start of every loop iteration and after every resumed or recovered
session. Update its matrix checkpoint when evidence changes, but keep detailed
logs in scratch storage rather than turning this file into a turn-by-turn
diary.

The user-defined target is:

> Make Sage and a useful set of open-source optional packages pip installable
> on Linux x86_64, Linux aarch64, and macOS arm64 with CPython 3.12, 3.13, and
> 3.14, and make the full standard non-optional installed Sage test suite pass.

Optional packages are useful and should be expanded, but optional-package
tests are not a release blocker. Do not let optional work delay completion of
the standard 3-by-3 matrix.

## Non-Negotiable Scope

For each of the nine platform/Python cells, final standard-suite acceptance
requires all of the following from one coherent, committed source revision:

1. A compatible repaired primary `sagelite` wheel exists.
2. Every standard companion runtime and data dependency required by
   `sagelite[all-needed-extras]` exists as a compatible wheel.
3. A fresh wheel-only install succeeds with no source builds.
4. `python -m pip check` passes.
5. `sagelite-selftest` passes.
6. Required native extension imports and companion executable probes pass.
7. The full installed standard doctest sweep exits successfully with no failed
   examples, failed modules, framework errors, or timeouts.

The acceptance doctest tag set is explicitly `--optional=sage`. This means
the normal Sage tests, not tests requiring optional third-party packages.
Always pass this option explicitly because the current helper default is
`sage,optional`.

Install `sagelite[all-needed-extras]` for certification even though the test
tag set is only `sage`. The extra supplies the complete runtime and data
closure needed by standard Sage; it does not redefine optional tests as
release blockers.

The following do not count as final acceptance evidence:

- a source-tree Sage test run;
- a raw, unrepaired Linux wheel;
- a build or install that inherits Sage paths, `PYTHONPATH`,
  `LD_LIBRARY_PATH`, or runtime state from the build tree;
- a venv modified by manually copying extensions or runtime files;
- an install that consults the host system for a bundled standard runtime;
- a short doctest run, targeted failure rerun, or import-only smoke;
- a run from an uncommitted source tree;
- a retagged wheel that has not been revalidated for its advertised metadata.

## Machine And Storage Assignment

Use SSH aliases, never literal IP addresses. Their backing addresses may
change.

| Role | Access | Work assigned here | Bulk storage |
|---|---|---|---|
| Controller | current CoCalc container | source edits, commits, orchestration, status reports, merged wheelhouse assembly, R2 publication | `/scratch` |
| Linux x86_64 builder | `ssh host` | all Linux x86_64 builds, containers, clean installs, smoke tests, and full tests | `/mnt/cocalc-scratch` |
| Apple Silicon builder | `ssh m1` | all arm64 work: native macOS arm64 and native Linux aarch64 containers or VMs | `/Volumes/sage` |

Rules:

- Keep the canonical source checkout at `/home/user/sage` in the controller.
- Do not do heavy builds in the controller filesystem outside `/scratch`.
- Do not put build trees, wheelhouses, venvs, caches, or large logs in `/`,
  `/tmp`, or `$HOME` on either remote host.
- On `host`, set all build roots, container bind mounts, caches, `TMPDIR`, and
  venv paths below `/mnt/cocalc-scratch`.
- On `m1`, set all such paths below `/Volumes/sage`.
- Use `host` only for x86_64 work. Do not run Linux aarch64 under qemu there
  merely because the native arm64 environment is temporarily unavailable.
- Use `m1` for Linux aarch64 as well as macOS arm64. Prefer native arm64 Linux
  Docker containers on the Mac. A persistent Multipass VM is acceptable when
  Docker is unsuitable.
- Verify the architecture inside the actual build and test environment, not
  only on the outer host. Expect `x86_64` for `host`, `arm64` for macOS, and
  `aarch64` or `arm64` inside Linux arm64.
- The R2 secret is available only to the controller at
  `/run/secrets/cocalc/sagelite-r2-bucket.sh`. Never print it, copy it to a
  remote host, include it in logs, or commit it.
- Publish to R2 from the controller. Do not publish directly from a builder.

As of the latest preflight, `m1` is reachable and has about 239 GiB free on
`/Volumes/sage`. Homebrew Python 3.12, 3.13, and 3.14 are installed. The native
Linux arm64 backend is a persistent Lima 2.1.4 Ubuntu 24.04 VM named
`sagelite-linux-arm64`, using QEMU/HVF with 8 CPUs, 20 GiB memory, and a
160 GiB disk below `/Volumes/sage/.lima`. Its guest reports `Linux` and
`aarch64`, has about 151 GiB free, runs Docker 29.6.1 as `linux/arm64`, and
passed a native arm64 container probe with no block or ext4 errors. Multipass
1.16.3 is also installed and authenticated, but its test guests did not
complete DHCP on this macOS host; do not move the build to `host` merely to
avoid the working Lima backend.

After its changed address was corrected, `host` was reachable again and
reported `x86_64` with both Docker and Podman installed. Its bulk scratch
filesystem was enlarged and had about 104 GiB free at that controller check.
On 2026-07-15 the alias instead reached an `x86_64` staging host where the
expected `/mnt/cocalc-scratch` mount was absent. That host had only 64 GiB free
on `/mnt/cocalc`, below the 100 GiB heavy-build threshold, and provided Podman
but not Docker or a host CPython 3.14. Do not start an x86_64 rebuild until the
expected bulk volume is restored or another in-scope filesystem on `host` is
explicitly shown to satisfy the threshold. Treat future SSH reachability or
mount failures as a preflight problem, not as evidence that the host assignment
has changed.

On 2026-07-16, repeated preflight attempts to `host` timed out during SSH
connection. The next x86_64 iteration remains blocked until the assigned host
is reachable and its required bulk filesystem can be checked again. Independent
work continued on `m1`: exact pushed source `bd3d4c40efe` produced the repaired
macOS arm64 CPython 3.14 `post51` primary, and its CPython 3.14-compatible
168-wheel closure passed deterministic pip resolution and tag checks. The
strict fresh short gate was rejected after its runtime manifest proved that
the wheel reused the still-present build venv as `SAGE_LOCAL` and selftest used
Kenzo from that build tree. The `post52` source fix selects the active Python
prefix for an installed wheel while preserving source-build and explicit
environment configuration. Exact pushed source `b2350b4d3d4` produced the
repaired `post52` primary and its strict 168-wheel closure, but its fresh gate
showed that `var(force=True)` still consulted generated build configuration.
The gate was rejected. The `post53` fix makes forced fallback selection bypass
both the process environment and generated configuration. Exact `post53`
source then produced a repaired primary and strict 168-wheel closure. Its
fresh install and `pip check` passed, and the prefix hierarchy relocated
correctly, but `KENZO_FAS` still fell back to the build path after the
compatibility guard rejected the companion under Maxima's distinct ECL
support directory. An explicit probe confirmed that weakening the guard would
abort ECL. The `post54` repair preserves the guard while preventing installed
wheels from consulting build-time Kenzo configuration. Exact `post54` source
produced a repaired primary and strict 168-wheel closure. Its independent
fresh short and full gates passed strict preflight, wheel-only installation,
`pip check`, runtime isolation, selftest, all 3,953 installed standard modules
with zero failures, and packaged pytest with 226 passes and 5 skips. The full
unrestricted doctest took 791.8 seconds and the validator exited zero after
2,186.243 seconds. Details are in
`agents/sagelite-macos-arm64-cp314-validation.md`.

Later on 2026-07-16, `host` still timed out, so the next independent work-order
cell ran on the native Linux aarch64 backend. Deliberate cleanup retained the
accepted macOS and Linux wheelhouses and concise validation evidence while
restoring 112 GiB free on `/Volumes/sage` and 110,081,482,752 bytes free in
the Lima guest. Exact pushed source `9492b6cbf83` (`10.9.post54`) produced a
repaired CPython 3.12 primary and strict 191-wheel closure. After native
CPython 3.12 `pycosat` and `cysignals` supplements repaired the only closure
gap, the fresh short gate passed strict preflight, wheel-only installation,
`pip check`, runtime manifest, selftest, all 3,953 installed standard modules
with zero failures, and packaged pytest with 229 passes and 2 skips. A separate
fresh full gate then passed the same contract, all selftests, all 3,953 modules
with zero failures in 883.4 seconds, and packaged pytest with 229 passes and 2
skips. Its validator exited zero after 1,630.778 seconds. Details are in
`agents/sagelite-linux-aarch64-cp312-validation.md`.

On 2026-07-17, all three new connection attempts to `host` timed out. The
public manifest remained the 177-wheel set generated on 2026-07-09. The
native Linux arm64 guest was idle but initially below the 100 GiB heavy-build
threshold. Targeted cleanup removed only disposable source checkouts, host
venvs, and install homes from completed runs while retaining the accepted
CPython 3.12, 3.13, and 3.14 wheelhouses and full-validation evidence. This
restored 108,155,944,960 bytes free. Commit `e15c05ab4be` (`10.9.post54`) was
selected as the release-candidate source, verified as pushed, transferred in
a 145,749,785-byte exact-SHA bundle whose SHA256 is
`c30d53dc6364e9be0857fe4549f1f8dccd161c2552da58f9d01aa6707d465ad6`,
and checked out cleanly in the native guest. Its Linux aarch64 CPython 3.13
build and gated short/full watcher ran at
`/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260717-000806-e15c05ab4be`.
The build failed before wheel creation because a retained Meson install marker
and importable module had no matching prefix launcher, and `pplpy` therefore
could not find the `meson` executable. The cache validator now requires that
launcher before reusing the marker. The watcher correctly skipped validation;
no new wheel or pass is claimed. Details are in
`agents/sagelite-linux-aarch64-cp313-validation.md`.

The repair commit `4071f482bcc` passed focused repository checks, was pushed
and verified, and was transferred to the native guest as a 145,752,626-byte
depth-one exact-HEAD bundle with SHA256
`6dcb540bb8aa59de419210b0a21f6173e4dba99264a4e8a91d20b2b67a94c8bf`.
After precise cleanup of only the failed run's disposable checkout, venv, and
empty artifact directories, the replacement CPython 3.13 build launched with
107,499,569,152 bytes free. Its exact clean checkout and gated watcher are
at
`/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260717-003947-4071f482bcc`.
The native build produced a repaired 236,421,410-byte `post54` primary with
SHA256 `5c7e1322622acf6c5a0a221a1c551bcff08531aba3bca43c261b54282e101811`.
Its first closure attempt stopped before installation because the retained
`post33` seed had an obsolete Meataxe companion. A clean retry combined the
accepted ABI-independent `post54` companions, accepted CPython 3.13
`cysignals` and `pycosat`, and the exact new primary, `pplpy`, Maxima, and
QEPCAD wheels. The resulting strict 191-wheel closure passed independent
fresh short and full gates: wheel-only installation, `pip check`, runtime
isolation, every selftest, all 3,953 installed standard modules with zero
failures, and packaged pytest with 229 passes and 2 skips. The unrestricted
doctest sweep took 819.8 seconds and the full validator exited zero after
1,550.013 seconds. Details are in
`agents/sagelite-linux-aarch64-cp313-validation.md`.

The next scheduled iteration again found `host` unreachable by SSH, while the
native Linux arm64 guest was idle and had 105,595,858,944 bytes free. The
public R2 manifest remained the 177-wheel set generated on 2026-07-09. Exact
pushed release-candidate source `4071f482bcc` and its verified
145,752,626-byte bundle were checked out cleanly for the Linux aarch64 CPython
3.14 rerun at
`/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260717-023339-4071f482bcc`.
The native build produced a repaired 237,288,901-byte `post54` primary with
SHA256 `4ae5dbfc89bc1728dc103d5605d9e9468a64a2a0c9d43d7fea7be457ff595764`.
Its strict 180-wheel closure passed the fresh short gate. The first full run
then transiently misclassified the known prime square `(2^29-3)^2` in four
repeated constructor examples, causing four follow-on failures in one
polynomial module. An exact-seed focused replay, including 100 constructor
repetitions, passed. A separately named fresh full rerun from the unchanged
closure passed wheel-only installation, `pip check`, runtime isolation, every
selftest, all 3,953 installed standard modules with zero failures, and
packaged pytest with 229 passes and 2 skips. Its validator exited zero after
1,661.187 seconds. Details are in
`agents/sagelite-linux-aarch64-cp314-validation.md`.

The following scheduled iteration again found `host` unreachable on all three
bounded SSH attempts. The public R2 manifest remained the 177-wheel set
generated on 2026-07-09. Exact pushed release-candidate source `4071f482bcc`
(`10.9.post54`) completed its native macOS arm64 CPython 3.12 build and
produced a repaired 102,252,654-byte primary with SHA256
`f45f17aba5ca6f6564097bb0e4d1cf6d6df003bcabde9743e7a8da6e79be6503`.
Its deterministic strict closure contains 180 compatible wheels totaling
13,896,962,399 bytes. The fresh neutral-path short gate passed wheel-only
installation, `pip check`, runtime isolation, every selftest, and packaged
pytest with 226 passes and 5 skips, but its 3,954-module standard sweep found
one failure: `pycryptosat==5.14.7` returned the correct Boolean solution with
a different dictionary insertion order. The gate was rejected. The `post55`
working change compares the expected mapping by dictionary equality; the
complete focused module replay passed with `brial` and `pycryptosat` enabled.
An exact `post55` rebuild and both fresh strict gates are required. Details are
in `agents/sagelite-macos-arm64-cp312-validation.md`.

Exact pushed `post55` source `94480894829d` then produced a repaired
102,265,036-byte macOS arm64 CPython 3.12 primary with SHA256
`932d038a86563b873e338b56b328a92018d645fbee0f77aed02d22a50390aec5`.
Its strict 180-wheel closure totals 13,896,965,238 bytes. The independent fresh
short gate passed strict installation, isolation, every selftest, all 3,953
standard modules with zero failures, and packaged pytest with 226 passes and 5
skips. The separate full gate passed installation, isolation, and selftest,
then rejected one module after a seed-sensitive elliptic-curve kernel doctest
exceeded the 600-second worker timeout. The reducer classified one
performance-only timeout and zero failed examples. Exact pushed `post56`
source `288c3f21968` replaces both random searches in that coverage block with
deterministic equivalents. The complete module passed all 497 doctests under
the exact failing seed and original timeout in 7.5 seconds. A coherent post56
rebuild and both independent fresh gates are required; post55 is not accepted.
Details are in `agents/sagelite-macos-arm64-cp312-validation.md`.

Exact pushed `post56` source `288c3f21968` then completed its native macOS
arm64 CPython 3.12 build after all three bounded SSH attempts to the
higher-priority `host` target timed out. The public R2 manifest remained the
177-wheel set generated on 2026-07-09. A controlled same-tree resume raised
the soft file-descriptor limit for Maxima. The repaired 102,263,590-byte
primary has SHA256
`6b700467acc9083a7f9176e8ff684f50ab53e48810f6a1f84f2dcacea7561b7b`.
Its strict 180-wheel closure totals 13,896,963,792 bytes. Independent fresh
short and full gates both passed strict preflight, binary-only
`sagelite[all-needed-extras]` installation, `pip check`, runtime isolation,
all 102 selftests, all 3,953 installed `--optional=sage` modules with zero
failures, and packaged pytest with 226 passes and 5 skips. The unrestricted
suite completed in 742.4 seconds and the full validator exited zero after
1,991.206 seconds. Post56 is accepted locally for this cell. The public R2
preview remains unchanged and no artifact was published. Details are in
`agents/sagelite-macos-arm64-cp312-validation.md`.

The following scheduled iteration found the higher-priority `host` target
reachable as Linux `x86_64` with its expected bulk mount restored, but only
96,531,124,224 bytes free. Targeted cleanup removed only two superseded,
inactive `post6` and `post7` automation validation trees, restoring
129,343,483,904 bytes free. Exact pushed `post56` source
`288c3f21968` passed architecture, version, and clean-checkout guards. Its
first durable launch stopped before compilation because cibuildwheel's
read-only `/host` mount prevented writing the retained manylinux prefix. A
focused container probe proved a read/write bulk over-mount, and a fresh
exact-SHA replacement is now building natively for Linux x86_64 CPython 3.14
under `sagelite-post56-x86-cp314-build-r1.service` at
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-095911-288c3f21968`.
It passed the failed prefix-write phase in an actual x86_64 manylinux
container. No wheel or validation result is claimed yet. The public R2
manifest remains the 177-wheel set generated on 2026-07-09. Details are in
`agents/sagelite-linux-x86_64-cp314-validation.md`.

That first replacement then stopped because CPython 3.14 refused to create a
venv through the retained prefix symlink. A reversible host bind-mount probe
proved a real-directory path, and a fresh exact-`post56` retry cleared venv
creation but exposed a stale cache marker: when the prefix interpreter was
missing, the before-all hook skipped both venv initialization and
`python_build` marker validation. Exact pushed `post57` source
`6361dc1935c` initializes the missing selected-ABI venv before validating
cached modules. Its focused checks pass. The fresh authoritative build at
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-101057-6361dc1935c`
is running under `sagelite-post57-x86-cp314-build.service`. With the exact
missing-interpreter state reproduced, its log proves that the new branch ran,
stale Python markers were removed, and `python_build 1.4.2` installed
successfully. No wheel or validation result is claimed yet.

That exact CPython 3.14 build then completed with exit code zero and produced a
244,935,135-byte repaired `post57` primary with SHA256
`9f806bab9af28243e8437ef6b39d13188f3407f3f917e39ab1ffbd1e34b19b53`.
Because the Linux contract emits the complete platform companion set from its
CPython 3.12 leg, exact `post57` source also completed a synchronized cached
CPython 3.12 build at
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp312-companions-20260717-105534-6361dc1935c`.
It produced 82 repaired wheels totaling 4,654,304,280 bytes, and its full hash
inventory passed. Marker-aware comparison found only the policy-gated portable
4D polytope database missing from that output. The previously accepted
9,100,370,523-byte `py3-none-any` wheel is transferring durably from `m1`
under controller tmux session `sagelite-polytopes4d-transfer`, with artifacts
at `/scratch/sagelite-automation/polytopes4d-transfer-20260717`. A resumed
iteration found the transfer healthy; at `2026-07-17T12:39:14Z` the destination
had grown to 2,969,457,664 bytes, while the latest capacity check found
115,927,535,616 bytes free on `host`.
Controller tmux session `sagelite-post57-x86-cp314-watch` is queued to launch
exactly one durable host validation service after the transfer succeeds. Its
remote launcher will first verify the expected SHA256
`e22d60ebd324d848871f0980a7e48226396b5ed5ebecab23f8e1b5482b6438f2`,
then finish deterministic closure resolution and run independent fresh strict
short and full gates. No install or validation result is claimed yet, and the
public manifest remains the 177-wheel set generated on 2026-07-09.

The durable transfer subsequently completed with the expected size and SHA256,
and the watcher launched exactly one guarded validation service. The strict
181-wheel, 14,288,021,185-byte closure passed deterministic preflight, fresh
binary-only installation, `pip check`, runtime isolation, every selftest, and
packaged pytest with 229 passes and 2 skips. The short gate was rejected after
one of 3,954 seen modules failed: a successful `sage.misc.cython` C++ compile
printed Zig libc++'s nullability-warning flood because one parallel-output
fragment fused a Zig source excerpt with a pathless warning location. The
reducer reported one failed module and one failed example; the full gate was
correctly skipped. The `post58` working fix suppresses this interleaving shape
only when a nearby full Zig diagnostic corroborates the same line and column.
It preserves errors, unrelated warnings, and uncorroborated fragments. Seven
focused cases pass, and the exact helper reduces the preserved 4,464,649-byte
stderr to zero. An exact committed `post58` rebuild and both fresh gates are
required. Details are in
`agents/sagelite-linux-x86_64-cp314-validation.md`.

The focused repair commit `8bbd27d5134` was pushed and verified. Precise
cleanup removed only the rejected gate's inactive 21 GB install venv while
retaining its wheelhouse and validation evidence, restoring 108,724,629,504
bytes free. Exact clean `post58` source is now building natively for Linux
x86_64 CPython 3.14 under `sagelite-post58-x86-cp314-build.service` at
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-140439-8bbd27d5134`.
The live build passed source, architecture, capacity, idle-Docker, and prefix
guards and entered cached CPython 3.14 environment setup. No `post58` wheel or
validation result is claimed yet.

That exact build completed and produced a repaired 244,935,373-byte `post58`
primary with SHA256
`101544fef2dbd3b1b3ff35ca9013bb4196ebfd0283d1ac80540004a33e84c02d`.
Its strict 181-wheel, 14,288,021,423-byte closure passed the independent fresh
short gate with strict preflight, binary-only installation, `pip check`,
runtime isolation, every selftest, all 3,953 standard modules with zero
failures, and packaged pytest with 229 passes and 2 skips. The separate fresh
full gate passed installation, isolation, selftest, and packaged pytest, but
rejected `sage.misc.cython` after character-level parallel interleaving split
one pathless Zig libc++ warning fragment from intact matching diagnostics by
thousands of lines. The reducer reported one failed module and one failed
example. The `post59` working correction requires exact line-and-column
corroboration from any complete Zig libc++ diagnostic in the same compiler
stream, while preserving unrelated and uncorroborated output. Its focused
positive and negative cases pass, and the exact preserved 4,458,206-byte
stream reduces to zero. An exact committed rebuild and both fresh gates are
required. Details are in
`agents/sagelite-linux-x86_64-cp314-validation.md`.

Exact pushed `post59` source `48f88027b39` is now building natively for Linux
x86_64 CPython 3.14 under `sagelite-post59-x86-cp314-build.service` at
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-160733-48f88027b39`.
The run passed exact-source, clean-checkout, version, architecture, idle-Docker,
persistent-prefix, and capacity guards. It completed raw primary compilation
and entered wheel repair while both the build and watcher services remained
active. The watcher will assemble the strict closure and run independent fresh
short and full gates only after a successful build. No `post59` wheel or
validation result is claimed yet. The public R2 manifest remains the 177-wheel
set generated on 2026-07-09.

That exact build produced a repaired 244,935,382-byte `post59` primary with
SHA256 `f1aa27bb993bcbae3340409c9152c44196cef7c70a126738d042ce56cb2e785d`.
Its strict 181-wheel, 14,288,021,432-byte closure passed the independent fresh
short gate with binary-only installation, `pip check`, runtime isolation,
every selftest, all 3,953 standard modules with zero failures, and packaged
pytest with 229 passes and 2 skips. The separate fresh full gate passed the
same setup and confirmed the `sage.misc.cython` repair, but rejected one of
3,954 seen modules under seed
`166469527479524600599751122278591708351`. A sampled composite `q=12` made
`special_supersingular_curve` request a direct cyclic normalized isogeny that
does not exist; three later failures cascaded from the first exception. The
exact-seed module replay reproduced the failure, while the existing
composite-isogeny enumeration succeeded for the same `p=263`, extension
degree 8, and `q=12`. The `post60` working correction lets that constructor
`ValueError` select the existing fallback and adds a deterministic regression
example. A focused source overlay passed all 548 module doctests under the
exact failing seed. A committed exact `post60` rebuild and both fresh gates
are required. No `post59` full pass or public publication is claimed.

The focused repair is committed and pushed as exact `post60` source
`22a2cb56739`. After targeted cleanup of only completed `post59` install homes
and three superseded failed `post56` run trees, its exact clean checkout
started a native Linux x86_64 CPython 3.14 build with 107,563,696,128 bytes
free. The build is active under `sagelite-post60-x86-cp314-build.service` at
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp314-20260717-175700-22a2cb56739`.
It passed exact-source, clean-checkout, version, architecture, idle-Docker,
persistent-prefix, and pre-launch capacity guards and entered cached native
prerequisite setup. A separate guarded watcher will assemble the strict
closure and run both independent fresh gates only after build success. No
`post60` wheel or validation result is claimed yet.

That exact build completed with exit code zero and produced a repaired
244,935,492-byte `post60` primary with SHA256
`20c994068d744e08a0fd9c6c4196839517721a7b530a3f89e1caa47a473c96bb`.
Its strict 181-wheel, 14,288,021,542-byte closure passed independent fresh
short and full gates: strict preflight, binary-only
`sagelite[all-needed-extras]` installation, `pip check`, runtime isolation,
every selftest, all 3,953 installed `--optional=sage` modules with zero
failures, and packaged pytest with 229 passes and 2 skips. The unrestricted
doctest sweep took 914.9 seconds and the full validator exited zero after
1,928.526 seconds. Exact pushed `post60` source `22a2cb56739` is accepted
locally for Linux x86_64 CPython 3.14. The public R2 manifest remains the
177-wheel set generated on 2026-07-09; no artifact was published. Details are
in `agents/sagelite-linux-x86_64-cp314-validation.md`.

The next scheduled iteration selected the highest-priority remaining Linux
x86_64 CPython 3.13 cell. `host` was reachable, idle, and native `x86_64`, but
initially had 106,631,876,608 bytes free, slightly below the binary 100 GiB
heavy-build threshold. Precise cleanup removed only three disposable source
checkouts from completed or superseded runs while retaining their wheelhouses
and validation evidence. Exact pushed `post60` source `22a2cb56739` then
started natively with 107,631,353,856 bytes free under
`sagelite-post60-x86-cp313-build.service` at
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp313-20260717-200455-22a2cb56739`.
Its guarded watcher is active as `sagelite-post60-x86-cp313-watch.service`.
The actual manylinux container reports `x86_64` and CPython 3.13.12; the
selected-ABI cache guard replaced the retained CPython 3.14 interpreter with
CPython 3.13 and entered native prerequisite setup. No wheel or validation
result is claimed yet. The public R2 manifest remains the 177-wheel set
generated on 2026-07-09. Details are in
`agents/sagelite-linux-x86_64-cp313-validation.md`.

That exact build completed with exit code zero and produced a repaired
244,669,165-byte `post60` primary with SHA256
`f65a0903fa98471a38e5f6e145901258d6ef4503369d7febd46a078533f90885`.
The guarded watcher assembled the exact primary, new CPython 3.13 `pplpy`,
and verified portable 4D polytope database, but its first binary-only closure
resolution stopped before installation because PyPI has no CPython 3.13
`pycosat` wheel. The accepted public preview wheel matched manifest SHA256
`bbde2e7c9c887e8e6f63015ac53145d96493dda4976f8ec69626b965641c5773`.
After preserving the initial resolver log, a single guarded validation retry
added that wheel as an ABI-specific input and resolved a strict 192-wheel,
14,292,168,533-byte closure. Independent fresh short and full gates passed
strict preflight, binary-only `sagelite[all-needed-extras]` installation,
`pip check`, runtime isolation, every selftest, all 3,953 installed
`--optional=sage` modules with zero failures, and packaged pytest with 229
passes and 2 skips. The unrestricted sweep took 930.2 seconds and the full
validator exited zero. Exact pushed `post60` source `22a2cb56739` is accepted
locally for Linux x86_64 CPython 3.13. Deliberate cleanup retained its exact
wheelhouse and validation evidence while restoring 107,929,792,512 bytes free
on `/mnt/cocalc-scratch`. The public R2 manifest remains the 177-wheel set
generated on 2026-07-09; no artifact was published. Details are in
`agents/sagelite-linux-x86_64-cp313-validation.md`.

The next scheduled iteration selected the final unsynchronized Linux
`x86_64` cell, CPython 3.12. `host` was reachable, idle, and native `x86_64`.
Precise cleanup removed only regenerated closure copies from rejected runs and
superseded source-transfer inputs, restoring sufficient headroom while
retaining pushed revisions, primary outputs, and concise validation evidence.
Exact pushed `post60` source `22a2cb56739` is now building under
`sagelite-post60-x86-cp312-build.service` at
`/mnt/cocalc-scratch/sagelite-automation/linux-x86_64-cp312-20260717-220219-22a2cb56739`.
Its guarded watcher is active as
`sagelite-post60-x86-cp312-watch.service`. The exact checkout, version,
architecture, idle-Docker, persistent-prefix, and 100 GiB capacity guards all
passed. This CPython 3.12 leg will emit a synchronized platform companion set
before the watcher assembles the strict closure and runs independent fresh
short and full gates. No `post60` wheel or validation result is claimed yet.
The public R2 manifest remains the 177-wheel set generated on 2026-07-09.
Details are in `agents/sagelite-linux-x86_64-cp312-validation.md`.

The next scheduled iteration could not reconcile that `host` job because
three bounded SSH connection attempts timed out. The possibly surviving
Linux x86_64 CPython 3.12 build and watcher were left untouched. Independent
preflight found the native Linux arm64 Lima guest idle but initially below the
100 GiB heavy-build threshold. Precise cleanup removed only superseded
regenerated closure links, inactive disposable source checkouts, and obsolete
source bundles while retaining accepted wheelhouses and validation evidence.
Exact pushed `post60` source `22a2cb56739` was transferred in a verified
145,770,108-byte depth-one bundle with SHA256
`84f2902d2051d598b04430d9ef95b4e9fe672f4d02a0701a653d2764b82285dc`.
Its clean native Linux aarch64 CPython 3.12 build is active under
`sagelite-post60-arm-cp312-build.service` at
`/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260717-223804-22a2cb56739`.
The guarded `sagelite-post60-arm-cp312-watch.service` will assemble a strict
closure and run independent fresh short and full gates only after build
success. Pre-launch guest capacity was 108,560,244,736 bytes. No `post60`
wheel or validation result is claimed yet, and the public R2 manifest remains
the 177-wheel set generated on 2026-07-09.

That exact native Linux aarch64 CPython 3.12 build then completed with exit
code zero and produced 82 repaired primary and companion wheels totaling
4,623,974,563 bytes. The 236,678,592-byte `post60` primary has SHA256
`95ab03ac02865369c08ce3b6b2acb00f5cc54189404084ce4518f65ab7bcfd3b`.
Its deterministic strict 191-wheel closure totals 16,739,251,241 bytes.
Independent fresh short and full gates passed strict preflight, binary-only
`sagelite[all-needed-extras]` installation, `pip check`, runtime isolation,
every selftest, all 3,953 installed `--optional=sage` modules with zero
failures, and packaged pytest with 229 passes and 2 skips. The unrestricted
doctest sweep took 888.6 seconds and the full validator exited zero after
1,617.91 seconds. Exact pushed `post60` source `22a2cb56739` is accepted
locally for Linux aarch64 CPython 3.12. Deliberate cleanup retained its exact
wheelhouse and validation evidence while restoring 107,698,089,984 bytes free
in the native guest. All three bounded `host` attempts timed out, so the
possibly surviving Linux x86_64 CPython 3.12 job remains untouched and
unreconciled. The public R2 manifest remains the 177-wheel set generated on
2026-07-09; no artifact was published. Details are in
`agents/sagelite-linux-aarch64-cp312-validation.md`.

The next scheduled iteration again could not reconcile the possibly surviving
Linux x86_64 CPython 3.12 job because all three bounded `host` SSH attempts
timed out. The public R2 manifest remained the 177-wheel set generated on
2026-07-09, with no `post60` artifact. Independent preflight found `m1` and
its native Linux aarch64 guest idle. Precise cleanup removed only completed
install directories from the accepted Linux aarch64 CPython 3.13 and 3.14
runs while retaining their wheelhouses and validation evidence. This restored
108,866,015,232 bytes free in the guest. Exact pushed `post60` source
`22a2cb56739` is now building natively for Linux aarch64 CPython 3.13 under
`sagelite-post60-arm-cp313-build.service` at
`/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260718-003520-22a2cb56739`.
The exact checkout is clean, and the actual manylinux container reports
Linux `aarch64` and CPython 3.13.12. The guarded
`sagelite-post60-arm-cp313-watch.service` will assemble a strict closure and
run independent fresh short and full gates only after build success. No
`post60` CPython 3.13 wheel or validation result is claimed yet.

That exact native build completed with exit code zero and produced a repaired
236,421,729-byte `post60` primary with SHA256
`3e7b5af8f2381f3a90379561c5f503b92d2a4f7bb19b116c4357575aae097e93`.
Its deterministic strict 191-wheel closure totals 16,738,859,145 bytes. The
fresh short gate passed. The first full gate had one transient `msolve`
wrong-result example; its exact-seed module replay and 200-operation stress
probe passed. A fresh full rerun then had an independent GlucoseSyrup worker
timeout. A separately named init-wrapped fresh full rerun passed strict
preflight, binary-only `sagelite[all-needed-extras]` installation, `pip check`,
runtime isolation, every selftest, all 3,953 installed `--optional=sage`
modules with zero failures, and packaged pytest with 229 passes and 2 skips.
The unrestricted sweep took 842.2 seconds and the validator exited zero after
1,644.45 seconds. Exact pushed `post60` source `22a2cb56739` is accepted
locally for Linux aarch64 CPython 3.13. Deliberate cleanup retained its exact
wheelhouse and validation evidence while restoring 107,511,595,008 bytes free
in the native guest. All three bounded `host` SSH attempts timed out, so the
possibly surviving Linux x86_64 CPython 3.12 job remains untouched and
unreconciled. The public R2 manifest remains the 177-wheel set generated on
2026-07-09; no artifact was published. Details are in
`agents/sagelite-linux-aarch64-cp313-validation.md`.

The next scheduled iteration could not reconcile the possibly surviving
Linux x86_64 CPython 3.12 job because all three bounded `host` SSH attempts
timed out. The public R2 manifest remained the 177-wheel set generated on
2026-07-09, with no `post60` artifact. Independent preflight found `m1` and
its native Linux aarch64 guest idle. Cleanup removed only the completed Linux
aarch64 CPython 3.13 run's disposable source checkout, host venv, and install
homes while retaining its accepted wheelhouse and validation evidence. This
restored 108,741,181,440 bytes free in the guest. Exact pushed `post60` source
`22a2cb56739` is now building natively for Linux aarch64 CPython 3.14 under
`sagelite-post60-arm-cp314-build.service` at
`/home/sage.guest/sagelite-automation/linux-aarch64-cp314-20260718-031637-22a2cb56739`.
The verified 145,770,108-byte exact-SHA bundle and the accepted CPython 3.12
companion closure are reused; the accepted CPython 3.14 `cysignals` and
`pycosat` wheels supply the ABI-specific supplements. The exact checkout is
clean, and the actual manylinux container reports `aarch64` with CPython
3.14.3. The guarded `sagelite-post60-arm-cp314-watch.service` will assemble a
strict closure and run independent fresh short and full gates only after build
success. No `post60` CPython 3.14 wheel or validation result is claimed yet.

That exact native build completed with exit code zero and produced a repaired
237,289,190-byte `post60` primary with SHA256
`c0efdcb2737ec69e7790a027fca870f78388921515491ccc55172342271169ad`.
Its deterministic strict 180-wheel closure totals 16,735,951,613 bytes.
Independent fresh short and full gates passed strict preflight, binary-only
`sagelite[all-needed-extras]` installation, `pip check`, runtime isolation,
every selftest, all 3,953 installed `--optional=sage` modules with zero
failures, and packaged pytest with 229 passes and 2 skips. The unrestricted
doctest sweep took 898.3 seconds and the full validator exited zero after
1,652.432 seconds. Exact pushed `post60` source `22a2cb56739` is accepted
locally for Linux aarch64 CPython 3.14. Deliberate cleanup retained its exact
wheelhouse and validation evidence while restoring 107,425,660,928 bytes free
in the native guest. All three bounded `host` SSH attempts timed out, so the
possibly surviving Linux x86_64 CPython 3.12 job remains untouched and
unreconciled. The public R2 manifest remains the 177-wheel set generated on
2026-07-09; no artifact was published. Details are in
`agents/sagelite-linux-aarch64-cp314-validation.md`.

The next scheduled iteration again could not reconcile the possibly surviving
Linux x86_64 CPython 3.12 build and watcher because all three bounded `host`
SSH attempts timed out. They were left untouched, and no result was inferred.
The public R2 manifest remains the 177-wheel set generated on 2026-07-09, with
fourteen Sagelite primary wheels and no `post60` artifact. Exact pushed
`post60` source `22a2cb56739` completed its native macOS arm64 CPython 3.12
build with exit code zero and produced a repaired 102,263,875-byte primary
with SHA256
`4b450cf0fc612aca7737f55d1df8b332bfbd18af28bb38b022cb802480dc2566`.
Its deterministic strict closure contains 180 compatible wheels totaling
13,896,964,077 bytes. A single guarded watcher is active under tmux session
`sagelite_cp312_post60_validate` at
`/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260718-050339-22a2cb56739`.
The fresh short gate passed strict preflight, binary-only
`sagelite[all-needed-extras]` installation, and `pip check`, then entered the
installed runtime-manifest scan before selftest and the standard module sweep.
The full gate is guarded on a zero short-gate exit. No short or full pass is
claimed yet. Details are in
`agents/sagelite-macos-arm64-cp312-validation.md`.

That guarded macOS validator then completed.  The fresh short gate passed
strict preflight, binary-only installation, `pip check`, runtime isolation,
every selftest, all 3,953 standard modules with zero failures, and packaged
pytest with 226 passes and 5 skips.  The separate fresh full gate rejected one
of 3,954 seen modules under seed
`213528177385953471796963154323692312109`: four repeated
`GF((2^29-3)^2)` constructors rejected the square as a prime power, causing
four follow-on failures in the same polynomial module.  This is the same rare
decomposition failure previously seen on Linux aarch64 CPython 3.14, so the
gate is rejected rather than accepted as transient.  The `post61` working
repair decomposes square finite-field orders through GMP's exact integer
square root before the general PARI perfect-power path.  A diagnostic overlay
passed all 150 constructor doctests and all 1,363 polynomial-module doctests
under the exact failing seed.  A committed exact `post61` rebuild and both
fresh strict gates are required.  No `post60` full pass or publication is
claimed.  Details are in
`agents/sagelite-macos-arm64-cp312-validation.md`.

The committed repair is exact pushed `post61` source `33f8a4dae1d`.  Precise
cleanup on `m1` removed only the two completed disposable `post60` validation
installs while retaining their wheelhouse and evidence.  Native macOS and its
Linux arm64 guest were idle, and the post-transfer launch guard recorded
107,937,693,696 bytes free.  The exact 144,083,559-byte source archive has
SHA256
`a708b1fbe826894a03c0ed2606756ff0e60a55c4bd2d6686c24bfb0266dc4314`,
and its independently materialized tree matches committed tree
`c74fc7f733b8934357e7db5bdd24208da0540ad8`.  One native macOS arm64
CPython 3.12.13 build is active under tmux session
`sagelite_cp312_post61_build` at
`/Volumes/sage/sagelite-automation/macos-arm64-cp312-20260718-065714-33f8a4dae1d`.
This is exact-source build-start evidence only; no `post61` wheel, validation
pass, or publication is claimed.

That exact build then completed with exit code zero and produced a repaired
102,263,610-byte primary with SHA256
`0056083a2847e795d38e2e146f9d3684a1b5253ed54c407f27e52c66781cc17e`.
Its deterministic strict closure selected all 180 staged projects and removed
none: one primary, 68 companions, and 111 third-party wheels totaling
13,896,963,812 bytes.  A single guarded validator is active under tmux session
`sagelite_cp312_post61_validate`; its fresh short gate is installing the
binary-only exact closure, and the separate fresh full gate is guarded on a
zero short-gate exit.  No `post61` validation pass or publication is claimed
yet.

The guarded validator then completed with exit code zero.  The fresh short
gate passed strict preflight, binary-only installation, `pip check`, all 102
selftest checks, runtime isolation with zero leaks, all 3,953 installed
standard modules with zero failures, and packaged pytest with 226 passes and
5 skips.  Its standard sweep took 477.1 seconds, and the gate took 1,773.109
seconds.  The separate fresh full gate repeated that contract; its
unrestricted sweep passed all 3,953 modules with zero failures in 747.9
seconds, packaged pytest again passed with 226 passes and 5 skips, and the
gate took 1,988.185 seconds.  The prime-square failure did not recur.  Exact
pushed `post61` source `33f8a4dae1d` is accepted locally for macOS arm64
CPython 3.12.  Precise cleanup retained the source archive, strict wheelhouse,
and all validation evidence while restoring 110,707,924,992 bytes free.  No
artifact was published.

The next scheduled iteration could not reconcile the possibly surviving Linux
x86_64 CPython 3.12 `post60` build and watcher because all three bounded SSH
attempts to `host` timed out.  They were left untouched, and no result was
inferred.  The public R2 manifest remains the 177-wheel set generated on
2026-07-09, with fourteen Sagelite primary wheels and no `post60` or `post61`
artifact.  Independent preflight found `m1` and its native Linux aarch64 Lima
guest idle.  Precise cleanup removed only regenerated closures, obsolete
primary-wheel directories from superseded failure runs, and the recorded
`post60` source bundle while retaining accepted wheelhouses and validation
evidence.  This restored 110,247,145,472 bytes free in the guest.  Exact pushed
`post61` source `33f8a4dae1d` was transferred in a verified 145,788,566-byte
depth-one bundle with SHA256
`c2670796bf1b7a7254b7a9824f1caedd60dbb5295c2c08d658ce3bf5e00a4ab7`.
Its clean native Linux aarch64 CPython 3.12 build is active under
`sagelite-post61-arm-cp312-build.service` at
`/home/sage.guest/sagelite-automation/linux-aarch64-cp312-20260718-083928-33f8a4dae1d`.
The guarded `sagelite-post61-arm-cp312-watch.service` will assemble a strict
closure and run independent fresh short and full gates only after build
success.  The actual manylinux container reports Linux `aarch64` and CPython
3.12.13.  Pre-launch guest capacity was 110,101,356,544 bytes.  No `post61`
wheel, validation pass, or publication is claimed yet.

That exact native build then completed with exit code zero and produced 82
repaired primary and companion wheels totaling 4,623,984,325 bytes.  The
236,678,874-byte `post61` primary has SHA256
`ffe510e0ed81fe05b38e511e29df3c9e21c3871d31e7c7379eba86e67b08a4f8`.
Its deterministic strict 191-wheel closure totals 16,739,264,493 bytes.
Independent fresh short and full gates passed strict preflight, binary-only
`sagelite[all-needed-extras]` installation, `pip check`, runtime isolation
with zero leaks, all 102 selftest checks, and all 3,953 installed
`--optional=sage` modules with zero failures.  The unrestricted sweep took
901.0 seconds and the full validator exited zero after 1,651.972 seconds.
Exact pushed `post61` source `33f8a4dae1d` is accepted locally for Linux
aarch64 CPython 3.12.  Deliberate cleanup retained its exact strict closure
and validation evidence while restoring 108,312,612,864 bytes free in the
native guest.  The public R2 manifest remains the 177-wheel set generated on
2026-07-09; no artifact was published.  Details are in
`agents/sagelite-linux-aarch64-cp312-validation.md`.

The next scheduled iteration again could not reconcile the possibly surviving
Linux x86_64 CPython 3.12 build and watcher because all three bounded `host`
SSH attempts timed out.  They were left untouched, and no result was inferred.
The public R2 manifest remains the 177-wheel set generated on 2026-07-09, with
fourteen Sagelite primary wheels and no `post60` or `post61` artifact.
Independent preflight found `m1` and its native Linux aarch64 Lima guest idle.
Precise cleanup removed only two completed install-home trees and the
regenerated strict closure from the superseded `post54` CPython 3.13 run while
retaining accepted current wheelhouses and validation evidence.  Exact pushed
`post61` source `33f8a4dae1d` is now building natively for Linux aarch64
CPython 3.13 under `sagelite-post61-arm-cp313-build.service` at
`/home/sage.guest/sagelite-automation/linux-aarch64-cp313-20260718-103503-33f8a4dae1d`.
The retained 145,788,566-byte exact-SHA bundle has verified SHA256
`c2670796bf1b7a7254b7a9824f1caedd60dbb5295c2c08d658ce3bf5e00a4ab7`.
The exact checkout is clean, and the actual manylinux container reports Linux
`aarch64` and CPython 3.13.12.  The guarded
`sagelite-post61-arm-cp313-watch.service` will assemble a strict closure and
run independent fresh short and full gates only after build success.
Pre-launch guest capacity was 109,758,222,336 bytes.  No `post61` CPython 3.13
wheel, validation pass, or publication is claimed yet.  Details are in
`agents/sagelite-linux-aarch64-cp313-validation.md`.

That exact native build then completed with exit code zero and produced a
repaired 236,421,997-byte `post61` primary with SHA256
`b79d50401786b545bf766a08858b57e9f75ec4b01d6f9c3bededbe584614f44e`.
Its deterministic strict 191-wheel closure totals 16,738,873,278 bytes.
Independent fresh short and full gates passed strict preflight, binary-only
`sagelite[all-needed-extras]` installation, `pip check`, runtime isolation
with zero leaks, all 102 selftest checks, all 3,953 installed
`--optional=sage` modules with zero failures, and packaged pytest with 229
passes and 2 skips.  The unrestricted sweep took 821.9 seconds and the full
validator exited zero after 1,574.419 seconds.  Exact pushed `post61` source
`33f8a4dae1d` is accepted locally for Linux aarch64 CPython 3.13.  Deliberate
cleanup retained its exact strict closure and validation evidence while
restoring 108,068,274,176 bytes free in the native guest.  Three new bounded
`host` attempts timed out, so the possibly surviving Linux x86_64 CPython 3.12
job remains untouched and unreconciled.  The public R2 manifest remains the
177-wheel set generated on 2026-07-09; no artifact was published.  Details
are in `agents/sagelite-linux-aarch64-cp313-validation.md`.

## Scratch Layout

Use UTC timestamps and the committed source SHA in every run identifier:

```text
<target>-<YYYYMMDD-HHMMSS>-<short-sha>
```

Recommended roots:

```text
# Controller
/scratch/sagelite-automation/
/scratch/sagelite-r2-work/

# host
/mnt/cocalc-scratch/sagelite-automation/

# m1
/Volumes/sage/sagelite-automation/
```

Each run directory should contain or point to:

```text
source/                 exact source revision used for the build
build/                  disposable build tree
cache/                  bounded reusable build cache
wheelhouse/             wheels for exactly one target contract
install/                disposable clean validation venv
validation/             durable validation artifacts
command.log             top-level build or validation log
run-metadata.txt        target, host, source SHA, commands, and timestamps
pid                     durable background-process PID when applicable
exit-code               final process exit code
disk-before.txt         filesystem usage before the run
disk-after.txt          filesystem usage after cleanup
```

Do not combine primary wheels for multiple Python ABIs in an authoritative
per-cell wheelhouse. The R2 publication wheelhouse is a separate merged
artifact assembled only after per-cell validation.

Before a heavy build, require at least 100 GiB free on the assigned bulk
filesystem. Before a test-only full-suite run, require at least 30 GiB free.
If the threshold is not met, clean only automation-owned disposable paths or
ask the user for more space. Never delete an unfamiliar directory.

Only one heavy build may run on each builder at a time. A macOS build and a
Linux arm64 build therefore do not run concurrently on `m1` unless the user
explicitly increases that limit.

## Current Matrix Checkpoint

The public preview index is:

```text
https://sagelite.sagemath.org/dev/simple/
```

The current preview release is `10.9.post9`. At the last review, the public
R2 manifest contained 177 wheel files and fourteen Sagelite primary wheels:
seven each for `10.9.post8` and `10.9.post9`.

Status meanings:

- `full`: a full installed standard doctest baseline has passed;
- `smoke`: fresh install, `pip check`, and representative runtime tests pass;
- `missing`: no current primary preview wheel exists;
- a version in parentheses identifies the preview version that supplied the
  recorded evidence.

| Platform | Python | Primary wheel | Standard validation | Optional-wheel-ready validation |
|---|---:|---|---|---|
| Linux x86_64 | 3.12 | yes (`post9` public); exact `post60` job unreconciled | full baseline; 3,953 modules and 0 failures on the earlier accepted build. The exact pushed `post60` build and guarded watcher may still survive on `host`, but three new bounded SSH attempts timed out. They were left untouched; no synchronized `post60` result is claimed yet | smoke (`post8`) |
| Linux x86_64 | 3.13 | yes (`post60`, local; `post9`, public) | full (`post60`); exact pushed source `22a2cb56739` produced a repaired primary and strict 192-wheel closure. Independent fresh short and full gates passed strict preflight, binary-only `sagelite[all-needed-extras]` installation, `pip check`, runtime isolation, every selftest, all 3,953 installed `--optional=sage` modules with zero failures, and packaged pytest with 229 passes and 2 skips. The unrestricted sweep completed in 930.2 seconds | smoke (`post8`) |
| Linux x86_64 | 3.14 | yes (`post60`, local; `post9`, public) | full (`post60`); exact pushed source `22a2cb56739` produced a repaired primary and strict 181-wheel closure. Independent fresh short and full gates passed strict preflight, binary-only `sagelite[all-needed-extras]` installation, `pip check`, runtime isolation, every selftest, all 3,953 installed `--optional=sage` modules with zero failures, and packaged pytest with 229 passes and 2 skips. The unrestricted sweep completed in 914.9 seconds | smoke (`post9`) |
| Linux aarch64 | 3.12 | yes (`post61`, local; `post9`, public) | full (`post61`); exact pushed source `33f8a4dae1d` produced a repaired primary and strict 191-wheel closure. Independent fresh short and full gates passed strict preflight, binary-only `sagelite[all-needed-extras]` installation, `pip check`, runtime isolation with zero leaks, all 102 selftest checks, and all 3,953 installed `--optional=sage` modules with zero failures. The unrestricted sweep completed in 901.0 seconds | smoke (`post8`), with system `git` for GitPython |
| Linux aarch64 | 3.13 | yes (`post61`, local) | full (`post61`); exact pushed source `33f8a4dae1d` produced a repaired primary and strict 191-wheel closure. Independent fresh short and full gates passed strict preflight, binary-only `sagelite[all-needed-extras]` installation, `pip check`, runtime isolation with zero leaks, all 102 selftest checks, all 3,953 installed `--optional=sage` modules with zero failures, and packaged pytest with 229 passes and 2 skips. The unrestricted sweep completed in 821.9 seconds | none |
| Linux aarch64 | 3.14 | yes (`post60`, local) | full (`post60`); exact pushed source `22a2cb56739` produced a repaired primary and strict 180-wheel closure. Independent fresh short and full gates passed strict preflight, binary-only `sagelite[all-needed-extras]` installation, `pip check`, runtime isolation, every selftest, all 3,953 installed `--optional=sage` modules with zero failures, and packaged pytest with 229 passes and 2 skips. The unrestricted sweep completed in 898.3 seconds | none |
| macOS arm64 | 3.12 | yes (`post61`, local; `post9`, public) | full (`post61`); exact pushed source `33f8a4dae1d` produced a repaired primary and strict 180-wheel closure. Independent fresh short and full gates passed strict preflight, binary-only `sagelite[all-needed-extras]` installation, `pip check`, runtime isolation, all 102 selftest checks, all 3,953 installed standard modules with zero failures, and packaged pytest with 226 passes and 5 skips. The unrestricted sweep completed in 747.9 seconds, and the earlier prime-square failure did not recur | smoke (`post8`) |
| macOS arm64 | 3.13 | yes (`post51`, local; `post9`, public) | full (`post51`); exact pushed source `30bc6ffce55` produced a repaired 102,092,637-byte primary and strict 179-wheel closure. Independent fresh neutral-path short and full gates passed preflight, wheel-only `sagelite[all-needed-extras]` installation, `pip check`, selftest, runtime isolation, packaged pytest, and all 3,953 installed `--optional=sage` modules with zero failures. Detailed evidence is in `agents/sagelite-macos-arm64-cp313-validation.md` | smoke (`post8`) |
| macOS arm64 | 3.14 | yes (`post54`, local; `post9`, public) | full (`post54`); exact pushed source `cf0c58f7131` produced a repaired 102,365,990-byte primary and strict 168-wheel closure. Independent fresh neutral-path short and full gates passed preflight, wheel-only `sagelite[all-needed-extras]` installation, `pip check`, runtime isolation, selftest, packaged pytest, and all 3,953 installed `--optional=sage` modules with zero failures. Detailed evidence is in `agents/sagelite-macos-arm64-cp314-validation.md` | smoke (`post8`) |

The recorded full passes establish that the standard installed runtime can
pass on Linux x86_64, Linux aarch64, and macOS arm64. They are not a
synchronized 3-by-3 release-candidate run. Final matrix completion requires a
fresh full pass for all nine cells from one selected release-candidate
revision.

The optional-wheel-ready extra currently names 19 packages:

```text
admcycles, biopython, clarabel, cvxpy, cylp, ecos, GitPython, highspy,
joblib, nibabel, osqp, pybtex, pygraphviz, pyscipopt, python-flint, qdldl,
scs, SQLAlchemy, texttable
```

The 17-package `post8` version passed install smoke on all seven existing
wheel targets. `post9` adds `highspy` and `joblib`; the complete 19-package
extra has so far been validated only on Linux x86_64 CPython 3.14. `ecos` is
selected only on Linux x86_64 CPython 3.12. `GitPython` expects system `git`.

## Work Order

Unless newer evidence changes the matrix, use this order:

1. Exact pushed `post61` square-order source `33f8a4dae1d` is accepted on
   macOS arm64 CPython 3.12 and Linux aarch64 CPython 3.12 and 3.13. Complete
   the synchronized full standard-suite rerun from that exact
   release-candidate revision across the remaining six cells. The
   accepted `post60` gates remain useful baselines, and the possibly surviving
   Linux x86_64 CPython 3.12 `post60` job must still be reconciled when `host`
   returns, but they cannot establish the final matrix after the shared source
   repair.
2. Validate the current optional-wheel-ready extra across all nine cells,
   using environment markers for genuinely unavailable packages.
3. Resume systematic optional-package expansion in install-smoke batches.

If a failure is shared by several cells, fix it once on the fastest relevant
cell, validate the focused fix there, then rebuild and retest every affected
cell. Do not mark other cells passed by inference.

## One Automation Iteration

An iteration owns one target cell and, after the first failure, one coherent
failure class. It should end with either a validated commit and updated matrix
evidence, or a precise blocker with preserved artifacts.

### 1. Reconcile State

Before doing work:

1. Read this file, `SAGELITE.md`, and the relevant validation report under
   `agents/`.
2. Check the canonical worktree with `git status --short` and inspect recent
   commits. Preserve all changes not made by the current iteration.
3. Record the current source SHA, branch, target cell, and preview version.
4. Inspect the public R2 manifest rather than assuming the previous turn
   published successfully.
5. Inspect the assigned remote host for an active automation-owned process and
   existing `exit-code` or validation metadata before starting another job.
6. Check free disk space on every filesystem the iteration will use.

Do not restart a completed build merely because the conversational session was
recovered. Conversely, do not assume a process survived merely because its
directory exists. Check the PID, process, log growth, and exit-code artifact.

### 2. Preflight The Assigned Host

Useful read-only checks are:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=15 host \
  'uname -m; df -h / /mnt/cocalc-scratch'

ssh -o BatchMode=yes -o ConnectTimeout=15 m1 \
  '/bin/zsh -lic "
    uname -m
    df -h /Volumes/sage
    command -v brew
    command -v python3.12
    command -v python3.13
    command -v python3.14
    command -v docker
    command -v multipass
  "'
```

For Linux arm64, additionally prove that the selected container or VM is
usable and native:

```text
uname -s  -> Linux
uname -m  -> aarch64 or arm64
```

If `host` is unreachable, report it and continue only with independent work
assigned to `m1` or the controller. If the Linux arm64 backend on `m1` needs
administrator authentication, report the exact command or service that needs
attention and stop that target. Do not change host assignment automatically.

### 3. Prepare Exact Source Input

Make code changes only in `/home/user/sage`. Remote build trees are disposable
copies, not independent development branches.

For an exploratory build, transfer the working source plus a saved diff and
label the result non-authoritative. Before final validation:

1. run focused local tests;
2. commit the coherent change in the canonical repository;
3. transfer or check out that exact commit on the assigned builder;
4. verify the remote `git rev-parse HEAD` equals the recorded SHA;
5. create a new per-SHA build directory rather than mutating an old source
   tree in place.

Prefer a git clone, git bundle, or an explicitly verified source archive over
an opaque recursive copy. Use `origin/develop` as a remote build source only
after the current commit has been pushed and its remote SHA verified.

### 4. Build The Wheel Contract

The Linux matrix and build environment in `.github/workflows/release.yml` are
the source of truth. Reuse:

- `.github/workflows/cibw-before-all-linux.sh`;
- `.github/workflows/cibw-before-build-linux.sh`;
- `.github/workflows/cibw-build-wheel-linux.sh`;
- `.github/workflows/repair-wheel-linux.sh`.

Use `CIBW_BUILD=cp3XX-manylinux_<arch>` and the matching `CIBW_ARCHS`. Do not
replace the repaired manylinux build with a raw local wheel. Keep ccache and
download caches under the assigned bulk filesystem and cap their size.

For Linux aarch64 on `m1`, run the same CIBW contract in native arm64 Linux.
Do not cross-compile native Sage extensions on macOS. Reuse compatible
`py3-none-manylinux_*_aarch64` companion wheels only when the strict validator
confirms their tags and declared versions satisfy the selected primary wheel.

For macOS, build natively on `m1`, use the existing macOS repair helpers, and
record every Homebrew and repair command in the run metadata. Current preview
wheels are tagged `macosx_26_0_arm64`; reducing the deployment target is
desirable but separate from proving the current matrix.

Every wheelhouse must include SHA256 hashes and a machine-readable or concise
text inventory. Record the primary wheel, companion wheel count, third-party
wheel count, Python tag, ABI tag, platform tags, and total bytes.

### 5. Validate A Fresh Wheel-Only Install

Never validate in the build environment. Create a fresh venv outside the
source checkout with user-site packages disabled and inherited Sage runtime
variables removed.

For authoritative Linux proof, use the repository validator and its strict
repaired-wheelhouse profile:

```bash
python3 tools/validate-sagelite-wheelhouse.py \
  --wheelhouse "${WHEELHOUSE}" \
  --work-dir "${RUN_ROOT}" \
  --python "${PYTHON}" \
  --package "sagelite[all-needed-extras]==${VERSION}" \
  --strict-repaired-wheelhouse-preflight \
  --optional sage \
  --short 600 \
  --nthreads "${NTHREADS}"
```

The short run is a gate, not acceptance. Inspect `validation-summary.md`,
`install-metadata.json`, selftest output, runtime summary, manifest, and reduced
doctest analysis before starting the full sweep.

The repaired strict profile defines a Linux proof. For macOS, use the named
strict profile so the same closure, version, interpreter, ABI, architecture,
and host-compatible platform checks run against a primary `macosx` wheel:

```bash
python3 tools/validate-sagelite-wheelhouse.py \
  --wheelhouse "${WHEELHOUSE}" \
  --work-dir "${RUN_ROOT}" \
  --python "${PYTHON}" \
  --package "sagelite[all-needed-extras]==${VERSION}" \
  --strict-macos-wheelhouse-preflight \
  --optional sage \
  --short 600 \
  --nthreads "${NTHREADS}"
```

Public-index smoke is an additional gate after local wheelhouse validation:

```bash
python -m pip install --no-cache-dir --only-binary=:all: \
  --extra-index-url https://sagelite.sagemath.org/dev/simple/ \
  "sagelite==${VERSION}"
python -m pip check
sagelite-selftest
```

Run from a neutral directory. Verify representative polynomial and matrix
arithmetic plus GAP, Singular, Maxima, PARI/GP, and other standard companion
commands selected by `sagelite-selftest`.

### 6. Run The Full Standard Suite

After the short gate passes, run the same fresh installed wheelhouse with:

```bash
python3 tools/validate-sagelite-wheelhouse.py \
  --wheelhouse "${WHEELHOUSE}" \
  --work-dir "${RUN_ROOT}" \
  --python "${PYTHON}" \
  --package "sagelite[all-needed-extras]==${VERSION}" \
  --strict-repaired-wheelhouse-preflight \
  --optional sage \
  --full \
  --nthreads "${NTHREADS}"
```

Use `--strict-repaired-wheelhouse-preflight` on Linux and
`--strict-macos-wheelhouse-preflight` on macOS. Both profiles create a fresh
wheel-only venv, run `pip check` and selftest, and invoke the installed doctest
runner with the wheelhouse recorded explicitly.

For macOS full runs, the accepted current workaround is:

```bash
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

Record that setting in the validation metadata. It avoids an Objective-C
fork-safety abort in proxy detection used by one URL-opening doctest; it must
not be silently inherited.

A pass requires both process exit code zero and reduced analysis with zero
real failures. Warning-only File/Warning blocks are not failures, but actual
failed examples, explicit failure counts, failed stats entries, framework
errors, and timeouts are failures.

### 7. Triage And Fix Failures

Use the reduced analysis before opening the full log. Group failures into:

- missing or incorrectly repaired native library;
- missing companion executable or data;
- stale build/install path or inherited host state;
- runtime protocol or output mismatch;
- Python/NumPy/compiler/platform behavior difference;
- real Sage defect;
- flaky, randomized, timing-sensitive, or resource-sensitive test;
- optional package test accidentally included in the standard run.

Fix one coherent class at a time. Prefer additive packaging metadata,
companion runtime fixes, runtime discovery, and generally useful Sage fixes.
Upstream mergeability is a first-class invariant.

Do not use blanket `# random`, broad skips, relaxed comparison, or optional-tag
changes to hide packaging failures. A doctest expectation may change only when
the output variation is mathematically correct and narrowly justified. Add a
focused regression test whenever practical.

After a fix:

1. run the focused failing modules or tool tests;
2. rebuild only the affected primary or companion wheels when safe;
3. rerun the clean-install short gate;
4. rerun the full cell before marking it `full`;
5. identify every other matrix cell invalidated by the change.

### 8. Validate Optional-Wheel-Ready Separately

After the standard smoke gate passes, validate the optional extra without
making it a prerequisite for standard-suite acceptance:

```bash
python -m pip install --no-cache-dir --only-binary=:all: \
  --extra-index-url https://sagelite.sagemath.org/dev/simple/ \
  "sagelite[optional-wheel-ready]==${VERSION}"
python -m pip check
```

Run the import and representative solver smoke recorded in
`agents/sagelite-optional-wheel-ready-matrix-validation.md`. Record skipped
packages caused by environment markers. A missing optional wheel may result in
a narrower marker or a deferred candidate; it must not be papered over as a
standard dependency.

When expanding optional coverage, add small install-smoke batches. Require
binary-only resolution, clean installation, `pip check`, import tests, and one
meaningful operation before adding a package to `optional-wheel-ready`.

### 9. Record Evidence And Commit

For every completed change set:

1. update the relevant row in this matrix checkpoint;
2. add or update a concise report under `agents/` with absolute artifact paths,
   source SHA, wheel versions, commands, and result;
3. run relevant focused repository tests;
4. inspect `git diff --check` and `git status --short`;
5. commit automatically using the repository's required area-prefixed subject
   and useful markdown body;
6. immediately push the commit with `git push origin HEAD:develop`;
7. verify that `git ls-remote origin refs/heads/develop` reports the committed
   SHA before beginning another change set.

The configured upstream for this loop is
`git@github.com:sagemathinc/sagelite.git`, branch `develop`. A validated commit
is not complete until its push is verified. Retry transient network failures
reasonably. If a push is rejected because the remote changed, fetch and inspect
the remote commits, then reconcile without discarding either side. Never use a
force push, rewrite published history, or push to another repository or branch
without explicit user direction. If a safe push cannot be completed, preserve
the local commit, report the exact failure, and stop before accumulating more
local-only commits.

Do not amend earlier commits by default. Never revert or absorb unrelated
worktree changes.

Use exact claims:

- say `wheel built` only after wheel inventory and tag checks;
- say `install passed` only after a fresh wheel-only install and `pip check`;
- say `smoke passed` only after runtime probes;
- say `full passed` only after the complete standard installed suite;
- identify the preview version and source SHA for every claim.

### 10. Publish Only Validated Preview Artifacts

R2 `dev` publication is allowed only after per-cell wheelhouse validation and
a dry run. PyPI publication is never part of this loop without a new explicit
user instruction.

The publication script synchronizes the generated `simple/` index with
deletion. Therefore, never publish a wheelhouse containing only the newly built
cell. First assemble a merged wheelhouse containing every artifact that should
remain visible.

Publication rules:

- never reuse a versioned filename for different bytes;
- retain already-supported cells when adding a cell;
- verify hashes and reject duplicate normalized project/version/tag entries;
- generate the index locally and inspect the primary Sagelite page;
- run with `SAGELITE_PUBLISH_DRY_RUN=1` first;
- publish only to the `dev` prefix;
- verify the public root, simple project page, wheel URLs, and manifest;
- perform a fresh public-index install for the changed cell;
- keep the previous preview version indexed for rollback until the new matrix
  has sufficient feedback.

Current command shape:

```bash
AWS_BIN=/scratch/sagelite-r2-tools/bin/aws \
SAGELITE_SIMPLE_INDEX_URL=https://sagelite.sagemath.org/dev/simple/ \
SAGELITE_PUBLISH_DRY_RUN=1 \
tools/publish-sagelite-r2-wheel-index.sh "${MERGED_WHEELHOUSE}" dev
```

Repeat without `SAGELITE_PUBLISH_DRY_RUN` only after inspecting the dry run.
Do not print the sourced environment or run shell tracing while the R2 secret
is loaded.

### 11. Clean Up Deliberately

After recording evidence and copying needed wheels to the merged staging area:

Retain:

- the current validated wheelhouse for each matrix cell;
- validation summaries, metadata, reduced analyses, and final logs;
- the latest useful failed run for an unresolved failure class;
- bounded compiler/download caches that materially speed the next run;
- the exact merged wheelhouse used for the current R2 publication.

Remove only automation-owned:

- superseded venvs;
- extracted source and disposable build trees;
- duplicate downloads outside the bounded cache;
- old failed runs whose useful logs have been archived;
- obsolete merged wheelhouses after a newer one is published and verified.

Record disk usage after cleanup. Never use broad deletion patterns against
`/scratch`, `/mnt/cocalc-scratch`, or `/Volumes/sage`.

## Durable Long-Running Jobs

Builds and full doctest runs must survive SSH disconnects and conversation
recovery. Use a durable remote process mechanism that writes one log, PID, and
exit-code file into the run directory. `nohup` or an existing terminal
multiplexer is acceptable. Do not rely on an interactive SSH channel as the
only owner of a many-hour process.

The loop should poll without launching duplicates. A running process is healthy
only when the PID exists, the command matches the recorded run, and the log or
resource counters show plausible progress. If the process died, preserve its
log and metadata, classify the failure, and resume from the earliest invalid
phase rather than rebuilding blindly.

If the host itself restarts, first inspect the run directory, container state,
and filesystem consistency. Never assume a missing PID means its partial
wheelhouse is valid.

## Stop And Ask The User When

Stop the affected target and provide a precise status when:

- administrator action is required to start or authenticate the Linux arm64
  backend on `m1`;
- an SSH alias remains unreachable after reasonable retries;
- an automation-created commit cannot be pushed and verified on
  `origin/develop` after reasonable retries and safe reconciliation;
- the assigned bulk filesystem lacks space and safe automation-owned cleanup
  cannot restore the threshold;
- work would require publishing to PyPI, changing DNS, rotating secrets, or
  broadening public access;
- a package has a nonfree or unclear redistribution constraint;
- an unrelated worktree change makes a safe commit impossible;
- the only apparent route is a broad test skip or a material architectural
  departure from upstream Sage.

Host unavailability does not block independent work on another correctly
assigned host. Continue only when doing so cannot invalidate or duplicate the
active target.

## Project Completion

The matrix goal is complete when one release-candidate source SHA has all nine
rows marked `full`, with wheel-only clean-install evidence and public-index
install smoke for every row. At that point:

1. regenerate the merged R2 preview index from the nine validated cells;
2. rerun the documented copy-paste install commands;
3. summarize wheel sizes and installed disk usage per platform;
4. collect developer feedback for a defined preview period;
5. prepare, but do not execute, a PyPI publication plan for a thin `sage`
   package and the Sagelite/companion distributions.

Broad optional-package coverage remains an ongoing track after matrix
completion. Its progress should be reported as package and platform counts,
not folded into the standard-suite pass rate.

## References

- User-facing preview instructions and support status: `SAGELITE.md`
- Historical runtime parity work: `agents/sagelite-pip-runtime-parity-plan.md`
- macOS arm64 CPython 3.13 evidence:
  `agents/sagelite-macos-arm64-cp313-validation.md`
- macOS arm64 CPython 3.14 evidence:
  `agents/sagelite-macos-arm64-cp314-validation.md`
- Optional matrix evidence:
  `agents/sagelite-optional-wheel-ready-matrix-validation.md`
- Optional package inventory: `agents/sagelite-optional-package-inventory.md`
- Copy-paste preview evidence:
  `agents/sagelite-copy-paste-preview-validation.md`
- Linux x86_64 CPython 3.12 evidence:
  `agents/sagelite-linux-x86_64-cp312-validation.md`
- Linux build matrix and CIBW contract: `.github/workflows/release.yml`
- Wheelhouse validator: `tools/validate-sagelite-wheelhouse.py`
- Installed doctest runner: `tools/run-installed-wheel-doctests.py`
- Doctest reducer: `tools/analyze-doctest-log.py`
- R2 publisher: `tools/publish-sagelite-r2-wheel-index.sh`
