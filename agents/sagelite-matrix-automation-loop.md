# Sagelite Matrix Automation Loop

Last reviewed: 2026-07-14

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
filesystem was enlarged and had about 104 GiB free at the latest controller
check, just above the heavy-build threshold in this runbook. It is suitable
for an x86_64 rebuild, but monitor space closely and retain the deliberate
cleanup policy. Treat future SSH reachability failures as a preflight problem,
not as evidence that the host assignment has changed.

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
| Linux x86_64 | 3.12 | yes (`post9`) | full baseline; 3,953 modules and 0 failures on the earlier accepted build | smoke (`post8`) |
| Linux x86_64 | 3.13 | yes (`post9`) | smoke only | smoke (`post8`) |
| Linux x86_64 | 3.14 | yes (`post9`) | smoke only | smoke (`post9`) |
| Linux aarch64 | 3.12 | yes (`post9`) | smoke only; previous validation used qemu on x86_64 | smoke (`post8`), with system `git` for GitPython |
| Linux aarch64 | 3.13 | yes (`post20`, local) | the exact committed `post20` primary and matching Maxima wheel built successfully. Its fresh strict 177-wheel installation, `pip check`, every selftest probe, and packaged pytest passed natively, but the 3,954-module `--optional=sage` short sweep failed ten modules: eight core-supported and two optional-external. The preceding five-example msolve/result-display class is absent. Exact pushed `post21` source `396f11c604fd63438235c6bf825571bd7a8851c2` relocates Giac's missing completion database; its exact-SHA Giac `post1` companion passed a clean native completion smoke, and its exact-SHA primary rebuild plus gated short/full watcher are active. No `post21` primary wheel is claimed, and the cell remains below `full` | none |
| Linux aarch64 | 3.14 | missing | none | none |
| macOS arm64 | 3.12 | yes (`post9`) | full baseline plus packaged pytest on an earlier accepted build | smoke (`post8`) |
| macOS arm64 | 3.13 | yes (`post9`) | smoke only | smoke (`post8`) |
| macOS arm64 | 3.14 | yes (`post9`) | smoke only | smoke (`post8`) |

The two existing full baselines establish that the standard installed runtime
can pass on Linux x86_64 and macOS arm64. They are not a synchronized
`post9` 3-by-3 release-candidate run. Final matrix completion requires a fresh
full pass for all nine cells from one selected release-candidate revision.

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

1. Build and clean-install validate Linux aarch64 CPython 3.13 on `m1`.
2. Build and clean-install validate Linux aarch64 CPython 3.14 on `m1`.
3. Run and fix the full standard suite on Linux x86_64 CPython 3.14 on
   `host`; this is the highest-priority cocalc.ai target.
4. Run and fix the full standard suite on Linux x86_64 CPython 3.13.
5. Run and fix the full standard suite on macOS arm64 CPython 3.13.
6. Run and fix the full standard suite on macOS arm64 CPython 3.14.
7. Run and fix the full standard suite on native Linux aarch64, beginning
   with CPython 3.12 and then 3.13 and 3.14.
8. Select one release-candidate commit and rerun the full standard suite on
   all nine cells, including the two earlier CPython 3.12 baselines.
9. Validate the current optional-wheel-ready extra across all nine cells,
   using environment markers for genuinely unavailable packages.
10. Resume systematic optional-package expansion in install-smoke batches.

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

The strict profile currently defines a repaired Linux proof. For macOS, use a
fresh wheel-only install plus the compatible generic wheelhouse preflights and
the installed doctest runner. A useful implementation task is to add a named
macOS strict profile rather than maintaining a long ad hoc flag list.

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

Use the strict profile only on Linux until a macOS profile exists. On macOS,
invoke `tools/run-installed-wheel-doctests.py` from the clean wheel-only venv
with `--runtime-summary --selftest --optional sage --full` and record the
wheelhouse explicitly.

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
- Optional matrix evidence:
  `agents/sagelite-optional-wheel-ready-matrix-validation.md`
- Optional package inventory: `agents/sagelite-optional-package-inventory.md`
- Copy-paste preview evidence:
  `agents/sagelite-copy-paste-preview-validation.md`
- Linux build matrix and CIBW contract: `.github/workflows/release.yml`
- Wheelhouse validator: `tools/validate-sagelite-wheelhouse.py`
- Installed doctest runner: `tools/run-installed-wheel-doctests.py`
- Doctest reducer: `tools/analyze-doctest-log.py`
- R2 publisher: `tools/publish-sagelite-r2-wheel-index.sh`
